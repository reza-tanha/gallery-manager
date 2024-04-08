from django.utils import timezone


def path_media_file(instance , filename):
    user_id = str(instance.id) if instance else "anonymus"
    time_now = timezone.now().date()
    return f"mediahub/media/{time_now}/u_{user_id}/{filename}"

