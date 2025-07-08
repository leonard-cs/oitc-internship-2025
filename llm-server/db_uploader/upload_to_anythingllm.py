# db_uploader/upload_to_anythingllm.py
import os
import requests
from db_uploader.config import LLM_API_URL, LLM_API_KEY, LLM_WORKSPACE_ID

def upload_file_to_llm(file_path: str):
    url = f"{LLM_API_URL}/api/v1/document/upload"
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "accept": "application/json"
    }

    try:
        with open(file_path, "rb") as f:
            files = {
                "file": (os.path.basename(file_path), f, "application/json"),
                "addToWorkspaces": (None, LLM_WORKSPACE_ID)
            }
            response = requests.post(url, headers=headers, files=files)

        print(f"✅ Upload response: {response.status_code}")
        try:
            print("📦 Response JSON:", response.json())
        except Exception:
            print("⚠️ Response not JSON:")
            print(response.text)
    except Exception as e:
        print(f"❌ Upload failed: {e}")
