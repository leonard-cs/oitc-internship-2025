import os

import pyodbc
from app.config import backend_logger
from app.llm.ollama import get_ollama
from app.mssql.models import ImageTable, LLMDocumentResponse, Table
from app.mssql.utils import delete_file
from app.prompts.prompts import get_document_prompt
from app.vectorstore.service import get_qdrant_vector_store
from app.vectorstore.utils import generate_uuid
from langchain_community.utilities import SQLDatabase
from langchain_core.documents import Document


def fetch_table_names(db: SQLDatabase) -> list[str]:
    return list(db.get_usable_table_names())


def fetch_table_info(db: SQLDatabase, table_names: list[str]) -> str:
    return db.get_table_info(table_names)


def execute_sql(db: SQLDatabase, sql_query: str) -> str:
    return db.run_no_throw(sql_query)


async def sync_table_ai(
    db: SQLDatabase, table: Table, limit: int | None = None
) -> list[str]:
    table_info = parse_table_info(fetch_table_info(db, [table.value]))
    table_name = table.value

    rows = db.run_no_throw(table.sql(limit=3), fetch="all", include_columns=True)
    parsed_rows = parse_sql_result_string(rows)

    if not parsed_rows:
        backend_logger.error(f"No rows found for table {table_name}")
        raise Exception(f"No rows found for table {table_name}")
    backend_logger.debug(f"Retrieved {len(parsed_rows)} rows from table {table_name}")

    document_ids: list[str] = []
    documents: list[Document] = []
    ids: list[str] = []

    for row in parsed_rows:
        document_id_string, text = await generate_text_and_id(
            table_name, row, table_info
        )

        if not document_id_string or not text:
            backend_logger.warning("Document generation failed, skipping row")
            continue

        document_ids.append(document_id_string)
        document = Document(page_content=text, metadata={})
        documents.append(document)
        ids.append(generate_uuid(document_id_string))

    vector_store = get_qdrant_vector_store(table_name)
    added_ids = vector_store.add_documents(documents=documents, ids=ids)
    unique_added_ids = list(set(added_ids))

    backend_logger.trace(f"Document ids: {document_ids}")
    if len(unique_added_ids) != len(added_ids):
        backend_logger.success(
            f"{len(unique_added_ids)} / {len(added_ids)} documents added to collection {table_name}"
        )
    else:
        backend_logger.success(
            f"All {len(added_ids)} documents added to collection {table_name}"
        )

    return unique_added_ids


def extract_images(
    db_connection: pyodbc.Connection, table: ImageTable, export_dir: str = "exports"
) -> str:
    cursor = db_connection.cursor()
    cursor.execute(table.sql)

    folder_name = f"{table.value}-images"
    folder_path = os.path.join(export_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    count = 0
    for id, image in cursor.fetchall():
        # Strip the OLE header (78 bytes) if present
        image_data = image[78:]

        filename = f"{folder_name}_{id}.jpg"
        file_path = os.path.join(folder_path, filename)

        delete_file(path=folder_path, prefix=f"{folder_name}_{id}", sufix=".jpg")

        with open(file_path, "wb") as f:
            f.write(image_data)
        count += 1
    backend_logger.success(f"Exported {count} images")
    return export_dir


async def sync_table_images(table: ImageTable, export_dir: str) -> list[str]:
    # TODO: Implement this
    pass


def parse_table_info(table_info: str) -> str:
    table_info = table_info.split("/*")[0]
    return table_info


def parse_sql_result_string(result_string: str) -> list[str]:
    """
    Split a string representation of SQL results by closing braces.

    Args:
        result_string: String representation of SQL results

    Returns:
        List of strings split by '}'
    """
    parts = result_string.split("}")

    # Filter out empty strings and clean up
    cleaned_parts = []
    for part in parts:
        part = part.strip()
        if part and part != "]":  # Only add non-empty parts
            cleaned_parts.append(part)

    return cleaned_parts


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
    backend_logger.trace(f"Response: {response}")
    document_id_string = f"{table_name}_{response.id}"
    backend_logger.success(f"Document generated successfully, id: {document_id_string}")

    return document_id_string, response.text
