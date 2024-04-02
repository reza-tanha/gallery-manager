import django_filters
from gallery.mediahub.models import Media
from django.contrib.postgres.fields import ArrayField



class MediaFilter(django_filters.FilterSet):
    class Meta:
        model = Media
        fields = ("id", 'name', 'description', 'tags', 'user')
        filter_overrides = {
            ArrayField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }