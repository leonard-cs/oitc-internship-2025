import io
import os
from datetime import datetime

import pyodbc
from app.config import backend_logger
from app.embed.service import get_image_file_embeddings, get_text_embeddings
from app.llm.ollama import get_ollama
from app.llm.prompts import get_document_prompt
from app.mssql.models import ImageTable, LLMDocumentResponse, Table
from app.mssql.utils import delete_file, extract_sql_results, remove_sample_rows
from app.vectorstore.service import get_vectorstore
from app.vectorstore.utils import generate_uuid
from langchain_community.utilities import SQLDatabase
from PIL import Image
from PIL.ImageFile import ImageFile


def fetch_table_names(db: SQLDatabase) -> list[str]:
    return list(db.get_usable_table_names())


def fetch_table_info(db: SQLDatabase, table_names: list[str]) -> str:
    return db.get_table_info(table_names)


async def sync_table_ai(
    db: SQLDatabase, table: Table, limit: int | None = None
) -> list[str]:
    table_info = remove_sample_rows(fetch_table_info(db, [table.value]))
    table_name = table.value

    rows = db.run_no_throw(table.sql(limit=limit), fetch="all", include_columns=True)
    parsed_rows = extract_sql_results(rows)

    if not parsed_rows:
        backend_logger.error(f"No rows found for table {table_name}")
        raise Exception(f"No rows found for table {table_name}")
    backend_logger.debug(f"Retrieved {len(parsed_rows)} rows from table {table_name}")

    document_ids: list[str] = []
    contents: list[str] = []
    ids: list[str] = []
    metadata: list[dict[str, any]] = []
    embeddings: list[list[float]] = []

    for count, row in enumerate(parsed_rows):
        id, text = await generate_text_and_id(table_name, row, table_info)

        if not id or not text:
            backend_logger.warning("Document generation failed, skipping row")
            continue

        document_id = f"{table_name}_{id}"
        document_ids.append(document_id)
        contents.append(text)
        embeddings.append(get_text_embeddings(text))
        metadata.append({"source": document_id, "created_at": str(datetime.now())})
        ids.append(generate_uuid(document_id))

        if (count + 1) % 5 == 0 or count + 1 == len(parsed_rows):
            backend_logger.info(
                f"Processed {count + 1}/{len(parsed_rows)} rows in {table_name}"
            )

    vectorstore = get_vectorstore()
    added_ids = vectorstore.upload_collection(
        collection_name=table_name,
        vectors=embeddings,
        page_contents=contents,
        metadata=metadata,
        ids=ids,
    )

    backend_logger.trace(f"Document ids: {document_ids}")
    return added_ids


def extract_images(
    db_connection: pyodbc.Connection, table: ImageTable, export_dir: str = "exports"
) -> str:
    cursor = db_connection.cursor()
    cursor.execute(table.sql_image())

    folder_name = f"{table.value}-images"
    folder_path = os.path.join(export_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    count = 0
    for id, image in cursor.fetchall():
        # Strip the OLE header (78 bytes) if present
        image_data = image[78:]

        filename = f"{folder_name}_{id}.jpg"
        file_path = os.path.join(folder_path, filename)

        delete_file(path=folder_path, prefix=f"{folder_name}_{id}", suffix=".jpg")

        with open(file_path, "wb") as f:
            f.write(image_data)
        count += 1
    backend_logger.success(f"Exported {count} images")
    return export_dir


async def sync_table_images(
    db_connection: pyodbc.Connection, db: SQLDatabase, image_table: ImageTable
) -> list[str]:
    cursor = db_connection.cursor()
    cursor.execute(image_table.sql_image())

    image_embeddings: list[list[float]] = []

    for id, image in cursor.fetchall():
        # Strip OLE header (first 78 bytes) if needed
        image_data = image[78:]

        try:
            image_file: ImageFile = Image.open(io.BytesIO(image_data))
            image_file.load()  # Load the image to make sure it's not lazy-loaded
            image_embeddings.append(get_image_file_embeddings(image_file))

        except Exception as e:
            backend_logger.warning(f"Failed to process image ID {id}: {e}")
    backend_logger.success(f"{len(image_embeddings)} images processed")

    full_table = Table(image_table.value)

    table_info = remove_sample_rows(fetch_table_info(db, [full_table.value]))
    table_name = full_table.value

    rows = db.run_no_throw(full_table.sql(), fetch="all", include_columns=True)
    parsed_rows = extract_sql_results(rows)

    if not parsed_rows:
        backend_logger.error(f"No rows found for table {table_name}")
        raise Exception(f"No rows found for table {table_name}")
    backend_logger.debug(f"Retrieved {len(parsed_rows)} rows from table {table_name}")

    document_ids: list[str] = []
    contents: list[str] = []
    ids: list[str] = []
    metadata: list[dict[str, any]] = []
    for count, row in enumerate(parsed_rows):
        id, text = await generate_text_and_id(table_name, row, table_info)

        if not id or not text:
            backend_logger.warning("Document generation failed, skipping row")
            continue

        document_id = f"{table_name}_image_{id}"
        document_ids.append(document_id)
        contents.append(text)
        metadata.append({"source": document_id, "created_at": str(datetime.now())})
        ids.append(generate_uuid(document_id))

        if (count + 1) % 5 == 0 or count + 1 == len(parsed_rows):
            backend_logger.info(
                f"Processed {count + 1}/{len(parsed_rows)} rows in {table_name}"
            )

    vectorstore = get_vectorstore()
    added_ids = vectorstore.upload_collection(
        collection_name=table_name,
        vectors=image_embeddings,
        page_contents=contents,
        metadata=metadata,
        ids=ids,
    )
    backend_logger.trace(f"Document ids: {document_ids}")

    return added_ids


async def generate_text_and_id(
    table_name: str, row: str, table_info: str
) -> tuple[str, str] | None:
    ollama = get_ollama()
    structured_ollama = ollama.with_structured_output(LLMDocumentResponse)

    prompt_template = get_document_prompt()

    pipelines = (
        {
            "table_name": lambda x: x["table_name"],
            "row": lambda x: x["row"],
            "table_info": lambda x: x["table_info"],
        }
        | prompt_template
        | structured_ollama
    )

    response: LLMDocumentResponse = pipelines.invoke(
        {"table_name": table_name, "row": row, "table_info": table_info}
    )

    if not response.id or not response.text:
        backend_logger.error("No id or text found in the response")
        backend_logger.trace(f"Response: {response}")
        return None
    # backend_logger.trace(f"Response: {response}")
    # backend_logger.success(
    #     f"Document generated successfully, table: {table_name}, id: {response.id}"
    # )

    return response.id, response.text
