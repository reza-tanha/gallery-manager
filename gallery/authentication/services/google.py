import requests
from django.conf import settings
from urllib.parse import urlencode
from gallery.users.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError



class GoogleOAuth:

    def __init__(self) -> None:
        self.GOOGLE_CLIENT_ID = getattr(settings, "GOOGLE_CLIENT_ID", "")
        self.GOOGLE_CLIENT_SECRET = getattr(settings, "GOOGLE_CLIENT_SECRET", "")
        self.GOOGLE_AUTH_URL = getattr(settings, "GOOGLE_AUTH_URL", "https://accounts.google.com/o/oauth2/auth")
        self.GOOGLE_TOKEN_URL = getattr(settings, "GOOGLE_TOKEN_URL", "https://accounts.google.com/o/oauth2/token")
        self.GOOGLE_USER_INFO_URL = getattr(settings, "GOOGLE_USER_INFO_URL", "https://www.googleapis.com/oauth2/v1/userinfo")
        self.GOOGLE_REDIRECT_URL = getattr(settings, "GOOGLE_REDIRECT_URL")

    def google_login(self):
        params = {
            "client_id": self.GOOGLE_CLIENT_ID,
            "redirect_uri": self.GOOGLE_REDIRECT_URL,
            "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
            "response_type": "code"
        }
        return f"{self.GOOGLE_AUTH_URL}?{urlencode(params)}" 

    def google_auth(self, code):
        data = {
            "code": code,
            "client_id": self.GOOGLE_CLIENT_ID,
            "client_secret": self.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.GOOGLE_REDIRECT_URL,
            "grant_type": "authorization_code"
        }
        try:
            token_response = requests.post(
                self.GOOGLE_TOKEN_URL,
                data=data
            ).json()
        except Exception as e:
            token_response = None
            error_message = f"Error occurred: {e}"
            raise Exception(error_message)
        return token_response

    def google_user_info(self, access_token):
        params = {
            "access_token": access_token['access_token']
        }
        try:
            info = requests.get(
                self.GOOGLE_USER_INFO_URL,
                params=params
            ).json()
        except Exception as e:            
            info = None
            error_message = f"Error occurred: {e}"
            raise Exception(error_message)
        return info

class GoogleUserService:

    @staticmethod
    def get_user(*, email: int)-> User:
        return get_user_model().objects.filter(email=email).first()

    @staticmethod
    def user_create(*, email: str, password:str, **kwargs) -> User:
        return get_user_model().objects.create_user(
            email=email, password=password, **kwargs
        )
    @staticmethod
    def get_token(*, user: User):
        
        if not user.is_active:
            raise ValidationError("user is not active")
        
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }