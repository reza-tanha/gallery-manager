from django.db import transaction 
from gallery.users.models import User
from gallery.mediahub.models import Media
from django.contrib.auth import get_user_model
from gallery.common.services import model_update
from gallery.mediahub.filters import MediaFilter
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from django.conf import settings




class MediaService:

    @staticmethod
    def get_media(*, media_id: int)-> User:
        return Media.objects.get(pk=media_id)
    
    @staticmethod
    def media_create(*, user_id, **kwargs) -> Media:      
        media = Media.objects.create(
            user_id=user_id,
            **kwargs
        )
        return media

    @transaction.atomic
    @staticmethod
    def media_update(*, media:Media, data):
        non_side_effect_fields = ["name", "description", "file", "tags"]
        media, has_update = model_update(
            instance=media, 
            fields=non_side_effect_fields,
            data=data
        )            
        return media

    @staticmethod
    def file_write_disk(*, file, media_root_tmp="media"):
        storage = FileSystemStorage(location=media_root_tmp)
        file.name = storage.get_available_name(file)
        storage.save(file.name, File(file))
        file_path = os.path.join(media_root_tmp, file.name)
        file = {
            "file_path":file_path,
            "name":file.name
        }
        return file

    @staticmethod
    def media_list(*, filters=None):
        filters = filters or {}
        qs = Media.objects.all()
        return MediaFilter(filters, qs).qs
    
    