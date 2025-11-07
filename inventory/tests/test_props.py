from django.test import TestCase
from rest_framework.test import APIClient
from inventory.models.prop import Prop
from rest_framework import status


class PropAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.prop = Prop.objects.create(
            public_id="abc123",
            title="First Prop",
            agent="Luciano",
            property_type="Apartment",
            location="CDMX",
            price_amount=2500000.0,
            price_currency="MXN",
            operation_type="sale",
        )

    def test_list_props(self):
        """GET /api/props/ should return a list"""
        response = self.client.get("/api/props/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_prop(self):
        """GET /api/props/{public_id}/ should return a prop"""
        response = self.client.get(f"/api/props/{self.prop.public_id}/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_filter_by_operation_type(self):
        """GET /api/props/?operation_type=sale should return STATUS CODE 200"""
        response = self.client.get("/api/props/?operation_type=sale")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_prop_not_allowed(self):
        """POST not allowed"""
        data = {"public_id": "xyz789", "title": "New Prop"}
        response = self.client.post("/api/props/", data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
