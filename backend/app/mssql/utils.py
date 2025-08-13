import os


def delete_file(path: str, prefix: str = "", suffix: str = ""):
    for filename in os.listdir(path):
        if filename.startswith(prefix) and filename.endswith(suffix):
            os.remove(os.path.join(path, filename))
