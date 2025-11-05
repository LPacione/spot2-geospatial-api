from rest_framework import viewsets, status
from ..models import Spot
from ..serializers.spot_serializers import SpotSerializer, AveragePriceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg

class SpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Spot.objects.all() 
    serializer_class = SpotSerializer

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

    # Endpoint 7
    @action(detail=False, methods=['get'], url_path='top-rent')
    def top_rent(self, request):
        """
        Returns the spots with the highest total rental price, limited by the 'limit' parameter'.
        """
        try:
            # Obtener el límite (default 10)
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