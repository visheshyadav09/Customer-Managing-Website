import django_filters
from django_filters import DateFilter,CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date=DateFilter(field_name="date_created",lookup_expr='gte')
    end_date=DateFilter(field_name="date_created",lookup_expr='lte')
    note=CharFilter(field_name='note',lookup_expr='icontains')
    class Meta:
        model=Order
        fields='__all__'
        exclude=['customer','date_created']

# the exclude field lets us exclude the fields in the form which we dont want
# lte-less than or equal to
#gte- greater than or equal to