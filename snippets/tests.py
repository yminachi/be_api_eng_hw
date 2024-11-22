from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class UserListViewTests(APITestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username="Staff", password="password", is_staff=True)
        self.non_staff_user = User.objects.create_user(username="Someone", password="password", is_staff=False)
        self.inactive_user = User.objects.create_user(username="Inactive", password="password", is_active=False)

    def test_lists_active_users(self):
        response = self.client.get("/users/")
        self.assertEqual(len(response.data["results"]), 2)
    
    def test_lists_all_users_including_inactive(self):
        self.client.login(username=self.staff_user.username, password="password")
        response = self.client.get("/users/?show_inactive=true")
        self.assertEqual(len(response.data["results"]), 3)
    
    def test_non_staff_cant_see_inactive_users(self):
        self.client.login(username=self.non_staff_user.username, password="password")
        response = self.client.get("/users/?show_inactive=true")
        self.assertEqual(len(response.data["results"]), 2)
    
    def test_creates_user(self):
        login_response = self.client.login(username=self.staff_user.username, password="password")
        response = self.client.post("/users/", {"username": "newUser"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(User.objects.filter(username="newUser").first())
    
    def test_non_staff_cant_create_new_user(self):
        self.client.login(username=self.non_staff_user.username, password="password")
        response = self.client.post("/users/", {"username": "newUser"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNone(User.objects.filter(username="newUser").first())

class UserDetailViewTests(APITestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(id=1, username="Staff", password="password", is_staff=True)
        self.non_staff_user = User.objects.create_user(id=2, username="Someone", password="password", is_staff=False)
        self.inactive_user = User.objects.create_user(id=3, username="Inactive", password="password", is_active=False)

    def test_retrieves_active_user(self):
        self.client.login(username=self.non_staff_user.username, password="password")
        response = self.client.get("/users/1/")
        self.assertEqual(response.data["username"], self.staff_user.username)
    
    def test_retrieves_inactive_user(self):
        self.client.login(username=self.staff_user.username, password="password")
        response = self.client.get("/users/3/")
        self.assertEqual(response.data["username"], self.inactive_user.username)

    def test_non_staff_cant_retrive_inactive_user(self):
        self.client.login(username=self.non_staff_user.username, password="password")
        response = self.client.get("/users/3/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deletes_user(self):
        User.objects.create_user(id=4, username="Deleteme")
        self.client.login(username=self.staff_user.username, password="password")
        response = self.client.delete("/users/4/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username="Deleteme").first().is_active)
    
    def test_non_staff_cant_delete_user(self):
        User.objects.create_user(id=4, username="Deleteme")
        self.client.login(username=self.non_staff_user.username, password="password")
        response = self.client.delete("/users/4/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(username="Deleteme").first().is_active)
