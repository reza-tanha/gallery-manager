from celery import shared_task
from celery.utils.log import get_task_logger
from gallery.mediahub.models import Media
logger = get_task_logger(__name__)
from gallery.mediahub.services.media_services import MediaService
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.core.files import File


def upload_file(instance: Media=None, file=None):
    ...

@shared_task(bind=True, )
def media_file_upload(self, media_id, file: dict):
    from gallery.mediahub.services.media_services import MediaService

    media = MediaService.get_media(media_id=media_id)
    
    storage = FileSystemStorage()

    file_path_object = Path(file["file_path"])
    with file_path_object.open(mode="rb") as file:
        logger.info(f"Uploading file: {file.name} ....")
        image_file = File(file, name=f"{file.name}")
        media.file=image_file
        media.save(update_fields=["file"])


    # storage.delete(file["name"])
    # ...
    # try:
    #     MediaService.media_update(media=media, data={"file": file})
    # except Exception as exc:
    #     logger.warning(f"Exception occurred while uploading file: {exc}")
    #     self.retry(exc=exc, countdown=5)



