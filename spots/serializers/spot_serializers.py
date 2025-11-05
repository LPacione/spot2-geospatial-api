from rest_framework import serializers
from ..models import Spot


class SpotSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()

    class Meta:
        model = Spot
        fields = (
            "spot_id",
            "title",
            "description",
            "sector_id",
            "type_id",
            "settlement",
            "municipality",
            "state",
            "region",
            "corridor",
            "address",
            "area_sqm",
            "price_sqm_rent",
            "price_total_rent",
            "price_sqm_sale",
            "price_total_sale",
            "maintenance_cost",
            "modality",
            "user_id",
            "created_date",
            "geometry",
        )

    def get_geometry(self, obj):
        if obj.location:
            return {
                "type": "Point",
                "coordinates": [obj.location.x, obj.location.y],
            }
        return None

class AveragePriceSerializer(serializers.Serializer):
    sector_id = serializers.IntegerField() 
    avg_price = serializers.DecimalField(max_digits=15, decimal_places=2)