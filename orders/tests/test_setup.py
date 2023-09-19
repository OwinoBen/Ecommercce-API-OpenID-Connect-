import datetime

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from oauth2_provider.models import AccessToken, Application
from django.urls import reverse

from faker import Faker

from product.models import Product
from orders.models import Orders


class TestSetup(APITestCase):

    def setUp(self) -> None:
        self.order_url = reverse("orders:orders-list", args=())
        self.fake = Faker()

        self.product_payload = {
            "product_title": self.fake.name,
            "product_sku": f"SKU{self.fake.random_int(0, 10000)}",
            "product_qty": self.fake.random_digit(),
            "selling_price": self.fake.random_int(0, 100000),
            "discount_price": self.fake.random_int(0, 100000),
            "is_verified": True
        }
        password = self.fake.email().split('@')[0]
        self.customer_payload = {
            "email": self.fake.email(),
            "password": password,
            "username": self.fake.simple_profile()['username'],
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "phone": "0790232329"
        }

        self.product = Product.objects.create(**self.product_payload)
        self.customer = get_user_model().objects.create(**self.customer_payload)
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
        Orders.objects.create(customer=self.customer)
        self.order = Orders.objects.create(customer=self.customer, payment_mode="Cash", order_status="received",
                                           active=True)
        self.order_detail_url = reverse("orders:orders-detail", args=[self.order.id])
        self.order_payload = {
            "payment_mode": "Mpesa",
            "order_status": "received",
            "active": True,
            "items": [
                {
                    "item": self.product.id,
                    "quantity": self.fake.random_digit(),
                    "ordered": False
                }
            ]
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
