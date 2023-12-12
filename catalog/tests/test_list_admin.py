from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from catalog.models import Task, List


class ListAdminTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin',
                                                   password='testpass123')
        self.reg_user = User.objects.create_user(username='testUser',
                                                 password='test2pass123')
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        group_name = "Admin"
        self.group = Group(name=group_name)
        self.group.save()
        self.admin_user.groups.add(self.group)
        self.task = Task.objects.create(task_name='Test Task', priority='l',
                                        status='t', slug='test-task',
                                        assignee=self.admin_user)
        self.list = List.objects.create(list_name='Test List',
                                        slug='test-list')
        self.list.assigned_tasks.add(self.task)
        self.list.assigned_users.add(self.reg_user)

        self.client.force_authenticate(user=self.admin_user)

    def test_get_list_as_admin(self):
        response = self.client.get(
            reverse('list_admin_details', args=[str(self.list.slug)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['list_name'], 'Test List')

    def test_update_list_as_admin(self):
        new_list_name = 'Updated List'
        response = self.client.patch(
            reverse('list_admin_details', args=[str(self.list.slug)]),
            {'list_name': new_list_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['list_name'], new_list_name)

    def test_delete_list_as_admin(self):
        response = self.client.delete(
            reverse('list_admin_details', args=[str(self.list.slug)]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(List.objects.filter(slug=self.list.slug).exists())
