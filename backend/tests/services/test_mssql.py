# import pytest
# from app.mssql.dependencies import get_SQLDatabase
# from app.mssql.models import Table
# from app.mssql.services import sync_table_ai
# from app.vectorstore.utils import generate_uuid


# @pytest.mark.asyncio
# async def test_sync_table_ai():
#     limit = 3
#     table = Table.products
#     expected_doc_ids = [f"{table.value}_{i}" for i in range(1, limit + 1)]

#     synced_ids = await sync_table_ai(get_SQLDatabase(), table, limit=limit)

#     assert len(synced_ids) == limit, f"Expected {limit} IDs, got {len(synced_ids)}"
#     for id in expected_doc_ids:
#         expected_uuid = generate_uuid(id)
#         assert expected_uuid in synced_ids, f"Missing expected doc id: {id}"
