import os

from django.db import models
from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()

class Upload():

    @staticmethod
    def upload_file(file, filename):
        try:
            target_path = os.path.join('reports/', filename)
            path = storage.save(target_path, file)
            return storage.url(path)
        except Exception as e:
            print(f"Failed to upload!\n{e}")
        