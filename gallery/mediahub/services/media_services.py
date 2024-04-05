from django.db import transaction 
from django.db.models import QuerySet
from gallery.mediahub.models import Media
from gallery.common.services import model_update
from gallery.mediahub.filters import MediaFilter
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.core.files import File
        # return get_object_or_404(Media, pk=media_id, **kwargs)
import os#

class MediaService:

    @staticmethod
    def get_media(*, media_id: int, **kwargs)-> Media:
        return Media.objects.get(pk=media_id, **kwargs)
    
    @staticmethod
    def media_create(*, user_id, **kwargs) -> Media:      
        media = Media.objects.create(
            user_id=user_id,
            **kwargs
        )
        return media

    @transaction.atomic
    @staticmethod
    def media_update(*, media:Media, data) -> Media:
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
    def media_list(*, filters=None) -> QuerySet[Media]:
        filters = filters or {}
        qs = Media.objects.all()
        return MediaFilter(filters, qs).qs
    
    