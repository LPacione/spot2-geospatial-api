import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from inventory.models.spot import Spot
from datetime import datetime
from pathlib import Path
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "Load LK_SPOTS.csv into database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Path file',
            default=str(Path(__file__).resolve().parent.parent.parent/'LK_SPOTS.csv')
        )

    def handle(self, *args, **options):
        path = options['path']

        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            created, skipped = 0, 0

            for row in reader:
                try:
                    title = row.get('spot_settlement') or 'No name'
                    lat = float(row.get('spot_latitude', 0))
                    lon = float(row.get('spot_longitude', 0))
                    location = Point(lon, lat) if lat and lon else None
                    aware_date = make_aware(datetime.strptime(row.get('spot_created_date'), '%Y-%m-%d'))
    
                    Spot.objects.create(
                        spot_id=row.get('spot_id'),
                        title=title,
                        sector_id=row.get('spot_sector_id') or None,
                        type_id=row.get('spot_type_id') or None,
                        settlement=row.get('spot_settlement'),
                        municipality=row.get('spot_municipality'),
                        state=row.get('spot_state'),
                        region=row.get('spot_region'),
                        corridor=row.get('spot_corridor'),
                        area_sqm=row.get('spot_area_in_sqm') or None,
                        price_sqm_rent=row.get('spot_price_sqm_mxn_rent') or None,
                        price_total_rent=row.get('spot_price_total_mxn_rent') or None,
                        price_sqm_sale=row.get('spot_price_sqm_mxn_sale') or None,
                        price_total_sale=row.get('spot_price_total_mxn_sale') or None,
                        modality=row.get('spot_modality'),
                        user_id=row.get('uuiid') or None,
                        created_date=aware_date,
                        location=location,
                    )
                    created += 1

                except Exception as e:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f"Omitted row: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Load completed: {created} rows created, {skipped} omitted"))
