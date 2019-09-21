from django.test import TestCase

from django.test import TestCase
from rest_framework.test import APIClient


# Using the standard RequestFactory API to create a form POST request
class ViewTests(TestCase):
    def test_post_feedback(self):
        client = APIClient()
        client.post('/api/feedback',
                    {
                        'name': 'John Snow',
                        'email': 'john.snow@got.ca',
                        'phone': '470-090-1231',
                        'comment': 'Please join us for the fight!!!'
                    },
                    format='json')
