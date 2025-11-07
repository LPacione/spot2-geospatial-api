import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from pathlib import Path
from inventory.models.prop import Prop


class Command(BaseCommand):
    help = "Load props_list.json into database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Path to props_list.json file',
            default=str(Path(__file__).resolve().parent.parent.parent / 'props_list.json')
        )

    def handle(self, *args, **options):
        path = options['path']

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        created, skipped = 0, 0

        for item in data:
            try:
                operations = item.get("operations", [])
                op = operations[0] if operations else {}

                Prop.objects.create(
                    public_id=item["public_id"],
                    title=item.get("title"),
                    agent=item.get("agent"),
                    property_type=item.get("property_type"),
                    location=item.get("location"),
                    lot_size=item.get("lot_size"),
                    construction_size=item.get("construction_size"),
                    bathrooms=item.get("bathrooms"),
                    bedrooms=item.get("bedrooms"),
                    parking_spaces=item.get("parking_spaces"),
                    price_amount=op.get("amount"),
                    price_currency=op.get("currency"),
                    operation_type=op.get("type"),
                    title_image_full=item.get("title_image_full"),
                    title_image_thumb=item.get("title_image_thumb"),
                    updated_at=parse_datetime(item.get("updated_at")),
                )
                created += 1

            except Exception as e:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"Omitted item {item.get('public_id', 'unknown')}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Load completed: {created} rows created/updated, {skipped} omitted"))
