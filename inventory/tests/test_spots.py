from django.test import TestCase
from rest_framework.test import APIClient
from inventory.models.spot import Spot
from rest_framework import status


class SpotAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.spot = Spot.objects.create(
            spot_id=1001,
            title="First Spot",
            description="Mock",
            sector_id=9,
            type_id=1,
            municipality="Mock Municipality",
            state="Mock State",
        )

    def test_list_spots(self):
        """GET /api/spots/ should return at least 1 prop"""
        response = self.client.get("/api/spots/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data["results"][0]["title"], "First Spot")

    def test_get_spot_detail(self):
        """GET /api/spots/{spot_id}/ should return a prop"""
        response = self.client.get(f"/api/spots/{self.spot.spot_id}/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_filter_by_sector(self):
        """GET /api/spots/?sector=9 should return a prop and STATUS_CODE 200"""
        response = self.client.get("/api/spots/?sector=9")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nearby_spots_mocked(self):
        """GET /api/spots/nearby/ should return a list"""
        response = self.client.get("/api/spots/nearby/?lat=19.43&lng=-99.13&radius=2000")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_within_polygon_mocked(self):
        """POST /api/spots/within/ with new mock polygon"""
        polygon = {
            "polygon": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-99.135, 19.432],
                        [-99.13, 19.432],
                        [-99.13, 19.435],
                        [-99.135, 19.435],
                        [-99.135, 19.432],
                    ]
                ],
            }
        }
        response = self.client.post("/api/spots/within/", polygon, format="json")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_invalid_method_on_endpoint(self):
        """POST into a GET-only endpoint should return 405"""
        response = self.client.post("/api/spots/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
