from django.contrib.gis.db import models

class Spot(models.Model):
    spot_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sector_id = models.IntegerField()
    type_id = models.IntegerField()
    settlement = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, null=True)
    corridor = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    area_sqm = models.FloatField(blank=True, null=True)
    price_sqm_rent = models.FloatField(blank=True, null=True)
    price_total_rent = models.FloatField(blank=True, null=True)
    price_sqm_sale = models.FloatField(blank=True, null=True)
    price_total_sale = models.FloatField(blank=True, null=True)
    maintenance_cost = models.FloatField(blank=True, null=True)
    modality = models.CharField(max_length=50, blank=True, null=True)

    location = models.PointField(geography=True, null=True, blank=True)

    user_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.municipality})"
