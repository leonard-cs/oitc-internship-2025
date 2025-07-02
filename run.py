from db_uploader.extract_mssql import export_to_json
from db_uploader.upload_to_anythingllm import upload_file_to_llm

def main():
    table = "Products"  # change this
    output_file = f"{table}.json"

    export_to_json(table, output_file)
    upload_file_to_llm(output_file)
    # curl -H "Authorization: Bearer 690B86Y-SHZMP6S-PW7EGWJ-N0F08H3" http://localhost:3001/api/v1/workspaces

if __name__ == "__main__":
    main()
