from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from gallery.users.models import User
from gallery.users.services.user_services import UserService
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from drf_spectacular.utils import extend_schema
from gallery.utils.pagination import LimitOffsetPagination

from gallery.users.serializers.user_serializers import (
    InputRegisterSerializer, 
    OutPutRegisterSerializer,
    OutputUserSerializer,
    UserFilterSerializer
)

from gallery.users.services.user_services import (
    UserService,
)


@extend_schema(tags=['users'])
class RegisterApi(APIView):
    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = UserService.user_create(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password")
                )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(OutPutRegisterSerializer(user, context={"request":request}).data)

@extend_schema(tags=['users'])
class UserProfileApi(APIView):
    
    @extend_schema(responses=OutputUserSerializer)
    def get(self, request, user_id):
        try:
            user = UserService.get_user(user_id=user_id)
        except User.DoesNotExist as e:
            raise exceptions.NotFound(
                {"message": "user with provided user_id does not exists."}
            )
        serializer = OutputUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['users'])
class UsersListApi(APIView, LimitOffsetPagination):
    
    @extend_schema(responses=OutputUserSerializer, parameters=[UserFilterSerializer])
    def get(self, request):
        filters_serializer = UserFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            query = UserService.user_list(filters=filters_serializer.validated_data)
        except User.DoesNotExist as e:
            raise exceptions.NotFound(
                {"message": "user with provided user_id does not exists."}
            )
        
        pagination = self.paginate_queryset(query, self.request)               
        serializer = OutputUserSerializer(pagination, many=True, context={"request":request})
        response = self.get_paginated_data(serializer.data)
        
        return Response(response, status=status.HTTP_200_OK)
        

