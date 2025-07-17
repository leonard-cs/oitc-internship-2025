def extract_payload_texts(results: list) -> list[str]:
    """
    Extracts 'text' field from the payloads in a list of Qdrant ScoredPoint results.

    Args:
        results (list): List of ScoredPoint objects (dicts or objects with `.payload`)

    Returns:
        list[str]: List of extracted text payloads
    """
    extracted = []
    for item in results:
        payload = getattr(item, 'payload', None)
        if isinstance(payload, dict) and 'text' in payload:
            extracted.append(payload['text'])
        else:
            print(f"Warning: Skipping item with missing or invalid payload: {item}")
    return extracted
