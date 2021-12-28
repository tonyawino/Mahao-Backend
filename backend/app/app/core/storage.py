# TODO: Uncomment to actually upload files
# As per instructions on https://medium.com/@abdelhedihlel/upload-files-to-firebase-storage-using-python-782213060064
from fastapi import File
#from firebase_admin import credentials, initialize_app, storage
# Init firebase with your credentials
#cred = credentials.Certificate("../../../mahao-firebase-credentials.json")
#initialize_app(cred, {'storageBucket': 'mahao-1da7e.appspot.com'})


def upload_file(file: File, id: int, table: str) -> str:
    #bucket = storage.bucket(table)
    #blob = bucket.blob(id)
    #blob.upload_from_file(file)

    # Opt : if you want to make public access from the URL
    #blob.make_public()

    #return blob.public_url
    return f"https://www.google.com/search?q={table}{id}"
