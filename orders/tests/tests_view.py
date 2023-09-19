from rest_framework import status
from .test_setup import TestSetup


class TestOrderView(TestSetup):
    def test_add_unauthenticated_order_request(self):
        res = self.client.post(self.order_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_order_without_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.post(self.order_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_order_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.post(self.order_url, self.order_payload, format='json')
        self.assertEqual(res.data['error'], False)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_fetch_orders(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.get(self.order_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_fetch_single_orders(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.get(self.order_detail_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.delete(self.order_detail_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.patch(self.order_detail_url, self.order_payload, format='json')
        self.assertEqual(res.data['error'], False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
