async def retrieve_relevant_documents(query: str) -> tuple[list[str], list[str]]:
    # Simulate document retrieval
    docs = [
        "Product 'Chai' (ID 1) is supplied by supplier #1 under category #1. Each unit contains '10 boxes x 20 bags' and costs $18.00. There are 39 in stock, 0 on order, and the reorder level is 10. It is currently available.",
        "Product 'Chang' (ID 2) is supplied by supplier #1 under category #1. Each unit contains '24 - 12 oz bottles' and costs $19.00. There are 17 in stock, 40 on order, and the reorder level is 25. It is currently available.",
        "Product 'Aniseed Syrup' (ID 3) is supplied by supplier #1 under category #2. Each unit contains '12 - 550 ml bottles' and costs $10.00. There are 13 in stock, 70 on order, and the reorder level is 25. It is currently available.",
        "Product 'Chef Anton's Cajun Seasoning' (ID 4) is supplied by supplier #2 under category #2. Each unit contains '48 - 6 oz jars' and costs $22.00. There are 53 in stock, 0 on order, and the reorder level is 0. It is currently available.",
        "Product 'Chef Anton's Gumbo Mix' (ID 5) is supplied by supplier #2 under category #2. Each unit contains '36 boxes' and costs $21.35. There are 0 in stock, 0 on order, and the reorder level is 0. It is currently discontinued.",
    ]
    sources = [f"Product {i}" for i in range(1, 6)]
    return docs, sources
