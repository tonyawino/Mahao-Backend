# TODO: Uncomment to actually upload files
# As per instructions on https://medium.com/@abdelhedihlel/upload-files-to-firebase-storage-using-python-782213060064
import uuid

from fastapi import File
from firebase_admin import credentials, initialize_app, storage
import shutil, os
from pathlib import Path

# Init firebase with your credentials
cred = credentials.Certificate("./mahao-firebase-credentials.json")
initialize_app(cred, {'storageBucket': 'mahao-1da7e.appspot.com'})

def upload_file(file: File, id: int, table: str) -> str:
    bucket = storage.bucket(table)
    if not bucket.exists():
        bucket.create()

    fp: Path = Path(f"./uploads/{table}/")
    if not fp.exists():
        os.makedirs(fp)

    file_parts = file.filename.split(".")
    if len(file_parts) > 1:
        file_extension = file_parts[len(file_parts)-1]
        filename = f"{str(uuid.uuid4())}.{file_extension}"
    else:
        filename = file.filename
    fp = fp.joinpath(f"{filename}")
    blob = bucket.blob(f"{filename}")

    print(f"File path is {fp}")
    try:
        with fp.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    res = blob.upload_from_filename(fp)

    # Opt : if you want to make public access from the URL
    blob.make_public()

    # Delete local file after saving in the cloud
    os.remove(fp)

    return blob.public_url
