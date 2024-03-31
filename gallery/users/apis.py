from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_validator, letter_validator
from gallery.users.models import User
from gallery.users.services import UserService
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from drf_spectacular.utils import extend_schema
from gallery.utils.pagination import LimitOffsetPagination


class RegisterApi(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(
                validators=[
                        number_validator,
                        letter_validator,
                        special_char_validator,
                        MinLengthValidator(limit_value=10)
                    ]
                )
        confirm_password = serializers.CharField(max_length=255)
        
        def validate_email(self, email):
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("email Already Taken")
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data
    class OutPutRegisterSerializer(serializers.ModelSerializer):

        # token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = User 
            fields = ("email", "created_at", "updated_at")

        # def get_token(self, user):
        #     data = dict()
        #     token_class = RefreshToken

        #     refresh = token_class.for_user(user)

        #     data["refresh"] = str(refresh)
        #     data["access"] = str(refresh.access_token)

        #     return data


    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
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
        return Response(self.OutPutRegisterSerializer(user, context={"request":request}).data)

class UserProfileApi(APIView):
    class OutputUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User 
            fields = ("first_name", "last_name", "email", "created_at", "updated_at")

    @extend_schema(responses=OutputUserSerializer)
    def get(self, request, user_id):
        try:
            user = UserService.get_user(user_id=user_id)
        except User.DoesNotExist as e:
            raise exceptions.NotFound(
                {"message": "user with provided user_id does not exists."}
            )
        serializer = self.OutputUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UsersApi(APIView, LimitOffsetPagination):
    class OutputUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User 
            fields = ("first_name", "last_name", "email", "created_at", "updated_at", "is_active")

    class UserFilterSerializer(serializers.Serializer):
        is_active = serializers.BooleanField(
            required=False, allow_null=True, default=None
        )

    @extend_schema(responses=OutputUserSerializer, parameters=[UserFilterSerializer])
    def get(self, request):
        filters_serializer = self.UserFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            query = UserService.user_list(filters=filters_serializer.validated_data)
        except User.DoesNotExist as e:
            raise exceptions.NotFound(
                {"message": "user with provided user_id does not exists."}
            )
        
        pagination = self.paginate_queryset(query, self.request)               
        serializer = self.OutputUserSerializer(pagination, many=True, context={"request":request})
        response = self.get_paginated_data(serializer.data)
        
        return Response(response, status=status.HTTP_200_OK)
        

