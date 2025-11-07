from rest_framework import serializers
from ..models.prop import Prop

class PropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prop
        fields = [
            "public_id",
            "title",
            "agent",
            "property_type",
            "location",
            "lot_size",
            "construction_size",
            "bathrooms",
            "bedrooms",
            "parking_spaces",
            "price_amount",
            "price_currency",
            "operation_type",
            "title_image_full",
            "title_image_thumb",
            "updated_at",
        ]
