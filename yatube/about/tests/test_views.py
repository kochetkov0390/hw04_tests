from django.test import Client, TestCase


class ViewTestClass(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_view(self):
        response = self.client.get('/about/author/')
        self.assertTemplateUsed(response, 'about/author.html')

    def test_tech_view(self):
        response = self.client.get('/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html')
