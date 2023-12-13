from datetime import datetime

from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from catalog.models import Reminder, Task


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

        self.task = Task.objects.create(task_name='Test Task', priority='l',
                                        status='t', slug='test-task',
                                        assignee=self.admin_user)
        self.reminder = Reminder.objects.create(username=self.admin_user,
                                                task_id=self.task,
                                                slug='test-reminder',
                                                date=datetime.now())

    def test_admin_list_create(self):
        response = self.client.get(reverse('reminder_admin_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_update_delete(self):
        response = self.client.get(
            reverse('reminder_admin_details', args=[str(self.reminder.slug)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_create_reminder(self):
        date = datetime.now().isoformat()
        data = {'task_id': self.task.task_id, 'username': self.admin_user.id,
                'slug': 'new-reminder',
                'date': date}
        response = self.client.post(reverse('reminder_admin_list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Reminder.objects.filter(slug='new-reminder').exists())

    def test_admin_get_reminder(self):
        response = self.client.get(
            reverse('reminder_admin_details', args=[str(self.reminder.slug)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_update_reminder(self):
        new_date = datetime.now().isoformat()
        response = self.client.patch(
            reverse('reminder_admin_details', args=[str(self.reminder.slug)]),
            {'date': new_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Reminder.objects.get(slug=self.reminder.slug).date.isoformat(),
            new_date + '+00:00')

    def test_admin_delete_reminder(self):
        response = self.client.delete(
            reverse('reminder_admin_details', args=[str(self.reminder.slug)]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Reminder.objects.filter(slug=self.reminder.slug).exists())

    def test_admin_get_nonexistent_reminder(self):
        response = self.client.get(
            reverse('reminder_admin_details', args=['nonexistent-reminder']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_update_nonexistent_reminder(self):
        response = self.client.patch(
            reverse('reminder_admin_details', args=['nonexistent-reminder']),
            {'date': '2023-12-31T23:59:59Z'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_delete_nonexistent_reminder(self):
        response = self.client.delete(
            reverse('reminder_admin_details', args=['nonexistent-reminder']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
