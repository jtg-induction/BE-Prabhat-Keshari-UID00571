from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from projects.models import Project
from users.models import CustomUser


class ProjectMemberApiViewTestCase(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            email='test1@gmail.com', password='testPassword',
            first_name='John', last_name='Doe'
        )
        self.user2 = CustomUser.objects.create_user(
            email='test2@gmail.com', password='testPassword',
            first_name='John', last_name='Doe'
        )
        self.user3 = CustomUser.objects.create_user(
            email='test3@gmail.com', password='testPassword',
            first_name='John', last_name='Doe'
        )

        self.project1 = Project.objects.create(
            name='test project', max_members=2
        )
        self.project2 = Project.objects.create(
            name='test project', max_members=3
        )
        self.project3 = Project.objects.create(
            name='test project', max_members=3
        )

        self.token = Token.objects.create(user=self.user1)
        self.client = APIClient()

    def test_add_member_to_project(self):
        url = reverse(
            'projects:project-add', kwargs={'pk': self.project1.pk, 'action': 'add'}
        )

        self.project2.members.add(self.user2)
        self.project3.members.add(self.user2)

        request_data = {
            'user_ids': [self.user1.id]
        }

        expected_response = {
            "logs": {
                self.user1.id: "User added to project successfully.",
                self.user2.id: "Cannot add as User is a member in two projects."
            }
        }

        response = self.client.patch(
            url, request_data, HTTP_AUTHORIZATION=f'Token {self.token.key}', format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.json(), expected_response)

    def test_maxmember_add_member_to_project(self):
        url = reverse(
            'projects:project-add', kwargs={'pk': self.project1.pk, 'action': 'add'}
        )

        self.project1.members.add(self.user1)
        self.project1.members.add(self.user2)

        request_data = {
            'user_ids': [self.user3.id]
        }

        expected_response = {
            "logs": {
                self.user3.id: f"Project cannot have more than {self.project1.max_members} members."
            }
        }

        response = self.client.patch(
            url, request_data, HTTP_AUTHORIZATION=f'Token {self.token.key}', format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.json(), expected_response)

    def test_remove_member_to_project(self):
        url = reverse(
            'projects:project-remove', kwargs={'pk': self.project1.pk, 'action': 'remove'}
        )

        self.project1.members.add(self.user1)

        request_data = {
            'user_ids': [self.user1.id, self.user2.id]
        }

        expected_response = {
            "logs": {
                "8": "User removed successfully.",
                "1": "User is not a member of project."
            }
        }

        response = self.client.patch(
            url, request_data, HTTP_AUTHORIZATION=f'Token {self.token.key}', format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.json(), expected_response)
