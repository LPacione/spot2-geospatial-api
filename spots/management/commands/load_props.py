import json
from django.core.management.base import BaseCommand
from spots.models.prop import Prop
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = "Loads properties from prop_list.json"

    def handle(self, *args, **options):
        with open("spots/props_list.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            operations = item.get("operations", [])
            op = operations[0] if operations else {}

            Prop.objects.update_or_create(
                public_id=item["public_id"],
                defaults={
                    "title": item.get("title"),
                    "agent": item.get("agent"),
                    "property_type": item.get("property_type"),
                    "location": item.get("location"),
                    "lot_size": item.get("lot_size"),
                    "construction_size": item.get("construction_size"),
                    "bathrooms": item.get("bathrooms"),
                    "bedrooms": item.get("bedrooms"),
                    "parking_spaces": item.get("parking_spaces"),
                    "price_amount": op.get("amount"),
                    "price_currency": op.get("currency"),
                    "operation_type": op.get("type"),
                    "title_image_full": item.get("title_image_full"),
                    "title_image_thumb": item.get("title_image_thumb"),
                    "updated_at": parse_datetime(item.get("updated_at")),
                },
            )

        self.stdout.write(self.style.SUCCESS("Properties loaded successfully"))
