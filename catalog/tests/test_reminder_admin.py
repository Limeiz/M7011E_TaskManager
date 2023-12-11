from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from catalog.models import Reminder


class ReminderAdminTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin',
                                                   password='testpass123')
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        group_name = "Admin"
        self.group = Group(name=group_name)
        self.group.save()
        self.admin_user.groups.add(self.group)

        # Create a Reminder
        self.reminder = Reminder.objects.create(reminder_name='Test Reminder', slug='test-reminder')

    def test_admin_list_create(self):
        response = self.client.get(reverse('reminder_admin_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_update_delete(self):
        response = self.client.get(reverse('reminder_admin_details'), args=[str(self.reminder.slug)])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
