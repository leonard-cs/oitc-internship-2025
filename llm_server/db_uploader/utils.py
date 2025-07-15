import os
import glob

def clear_output_files(output_folder: str, extension: str):
    """
    Removes all files with the given extension from the output folder.
    """
    pattern = os.path.join(output_folder, f"*.{extension}")
    files = glob.glob(pattern)

    if not files:
        print(f"🧼 No .{extension} files found in '{output_folder}' to remove.")
        return

    for file_path in files:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"⚠️ Failed to delete {file_path}: {e}")
    
    print(f"🧹 Cleared {len(files)} .{extension} files from '{output_folder}'")

def product_info_to_sentence(data: dict) -> str:
    parts = []

    if "ProductID" in data and "ProductName" in data:
        parts.append(f"Product #{data['ProductID']} is called '{data['ProductName']}'")
    elif "ProductName" in data:
        parts.append(f"The product is called '{data['ProductName']}'")
    elif "ProductID" in data:
        parts.append(f"Product #{data['ProductID']}")

    if "UnitPrice" in data:
        parts.append(f"priced at ${data['UnitPrice']:.2f}")

    if "UnitsInStock" in data:
        parts.append(f"with {data['UnitsInStock']} units in stock")

    if "Discontinued" in data:
        if data["Discontinued"]:
            parts.append("and it has been discontinued")
        else:
            parts.append("and it is currently available")

    # Combine all parts into a full sentence
    sentence = " ".join(parts).strip()

    # Add punctuation if missing
    if sentence and not sentence.endswith("."):
        sentence += "."

    return sentence
