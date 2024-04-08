from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from gallery.utils.pagination import LimitOffsetPagination
from gallery.mediahub.tasks import media_file_upload
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from gallery.api.mixins import ApiAuthMixin
from config.settings.file_upload import FilePathTmp
from django.test import override_settings
from gallery.mediahub.serializers.media_serializers import (
    InputMediaSerializer,
    OutputMediaSerializer,
    MediaFilterSerializer
)
from gallery.mediahub.services.media_services import (
    MediaService,
    Media
)   
@extend_schema(tags=['media'])
class MediaApi(ApiAuthMixin, APIView, LimitOffsetPagination):

    @override_settings(FILE_UPLOAD_HANDLERS=[
        # "django.core.files.uploadhandler.MemoryFileUploadHandler",
        'config.settings.file_upload.MyCustomUploadHandler'
    ])
    @extend_schema(request=InputMediaSerializer)
    def post(self, request: Request, *args, **kwargs):
        field_name = "file"
        serializer = InputMediaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tmp_file_path = FilePathTmp(request, field_name).main()
        if field_name in request.data:
            request.data.pop(field_name)
        data_to_send = {key: value for key, value in serializer.validated_data.items() if key in request.data and value is not None}

        try:
            media = MediaService.media_create(
                user_id=request.user.id,
                **data_to_send
            )
        except Exception as e:
            raise exceptions.ValidationError(
                {"message": f"{e}"}
            )
        if tmp_file_path:
            media_file_upload.apply_async(
                args=[
                    media.id,
                    tmp_file_path
                ]
            )
        return Response(OutputMediaSerializer(media, ).data, status=status.HTTP_201_CREATED)
    
    @extend_schema(responses=OutputMediaSerializer, parameters=[MediaFilterSerializer])
    def get(self, request: Request, *args, **kwargs):

        filters_serializer = MediaFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            query = MediaService.media_list(filters=filters_serializer.validated_data)
        except Media.DoesNotExist as e:
            raise exceptions.ValidationError(
                {"message": f"{e}"}
            )
        pagination = self.paginate_queryset(query, self.request)               
        serializer = OutputMediaSerializer(pagination, many=True, context={"request":request})
        response = self.get_paginated_data(serializer.data)
        return Response(response, status=status.HTTP_200_OK)
        
@extend_schema(tags=['media'])
class MediaDetailApi(ApiAuthMixin, APIView):
    
    @extend_schema(responses=OutputMediaSerializer)
    def get(self, request: Request, media_id: int):
        try:
            media = MediaService.get_media(media_id=media_id)
        except Media.DoesNotExist as e:
            raise exceptions.NotFound(
                {"message": "media with provided media_id does not exists."}
            )
        serializer = OutputMediaSerializer(media)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @override_settings(FILE_UPLOAD_HANDLERS=[
        # "django.core.files.uploadhandler.MemoryFileUploadHandler",
        'config.settings.file_upload.MyCustomUploadHandler'
    ])
    @extend_schema(request=InputMediaSerializer)
    def put(self, request: Request, media_id: int):
        field_name = "file"

        serializer = InputMediaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tmp_file_path = FilePathTmp(request, field_name).main()
        if field_name in request.data:
            request.data.pop(field_name)

        try:
            media = MediaService.get_media(media_id=media_id, user=request.user)
        except Media.DoesNotExist as e:
            raise exceptions.NotFound(
                {"message": "media with provided media_id does not exists."}
            )
        data_to_send = {key: value for key, value in serializer.validated_data.items() if key in request.data and value is not None}
        try:
            media = MediaService.media_update(
                media=media,
                data=data_to_send
            )
        except Exception as e:
            raise exceptions.ValidationError(
                {"message": f"{e}"}
            )

        if tmp_file_path:
            media_file_upload.apply_async(
                args=[media.id, tmp_file_path]
            )

        return Response(OutputMediaSerializer(media).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, media_id: int):
        try:
            media = MediaService.get_media(media_id=media_id, user=request.user)
        except Media.DoesNotExist as e:
            raise exceptions.NotFound(
                {"message": "media with provided media_id does not exists."}
            )
        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

