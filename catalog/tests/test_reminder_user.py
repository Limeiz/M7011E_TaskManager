from datetime import datetime

from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from catalog.models import Reminder, Task


class ReminderRegularUserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.reg_user = User.objects.create_user(username='testUser',
                                                 password='testpass123')
        self.token = Token.objects.create(user=self.reg_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.other_user = User.objects.create_user(username='otherUser',
                                                   password='otherpass123')
        self.other_user_token = Token.objects.create(user=self.other_user)

        group_name = "RegularUser"
        self.group = Group(name=group_name)
        self.group.save()
        self.reg_user.groups.add(self.group)
        self.other_user.groups.add(self.group)

        self.task = Task.objects.create(task_name='Test Task', priority='l',
                                        status='t', slug='test-task',
                                        assignee=self.reg_user)
        self.task2 = Task.objects.create(task_name='Test Task 2', priority='l',
                                         status='t', slug='test-task2',
                                         assignee=self.other_user)
        self.reminder = Reminder.objects.create(username=self.reg_user,
                                                task_id=self.task,
                                                slug='test-reminder',
                                                date=datetime.now())
        self.other_user_reminder = Reminder.objects.create(
            username=self.other_user,
            task_id=self.task2,
            slug='other-reminder',
            date=datetime.now())

        self.client.force_authenticate(user=self.reg_user)

    def test_regular_user_list_create(self):
        response = self.client.get(reverse('reminder_user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_get_update_delete(self):
        response = self.client.get(
            reverse('reminder_user_details', args=[str(self.reminder.slug)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_users_reminder_work(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse('reminder_user_details', args=[
            str(self.other_user_reminder.slug)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cant_get_other_users_reminder_details(self):
        response = self.client.get(reverse('reminder_user_details', args=[
            str(self.other_user_reminder.slug)]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_regular_user_cant_update_other_users_reminder(self):
        new_date = '2024-01-01T12:00:00Z'
        updated_data = {'date': new_date}

        response = self.client.patch(reverse('reminder_user_details', args=[
            str(self.other_user_reminder.slug)]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_regular_user_cant_delete_other_users_reminder(self):
        response = self.client.delete(reverse('reminder_user_details', args=[
            str(self.other_user_reminder.slug)]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            Reminder.objects.filter(slug='other-reminder').exists())
