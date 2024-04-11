from django.urls import path, include
from .apis.jwt_api import (_TokenObtainPairView, _TokenRefreshView, _TokenVerifyView)
from .apis.google_api import (GoogleAuth, GoogleAuthCallback)


urlpatterns = [
        path('jwt/', include(
            (
                [
                    path('login/',_TokenObtainPairView.as_view(), name="login"),
                    path('refresh/', _TokenRefreshView.as_view(),name="refresh"),
                    path('verify/', _TokenVerifyView.as_view(),name="verify"),
                ]
            )
            ),
            name="jwt"
        ),

        path('google/', include(
            (
                [
                    path("", GoogleAuth.as_view(), name="google-authoriztion"),
                    path("callback/", GoogleAuthCallback.as_view(), name='google-callback-authoriztion'),
                ]
            )
            ),
            name="google"
        )
]