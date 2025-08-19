from app.chat.models import ChatRequest, ChatResponse
from app.chat.service import (
    handle_chat_request,
    handle_chat_request_image,
    handle_chat_request_sql,
)
from app.config import backend_logger
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

router = APIRouter()


@router.post(
    "/vector-rag-query",
    response_model=ChatResponse,
    summary="Process Chat Query with RAG Pipeline",
    description="Process a user query through the complete Retrieval-Augmented Generation (RAG) chatbot pipeline with optional query preprocessing",
)
async def vector_rag_query(payload: ChatRequest) -> ChatResponse:
    """
    Process a user query through the full RAG chatbot pipeline.

    This endpoint handles general chat queries by:
    1. Optionally preprocessing the query through a query processor for better understanding
    2. Retrieving relevant context from the vector database
    3. Generating a comprehensive response using the LLM with retrieved context
    4. Returning the answer along with source references

    Args:
        payload (ChatRequest): The chat request containing:
            - user_query (str): The user's question or query
            - use_query_processor (bool, optional): Whether to preprocess the query for better retrieval. Defaults to False.

    Returns:
        ChatResponse: Contains:
            - semantic_query (str): The processed/semantic version of the query
            - answer (str): The generated response from the LLM
            - sources (list[str]): List of source document references used
            - tools_used (list, optional): Any tools that were utilized during processing

    Raises:
        HTTPException: 500 status code if processing fails
    """
    try:
        result: ChatResponse = await handle_chat_request(
            user_query=payload.user_query,
            use_query_processor=payload.use_query_processor,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/sql-rag-query",
    response_model=ChatResponse,
    summary="Process SQL-Based Query with RAG Pipeline",
    description="Process a user query through the SQL-focused Retrieval-Augmented Generation pipeline for database-related questions",
)
async def sql_rag_query(
    query: str = Query(
        ..., description="The user's natural language query about database content"
    ),
) -> ChatResponse:
    """
    Process a user query through the SQL RAG chatbot pipeline.

    This endpoint is specifically designed for database-related queries and:
    1. Analyzes the user's natural language query to understand database intent
    2. Identifies relevant database tables and schemas
    3. Generates appropriate SQL queries when needed
    4. Retrieves and processes database information
    5. Provides natural language responses based on database content

    Args:
        query (str): The user's natural language question about database content.
                    Examples: "Show me sales data from last month", "What customers are from California?"

    Returns:
        ChatResponse: Contains:
            - semantic_query (str): The processed/semantic version of the query
            - answer (str): Natural language response based on database content
            - sources (list[str]): Database tables or sources referenced
            - tools_used (list, optional): SQL queries or database tools used

    Raises:
        HTTPException: 500 status code if SQL processing or database query fails
    """
    try:
        result: ChatResponse = await handle_chat_request_sql(user_query=query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/image-query",
    response_model=ChatResponse,
    summary="Process Image-Based Query with Multimodal RAG",
    description="Analyze uploaded images and answer questions about their content using multimodal Retrieval-Augmented Generation",
)
async def image_query(
    file: UploadFile = File(..., description="Image file to analyze (JPEG, PNG, etc.)"),
    user_query: str = Query(
        ..., description="Question or query about the uploaded image content"
    ),
) -> ChatResponse:
    """
    Process a user query through the image RAG pipeline using multimodal analysis.

    This endpoint enables image-based question answering by:
    1. Processing and analyzing the uploaded image by generating image embeddings
    3. Combining image embeddings with text-based context retrieval
    4. Generating comprehensive textual information responses
    5. Providing relevant sources and context for the image query

    Args:
        file (UploadFile): The image file to analyze. Supported formats include:
                          JPEG, PNG, GIF, BMP, and other common image formats.
        user_query (str): The question or query about the image content.
                         Examples: "What objects are in this image?", "Describe the scene",
                         "What text can you read in this image?"

    Returns:
        ChatResponse: Contains:
            - semantic_query (str): The processed version of the user's query
            - answer (str): Comprehensive response combining image analysis and retrieved context
            - sources (list[str]): Sources used for context and image analysis
            - tools_used (list, optional): Computer vision tools and models used

    Raises:
        HTTPException: 500 status code if image processing, analysis, or query processing fails
    """
    backend_logger.info(
        f"Image query requested with file={file.filename}, user query={user_query}"
    )
    try:
        result: ChatResponse = await handle_chat_request_image(
            user_query=user_query, image=file
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
