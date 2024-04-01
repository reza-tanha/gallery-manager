from django.urls import path
from gallery.users.apis.user_apis import (
    RegisterApi, UserProfileApi, UsersListApi
)


urlpatterns = [
    path('', UsersListApi.as_view(),name="users"),
    path("<int:user_id>/", UserProfileApi.as_view(), name="user-ditail"),
    path('register/', RegisterApi.as_view(),name="register"),
]
