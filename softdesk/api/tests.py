from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Project, User


class ProjectTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project_data = {
            'title': 'Test Project',
            'description': 'A simple test project.',
            'type': 'back',
        }

    def test_create_project(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('project-list'), self.project_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)

    def test_get_projects(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

