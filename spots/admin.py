from django.contrib import admin
from .models.spot import Spot

@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("title", "municipality", "state", "price_total_rent")
    search_fields = ("title", "municipality", "state")
