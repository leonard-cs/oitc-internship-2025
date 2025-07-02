import glob

from db_uploader.extract_mssql import export_each_product_to_json
from db_uploader.upload_to_anythingllm import upload_file_to_llm

def main():
    table = "Products"  # change this
    output_folder = table

    export_each_product_to_json(table, output_folder)

    for file_path in glob.glob(f"{output_folder}/*.json"):
        upload_file_to_llm(file_path)
    print(f"\n✅ Upload complete")

if __name__ == "__main__":
    main()
