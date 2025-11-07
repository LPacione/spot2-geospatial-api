from rest_framework import viewsets
from ..models.prop import Prop
from ..serializers.prop_serializers import PropSerializer

class PropViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoints
    """
    queryset = Prop.objects.all().order_by('public_id')
    serializer_class = PropSerializer
    lookup_field = "public_id"
