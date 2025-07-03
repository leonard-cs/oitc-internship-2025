import requests

from db_uploader.config import LLM_API_URL, LLM_API_KEY, LLM_WORKSPACE_ID

QUERY_TEXT = "show info of product 1"

def query_anythingllm(workspace_slug, query):
    url = f"{LLM_API_URL}/api/v1/workspace/{workspace_slug}/chat"
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "message": QUERY_TEXT,
        "mode": "query",  # 或 chat
        "sessionId": "example-session-id",  # 你可以隨便給一個 UUID 或文字
        "reset": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 回應內容：")
        print("Text:", data.get("textResponse"))
        print("來源文件：")
        for src in data.get("sources", []):
            title = src.get("title", "無標題")
            chunk = src.get("chunk", "無內容")
            print(f"- {title} : {chunk}")
    else:
        print("❌ 錯誤：", response.status_code, response.text)

# 執行查詢
query_anythingllm(LLM_WORKSPACE_ID, QUERY_TEXT)
