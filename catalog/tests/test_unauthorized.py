from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase, APIClient

from catalog.models import Task


class UnauthorizedTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testUser', password='testpass123')

    def test_unauthorized_access_task(self):
        self.task = Task.objects.create(task_name='Test Task', priority='l', status='t', slug='test-task')
        response = self.client.get(reverse('task_user_details', args=[str(self.task.slug)]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
