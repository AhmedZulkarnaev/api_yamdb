from django_filters import rest_framework as fil

from reviews.models import Title


class TitleFilter(fil.FilterSet):
    name = fil.CharFilter(field_name='name', lookup_expr='contains')
    genre = fil.CharFilter(field_name='genre__slug', lookup_expr='exact')
    category = fil.CharFilter(
        field_name='category__slug', lookup_expr='exact'
    )
    year = fil.NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year', )
