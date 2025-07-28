import re
import uuid


def generate_uuid(id: str) -> str:
    """
    Generate a deterministic UUID based on a given string.
    The same input string will always produce the same UUID.
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, id))


def extract_file_info(filename: str) -> tuple[str, str, str] | None:
    # Regex to capture: collection_name, id, date (YYYYMMDD), time (HHMMSS)
    pattern = r"^([a-zA-Z0-9]+)_(\d+)_(\d{8})_(\d{6})"
    match = re.match(pattern, filename)
    if match:
        collection_name, id_, date, time = match.groups()
        return f"{collection_name}_{id_}", date, time
    return None
