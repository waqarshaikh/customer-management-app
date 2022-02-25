from django.test import TestCase
class URLTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.url, '/login/?next=/')
        