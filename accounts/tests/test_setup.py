from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from faker import Faker


class TestSetup(APITestCase):

    def setUp(self) -> None:
        self.fake = Faker()
        self.user = get_user_model()
        password = self.fake.email().split('@')[0]
        self.customer_payload = {
            "email": self.fake.email(),
            "password": password,
            "username": self.fake.simple_profile()['username'],
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "phone": "0746180701"
        }
        self.register_url = reverse("accounts:auth-list", args=())

        return super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
