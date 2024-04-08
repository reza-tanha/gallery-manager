import django_filters
from gallery.mediahub.models import Media
from django.contrib.postgres.fields import ArrayField



class MediaFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(method='filter_tags')
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
    
    def filter_tags(self, queryset, name, value):
        if isinstance(value, str):
            value = eval(value)
        return queryset.filter(tags__contains=value)