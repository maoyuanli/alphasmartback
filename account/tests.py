from django.test import TestCase, RequestFactory

from account.views import AccountView
from rest_framework.test import APIClient
from rest_framework import status


class AccountApiTest(TestCase):
    account_api = AccountView()


    def test_create_user(self):
        self.account_api.register(
            '/api/order',
            {
                'first_name': 'James',
                'last_name': 'Bond',
                'username': 'james007',
                'email': 'james.bond@mi5.uk',
                'password': 'testpass'
            }
        )
