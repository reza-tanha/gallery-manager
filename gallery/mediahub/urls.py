from django.urls import path
from gallery.mediahub.apis.media_apis import (
    MediaApi, MediaDetailApi
)


urlpatterns = [
    path('', MediaApi.as_view(), name="medias"),
    path("<int:media_id>/", MediaDetailApi.as_view(), name="media-detail"),
]
