import datetime

from oauth2_provider.models import AccessToken, Application
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from faker import Faker
from accounts.tests.test_setup import TestSetup


class TestSetup(APITestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        password = self.fake.email().split('@')[0]
        self.customer_payload = {
            "email": self.fake.email(),
            "password": password,
            "username": self.fake.simple_profile()['username'],
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "phone": "0790232329"
        }

        self.customer = get_user_model().objects.create(**self.customer_payload)
        self.customer_url = reverse("customers:customers-list")
        self.customer_detail_url = reverse("customers:customers-detail", args=[self.customer.id])

        self.application = Application.objects.create(
            name="test application",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_OPENID_HYBRID,
            user=self.customer,
            redirect_uris='http://127.0.0.1:8001/api/v1/auth/callback'
        )
        current_date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        self.token = AccessToken.objects.create(
            user=self.customer,
            application=self.application,
            token='beICluzhyzcQ5RLGUKLXFhuQBq75os',
            expires=current_date + datetime.timedelta(minutes=50),
            scope='openid read write'
        )
        self.AUTH_TOKEN = 'Bearer {}'.format(self.token.token)

        return super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
