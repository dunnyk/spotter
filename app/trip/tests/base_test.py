from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse


class TestBaseCase(APITestCase):

    def setUp(self):
        self.create_trip_url = api_reverse("trip:trip-view")
