from rest_framework import status

from .test_setup import TestSetup
from django.contrib.auth import get_user_model


class TestViews(TestSetup):
    def test_customer_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_can_register(self):
        if get_user_model().objects.filter(email=self.customer_payload['email']).exists():
            self.customer_payload['email'] = self.fake.email()
        self.customer_payload['confirm_pass'] = self.customer_payload['password']
        res = self.client.post(self.register_url, self.customer_payload, format='json')
        self.assertEqual(res.data['error'], False)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_super_user(self):
        self.customer_payload['is_staff'] = True
        self.customer_payload['is_superuser'] = True
        self.customer_payload['confirm_pass'] = self.customer_payload['password']
        res = self.client.post(self.register_url, self.customer_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
