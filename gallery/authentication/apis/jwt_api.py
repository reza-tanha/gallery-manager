from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["auth"])
class _TokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=["auth"])
class _TokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=["auth"])
class _TokenVerifyView(TokenVerifyView):
    pass
