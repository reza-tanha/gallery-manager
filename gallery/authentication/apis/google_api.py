from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpResponseRedirect
from ..services.google import GoogleOAuth
from gallery.authentication.services.google import GoogleUserService
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from drf_spectacular.utils import extend_schema
from gallery.utils.utils import generate_password


@extend_schema(tags=["auth"])
class GoogleAuth(APIView):

    def get(self, request):
        google_login = GoogleOAuth().google_login()
        return HttpResponseRedirect(redirect_to=google_login)
    
@extend_schema(tags=["auth"])
class GoogleAuthCallback(APIView):

    class OutputGoogleCallbackSerializer(serializers.Serializer):
        refresh = serializers.CharField()
        access = serializers.CharField()

    @extend_schema(responses=OutputGoogleCallbackSerializer)
    def get(self, request: Request):
        if code := request.query_params.get("code", None):

            access_token_data = GoogleOAuth().google_auth(code)
            
            info = GoogleOAuth().google_user_info(access_token_data)
            
            user = GoogleUserService.get_user(
                email=info['email']
            )

            if not user:
                user = GoogleUserService.user_create(
                    email=info['email'],
                    password=generate_password(15)
                )

            serializers_data = self.OutputGoogleCallbackSerializer(data=GoogleUserService.get_token(user=user))
            serializers_data.is_valid(raise_exception=True)
            
            return Response(serializers_data.data, status=HTTP_200_OK)
            
        return Response(
            {
                "message": "Authentication Is Faield ."
            },
            status=HTTP_400_BAD_REQUEST
        )

