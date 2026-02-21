from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class PageTests(TestCase):
    def test_landing_page_loads(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)


class AuthFlowTests(TestCase):
    def test_register_creates_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'alice',
            'email': 'alice@example.com',
            'password1': 'strongpass123!',
            'password2': 'strongpass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='alice').exists())

    def test_logged_in_user_can_analyze_news(self):
        user = User.objects.create_user(username='bob', password='pass12345!')
        client = Client()
        client.login(username='bob', password='pass12345!')
        response = client.post(reverse('dashboard'), {
            'headline': 'Government releases report on healthcare outcomes',
            'content': 'Official report with data and analysis was published.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detection Result')
