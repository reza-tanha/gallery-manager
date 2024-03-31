from django.urls import path
from .apis import (
    RegisterApi, UserProfileApi, UsersApi
)


urlpatterns = [
    path('', UsersApi.as_view(),name="users"),
    path("<int:user_id>/", UserProfileApi.as_view(), name="user-ditail"),
    path('register/', RegisterApi.as_view(),name="register"),
]
