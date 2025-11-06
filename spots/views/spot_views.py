from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from ..models import Spot
from ..serializers.spot_serializers import SpotSerializer, AveragePriceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry

class SpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Spot.objects.all() 
    serializer_class = SpotSerializer
    
    lookup_field = 'spot_id'

    # Endpoint 2
    @action(detail=False, methods=['get'], url_path='nearby')
    def nearby(self, request):
        """
        Returns spots near a given lat/lng within a radius in meters.
        Query params: lat, lng, radius
        """
        try:
            lat = float(request.query_params.get('lat'))
            lng = float(request.query_params.get('lng'))
            radius = float(request.query_params.get('radius', 1000))  # default 1000 m
        except (TypeError, ValueError):
            return Response({"detail": "Parameters 'lat', 'lng', 'radius' must be numbers."},
                            status=status.HTTP_400_BAD_REQUEST)

        point = Point(lng, lat, srid=4326)  # lon, lat
        nearby_spots = Spot.objects.annotate(distance=Distance('location', point)) \
                                .filter(distance__lte=radius) \
                                .order_by('distance')
        
        serializer = self.get_serializer(nearby_spots, many=True)
        return Response(serializer.data)


    # Endpoint 3
    def get_queryset(self):
        """
        Override get_queryset to allow filtering by sector, type, and municipality using query parameters
        """
        queryset = super().get_queryset()
        query_params = self.request.query_params

        sector = query_params.get('sector')
        if sector:
            queryset = queryset.filter(sector_id=sector)

        spot_type = query_params.get('type')
        if spot_type:
            queryset = queryset.filter(type_id=spot_type)
        
        municipality = query_params.get('municipality')
        if municipality:
            queryset = queryset.filter(municipality__iexact=municipality)

        return queryset
    
    # Endpoint 4
    @action(detail=False, methods=['post'], url_path='within')
    def within(self, request):
        """
        Returns spots inside a polygon.
        Body: { "polygon": { "type": "Polygon", "coordinates": [...] } }
        """
        try:
            polygon_geojson = request.data.get('polygon')
            polygon = GEOSGeometry(str(polygon_geojson))
        except Exception:
            return Response({"detail": "Invalid polygon geometry."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        spots_within = Spot.objects.filter(location__within=polygon)
        serializer = self.get_serializer(spots_within, many=True)
        return Response(serializer.data)


    # Endpoint 5
    @action(detail=False, methods=['get'], url_path='average-price-by-sector')
    def average_price_by_sector(self, request):
        """
        Calculates the average rental price by sector.
        """
        average_prices = (
            Spot.objects
            .exclude(price_total_rent__isnull=True)
            .values('sector_id')
            .annotate(avg_price=Avg('price_total_rent'))
            .order_by('sector_id')
        )
        
        serializer = AveragePriceSerializer(average_prices, many=True)
        return Response(serializer.data)

    # # Endpoint 6
    def retrieve(self, request, spot_id=None):  # with lookup_field
        """
        Retrieve information related to the spot_id.
        Not necessary, but I choose define it.
        """
        spot = get_object_or_404(Spot, spot_id=spot_id)
        serializer = self.get_serializer(spot)
        return Response(serializer.data)

    # Endpoint 7
    @action(detail=False, methods=['get'], url_path='top-rent')
    def top_rent(self, request):
        """
        Returns the spots with the highest total rental price, limited by the 'limit' parameter'.
        """
        try:
            limit = int(request.query_params.get('limit', 10))
            if limit <= 0:
                raise ValueError
        except ValueError:
            return Response(
                {"detail": "Parameter 'limit' should be integer positive."},
                status=status.HTTP_400_BAD_REQUEST
            )

        top_spots = (
            Spot.objects
            .exclude(price_total_rent__isnull=True)
            .order_by('-price_total_rent')
            [:limit]
        )
        
        serializer = self.get_serializer(top_spots, many=True)
        return Response(serializer.data)