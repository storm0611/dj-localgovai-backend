import shutil
import zipfile
import os
import io
from datetime import datetime
from backend.settings import (
    TMP_DIR
)

def zip_folder(folder_path, output_path=None):
    if not output_path:
        output_path = os.path.join(TMP_DIR, str(int(datetime.now().timestamp())))
    shutil.make_archive(output_path, 'zip', folder_path)
    return output_path + ".zip"

def zip_file(file_path, output_path=None):
    if not output_path:
        output_path = os.path.join(TMP_DIR, str(int(datetime.now().timestamp())) + ".zip")
    with zipfile.ZipFile(output_path, 'w') as zip_file:
        zip_file.write(file_path)
    return output_path

def del_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
