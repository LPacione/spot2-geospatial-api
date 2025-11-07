from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.spot_views import SpotViewSet
from .views.prop_views import PropViewSet
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'spots', SpotViewSet, basename='spot')
router.register(r'props', PropViewSet, basename='prop')

def home(request):
    return HttpResponse("Welcome to Spot2 API.")

urlpatterns = [
    path('', home),
    path('', include(router.urls)),
]