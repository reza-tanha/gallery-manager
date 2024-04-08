from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.utils import extend_schema

#just for test push
@extend_schema(tags=["auth"])
class _TokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=["auth"])
class _TokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=["auth"])
class _TokenVerifyView(TokenVerifyView):
    pass

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
]