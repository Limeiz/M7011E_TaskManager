from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from catalog.models import Reminder


class ReminderRegularUserTestCase(APITestCase):


    def setUp(self):
        self.client = APIClient()
        self.reg_user = User.objects.create_user(username='testUser',
                                                   password='testpass123')
        self.token = Token.objects.create(user=self.reg_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        group_name = "RegularUser"
        self.group = Group(name=group_name)
        self.group.save()
        self.reg_user.groups.add(self.group)
        self.reminder = Reminder.objects.create(reminder_name='Test Reminder', slug='test-reminder')

        self.client.force_authenticate(user=self.reg_user)

    def test_regular_user_list_create(self):
        response = self.client.get(reverse('reminder_user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_get_update_delete(self):
        response = self.client.get(reverse('reminder_admin_details'), args=[str(self.reminder.slug)])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

