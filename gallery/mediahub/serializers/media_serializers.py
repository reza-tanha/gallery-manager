from rest_framework import serializers
from gallery.mediahub.models import Media


from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
User = get_user_model()
from gallery.users.validators import number_validator, special_char_validator, letter_validator


class InputMediaSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=None, default=None, allow_null=False)
    # file = serializers.FileField(required=None, default=None, allow_null=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    files = serializers.ListField(child=serializers.FileField(), required=None, default=None, allow_null=False)
class MediaFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, default=None, allow_null=False)
    description = serializers.CharField(required=None, default=None, allow_null=False)
    tags = serializers.ListField(required=False, allow_empty=True)
    user = serializers.IntegerField(required=False,  default=None)

class OutputMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
