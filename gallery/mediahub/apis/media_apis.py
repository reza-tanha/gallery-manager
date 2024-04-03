from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from gallery.utils.pagination import LimitOffsetPagination
from gallery.mediahub.tasks import media_file_upload
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request


from gallery.mediahub.serializers.media_serializers import (
    InputMediaSerializer,
    OutputMediaSerializer,
    MediaFilterSerializer
)

from gallery.mediahub.services.media_services import (
    MediaService,
    Media
)

    
class MediaApi(APIView, LimitOffsetPagination):

    @extend_schema(request=InputMediaSerializer)
    def post(self, request: Request, *args, **kwargs):
        serializer = InputMediaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = request.FILES.get("file")
        request.data.pop("file")
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

        if file:
            file_data = MediaService.file_write_disk(file=file, media_root_tmp=settings.MEDIA_ROOT_TMP)
            media_file_upload.apply_async(
                args=[
                    media.id,
                    file_data
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
        
class MediaDetailApi(APIView):

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

    def put(self, request: Request, media_id: int):
        ...

    def delete(self, request: Request, media_id: int):
        ...

# class MyMediaApi(APIView):

#     @extend_schema(responses=OutputMediaSerializer)
#     def get(self, request, *args, **kwargs):
#         ...

# class RegisterApi(APIView):
#     @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
#     def post(self, request):
#         serializer = InputRegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             user = UserService.user_create(
#                 email=serializer.validated_data.get("email"),
#                 password=serializer.validated_data.get("password")
#                 )
#         except Exception as ex:
#             return Response(
#                     f"Database Error {ex}",
#                     status=status.HTTP_400_BAD_REQUEST
#                     )
#         return Response(OutPutRegisterSerializer(user, context={"request":request}).data)

# class UserProfileApi(APIView):
    
    # @extend_schema(responses=OutputUserSerializer)
    # def get(self, request, user_id):
    #     try:
    #         user = UserService.get_user(user_id=user_id)
    #     except User.DoesNotExist as e:
    #         raise exceptions.NotFound(
    #             {"message": "user with provided user_id does not exists."}
    #         )
    #     serializer = OutputUserSerializer(user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

# class UsersListApi(APIView, LimitOffsetPagination):
    
#     @extend_schema(responses=OutputUserSerializer, parameters=[UserFilterSerializer])
#     def get(self, request):
#         filters_serializer = UserFilterSerializer(data=request.query_params)
#         filters_serializer.is_valid(raise_exception=True)

#         try:
#             query = UserService.user_list(filters=filters_serializer.validated_data)
#         except User.DoesNotExist as e:
            # raise exceptions.NotFound(
            #     {"message": "user with provided user_id does not exists."}
            # )
        
#         pagination = self.paginate_queryset(query, self.request)               
#         serializer = OutputUserSerializer(pagination, many=True, context={"request":request})
#         response = self.get_paginated_data(serializer.data)
        
#         return Response(response, status=status.HTTP_200_OK)
        

