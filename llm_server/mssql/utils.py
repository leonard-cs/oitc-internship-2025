import os
from datetime import datetime

TIME = datetime.now().strftime("%Y%m%d_%H%M%S")

def delete_file(path: str, prefix: str = "", sufix: str = ""):
    for filename in os.listdir(path):
        if filename.startswith(prefix) and filename.endswith(sufix):
            os.remove(os.path.join(path, filename))