from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.spot_views import SpotViewSet
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'', SpotViewSet, basename='spot') 

def home(request):
    return HttpResponse("Bienvenido a Spot2 API. Usa /api/spots/ para ver los endpoints.")

urlpatterns = [
    path('spots/', include(router.urls)), 
    path('', home),
]