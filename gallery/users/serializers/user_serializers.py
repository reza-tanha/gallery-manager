from gallery.users.validators import number_validator, special_char_validator, letter_validator
from rest_framework import serializers
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
User = get_user_model()


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

    def validate(self, data: dict):
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

class OutputUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ("first_name", "last_name", "email", "created_at", "updated_at", "is_active")

class UserFilterSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(
        required=False, allow_null=True, default=None
    )
