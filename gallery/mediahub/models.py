from django.db import models
from gallery.common.models import BaseModel
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from gallery.utils.models_path_aws import path_media_file


class Media(BaseModel):

    name = models.CharField(max_length=50)

    description = models.TextField()

    file = models.FileField(upload_to=path_media_file)

    tags = ArrayField(base_field=models.CharField(max_length=30))

    user = models.ForeignKey(
        to=get_user_model(), 
        on_delete=models.SET_NULL,
        related_name="medias",
        null=True, blank=True
    )

    def __str__(self) -> str:
        return  f"{self.name}"