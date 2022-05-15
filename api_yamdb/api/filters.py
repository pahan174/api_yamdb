from django_filters import CharFilter, FilterSet, NumberFilter
from reviews.models import Title


class TitlesFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='contains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='contains')
    name = CharFilter(lookup_expr='contains')
    year = NumberFilter(lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
