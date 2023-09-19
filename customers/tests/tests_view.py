from rest_framework import status

from .test_setup import TestSetup


class CustomerTests(TestSetup):
    def test_update_email(self):
        """
            Test an authorised customer
        """
        res = self.client.patch(self.customer_detail_url, self.customer_payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_customers(self):
        """
            Test fetch all customers from the database
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.get(self.customer_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_single_customer(self):
        """
            Test fetch single customers from the database with the customer id
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.get(self.customer_detail_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_customer(self):
        """
            Test Delete customer from the database with the specified id
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        res = self.client.delete(self.customer_detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_customer_details(self):
        """
            Test modify customer information/details from the database
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.AUTH_TOKEN)
        self.customer_payload.pop('email')
        res = self.client.put(self.customer_detail_url, self.customer_payload, format='json')
        self.assertEqual(res.data['error'], False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


