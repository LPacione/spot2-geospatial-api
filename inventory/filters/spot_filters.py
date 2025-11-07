from django_filters import FilterSet, NumberFilter, CharFilter
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point 
from ..models import Spot

class SpotFilter(FilterSet):
    sector_id = NumberFilter(field_name='sector_id')
    modality = CharFilter(field_name='modality')
    
    lng = NumberFilter(method='filter_by_distance')
    lat = NumberFilter(method='filter_by_distance')
    dist = NumberFilter(method='filter_by_distance')

    class Meta:
        model = Spot
        fields = ['sector_id', 'modality']
        
    def filter_by_distance(self, queryset, name, value):
        lng = self.data.get('lng')
        lat = self.data.get('lat')
        dist_km = self.data.get('dist')

        if lng is None or lat is None or dist_km is None:
            return queryset

        try:
            lng = float(lng)
            lat = float(lat)
            dist_km = float(dist_km)

            if dist_km <= 0 or not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                return queryset
            
            ref_point = Point(float(lng), float(lat), srid=4326)
            return queryset.filter(location__distance_lte=(ref_point, D(km=dist_km)))
            
        except (ValueError, TypeError):
            return queryset