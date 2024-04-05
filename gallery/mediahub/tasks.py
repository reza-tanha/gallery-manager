from celery import shared_task
from celery.utils.log import get_task_logger
from gallery.mediahub.models import Media
logger = get_task_logger(__name__)
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os



@shared_task(bind=True, )
def media_file_upload(self, media_id, file_path: list[str]):
    from gallery.mediahub.services.media_services import MediaService
    media = MediaService.get_media(media_id=media_id)
    # for path in file_path: # if multi path in list [0,1,2,3,5]
    #     path

    file_path_object = Path(file_path[0])
    with file_path_object.open(mode="rb") as file:
        logger.info(f"Uploading file: {file.name} ....")
        image_file = File(file, name=f"{file.name}")
        media.file=image_file
        media.save(update_fields=["file"])
    try:
        os.remove(file_path[0])
    except:
        pass
    return "Uploading File Success."
