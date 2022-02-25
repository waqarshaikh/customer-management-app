from django.test import TestCase
class URLTests(TestCase):
    def test_homepage_redirects_to_loginpage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/')