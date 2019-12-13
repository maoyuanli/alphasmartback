from django.test import TestCase
from account.views import UserRegisterView
from rest_framework.test import APIClient
import json


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

