from django.contrib.gis.db import models

class Prop(models.Model):
    public_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    agent = models.CharField(max_length=255, null=True, blank=True)
    property_type = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    lot_size = models.FloatField(null=True, blank=True)
    construction_size = models.FloatField(null=True, blank=True)
    bathrooms = models.FloatField(null=True, blank=True)
    bedrooms = models.FloatField(null=True, blank=True)
    parking_spaces = models.IntegerField(null=True, blank=True)
    price_amount = models.FloatField(null=True, blank=True)
    price_currency = models.CharField(max_length=10, null=True, blank=True)
    operation_type = models.CharField(max_length=50, null=True, blank=True)
    title_image_full = models.URLField(null=True, blank=True)
    title_image_thumb = models.URLField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    location_point = models.PointField(null=True, blank=True, srid=4326)

    def __str__(self):
        return self.title
