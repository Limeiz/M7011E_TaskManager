from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from catalog.models import Task


class TaskAdminTestCase(APITestCase):
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
        self.task = Task.objects.create(task_name='Test Task', priority='l',
                                        status='t', slug='test-task',
                                        assignee=self.reg_user)

        self.other_user = User.objects.create_user(username='otherUser',
                                                   password='test2pass123')
        self.other_users_task = Task.objects.create(task_name='Secret Task',
                                                    priority='l', status='t',
                                                    slug='secret-task',
                                                    assignee=self.other_user)

        self.client.force_authenticate(user=self.reg_user)

    def test_get_task(self):
        response = self.client.get(
            reverse('task_user_details', args=[str(self.task.slug)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_name'], 'Test Task')

    def test_get_secret_task(self):
        response = self.client.get(reverse('task_user_details', args=[
            str(self.other_users_task.slug)]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task(self):
        new_task_name = 'Updated Task'
        response = self.client.patch(
            reverse('task_user_details', args=[str(self.task.slug)]),
            {'task_name': new_task_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_name'], new_task_name)

    def test_update_secret_task(self):
        new_task_name = 'Updated Secret Task'
        response = self.client.patch(reverse('task_user_details', args=[
            str(self.other_users_task.slug)]),
                                     {'task_name': new_task_name})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        response = self.client.delete(
            reverse('task_user_details', args=[str(self.task.slug)]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(slug=self.task.slug).exists())

    def test_delete_secret_task(self):
        response = self.client.delete(reverse('task_user_details', args=[
            str(self.other_users_task.slug)]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Task.objects.filter(slug=self.other_users_task.slug).exists())
