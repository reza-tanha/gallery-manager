import django_filters

from django.contrib.auth import get_user_model


BaseUser = get_user_model()

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = BaseUser
        fields = ("id", "email", "is_active", 'first_name')
