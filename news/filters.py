from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='post_time',
        lookup_expr='gte',
        widget=DateTimeInput(
            format='%y-%m-%dT',
            attrs={'type': 'datetime-local'},
        ))


    class Meta:
        model = Post
        fields = {'title': ['icontains'],
                  'category__category': ['icontains'],
                  }
