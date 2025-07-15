# run.py
import glob

from db_uploader.extract_mssql import *
from db_uploader.upload_to_anythingllm import upload_file_to_llm
from db_uploader.utils import *

def main():
    mode = 'txt'
    # mode = 'json'
    table = "Products"  # change this
    output_folder = table

    clear_output_files(output_folder, mode)

    if mode == 'txt':
        # export_each_product_to_txt(table, output_folder)
        # export_product_with_discontinued_and_stock(table, output_folder)
        # export_sentence(table, output_folder)
        export_all_products_as_sentences(table, output_folder)
    else:
        export_each_product_to_json(table, output_folder)

    for file_path in glob.glob(f"{output_folder}/*.{mode}"):
        upload_file_to_llm(file_path)
    print(f"\n✅ Upload complete")

if __name__ == "__main__":
    main()
