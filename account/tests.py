import json

from django.test import TestCase
from rest_framework.test import APIClient

from account.views import UserRegisterView


class AccountApiTest(TestCase):
    account_api = UserRegisterView()
    client = APIClient()

    def test_create_user(self):
        post_data = json.dumps(
            {
                "first_name": "James",
                "last_name": "Bond",
                "username": "james007ca",
                "email": "james.bond2@mi5.uk",
                "password": "testpass"
            }
        )

        self.client.post('api/account/', {"new_user": post_data})
