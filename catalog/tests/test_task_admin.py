from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from catalog.models import Task


class TaskAdminTestCase(APITestCase):
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
        self.task = Task.objects.create(task_name='Test Task', priority='l', status='t', slug='test-task', assignee=self.admin_user)

        self.client.force_authenticate(user=self.admin_user)

    def test_get_task(self):
        response = self.client.get(reverse('task_admin_details', args=[str(self.task.slug)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_name'], 'Test Task')

    def test_update_task(self):
        new_task_name = 'Updated Task'
        response = self.client.patch(reverse('task_admin_details', args=[str(self.task.slug)]),
                                     {'task_name': new_task_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_name'], new_task_name)

    def test_delete_task(self):
        response = self.client.delete(reverse('task_admin_details', args=[str(self.task.slug)]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(slug=self.task.slug).exists())
