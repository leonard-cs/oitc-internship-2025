import os


def delete_file(path: str, prefix: str = "", sufix: str = ""):
    for filename in os.listdir(path):
        if filename.startswith(prefix) and filename.endswith(sufix):
            os.remove(os.path.join(path, filename))
