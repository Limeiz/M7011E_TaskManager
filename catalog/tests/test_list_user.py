from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from catalog.models import Task, List


class ListUserTestCase(APITestCase):
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
        self.list = List.objects.create(list_name='Test List',
                                        slug='test-list')
        self.list.assigned_tasks.add(self.task)
        self.list.assigned_users.add(self.reg_user)

    def test_get_list_as_regular_user(self):
        response = self.client.get(
            reverse('list_user_details', args=[str(self.list.slug)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['list_name'], 'Test List')

    def test_update_list_as_regular_user(self):
        new_list_name = 'Updated List'
        response = self.client.patch(
            reverse('list_user_details', args=[str(self.list.slug)]),
            {'list_name': new_list_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['list_name'], new_list_name)

    def test_delete_list_as_regular_user(self):
        response = self.client.delete(
            reverse('list_user_details', args=[str(self.list.slug)]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(List.objects.filter(slug=self.list.slug).exists())

    def test_get_nonexistent_list_as_regular_user(self):
        response = self.client.get(
            reverse('list_user_details', args=['nonexistent-list']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_list_as_regular_user(self):
        new_list_name = 'Updated List'
        response = self.client.patch(
            reverse('list_user_details', args=['nonexistent-list']),
            {'list_name': new_list_name})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_list_as_regular_user(self):
        response = self.client.delete(
            reverse('list_user_details', args=['nonexistent-list']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_list_as_regular_user(self):
        data = {'list_name': 'New List', 'slug': 'new-list'}
        response = self.client.post(reverse('list_user_list'), data)
        print(response.content) # same problem with all list create
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(List.objects.filter(slug='new-list').exists())

    def test_create_list_with_existing_slug_as_regular_user(self):
        existing_list = List.objects.create(list_name='Existing List',
                                            slug='existing-list')
        data = {'list_name': 'Duplicate List', 'slug': 'existing-list'}
        response = self.client.post(reverse('list_user_list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            List.objects.filter(list_name='Duplicate List').exists())

    # doesn't work right now but maybe it should? feels like bad security otherwise
    def test_create_list_with_existing_slug_by_other_user(self):
        other_user = User.objects.create_user(username='otherUser',
                                              password='otherpass123')
        other_user.groups.add(self.group)
        other_user_token = Token.objects.create(user=other_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {other_user_token.key}')

        existing_list = List.objects.create(list_name='Existing List',
                                            slug='existing-list')

        data = {'list_name': 'Duplicate List', 'slug': 'existing-list'}
        response = self.client.post(reverse('list_user_list'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(List.objects.filter(slug='existing-list',
                                            assigned_users=other_user).exists())
