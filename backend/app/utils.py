from langchain_core.documents import Document


def documents_to_string(documents: list[Document]) -> str:
    return "\n\n".join(
        [
            f"{document.page_content} [Source: {document.metadata['source']}]"
            for document in documents
        ]
    )
