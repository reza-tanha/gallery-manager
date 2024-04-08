from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile
import os
import tempfile
from django.conf import settings
from rest_framework.request import Request


class MY_TemporaryUploadedFile(UploadedFile):
    def __init__(self, name, content_type, size, charset, content_type_extra=None):
        _, ext = os.path.splitext(name)
        file = tempfile.NamedTemporaryFile(
            suffix=".upload" + ext, dir=settings.FILE_UPLOAD_TEMP_DIR
        )
        super().__init__(file, name, content_type, size, charset, content_type_extra)

    def temporary_file_path(self):
        return self.file.name

    def close(self):
       pass

class MyCustomUploadHandler(FileUploadHandler):
    def new_file(self, *args, **kwargs):
        super().new_file(*args, **kwargs)
        self.file = MY_TemporaryUploadedFile(
            self.file_name, self.content_type, 0, self.charset, self.content_type_extra
        )

    def receive_data_chunk(self, raw_data, start):
        self.file.write(raw_data)

    def file_complete(self, file_size):
        self.file.seek(0)
        self.file.size = file_size
        return self.file

    def upload_interrupted(self):
        pass


class FilePathTmp:

    def __init__(self, request: Request, field_name: str = "files") -> None:
        self.request = request
        self.field_name = field_name
        self.fields_data = []

    def get_files(self) -> UploadedFile:
        return self.request.FILES.getlist(self.field_name, None)
        
    def main(self):
        if files := self.get_files():
            for _field in files:
                self.fields_data.append(
                    _field.temporary_file_path()
                )
            return self.fields_data
        return None