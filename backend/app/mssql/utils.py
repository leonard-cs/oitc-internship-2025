import os
import re


def delete_file(path: str, prefix: str = "", suffix: str = ""):
    for filename in os.listdir(path):
        if filename.startswith(prefix) and filename.endswith(suffix):
            os.remove(os.path.join(path, filename))


def remove_sample_rows(table_info: str) -> str:
    """Remove sample rows from the table info. Returns the table info without the sample rows."""
    table_info = table_info.split("/*")[0]
    return table_info


def extract_sql_results(result_string: str) -> list[str]:
    """
    Extracts all SQL result strings from a given string.
    """
    return re.findall(r"\{.*?\}", result_string)
