from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from snippets.models.audit_log import AuditLog

class AuditViewTests(APITestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username="Staff", password="password", is_staff=True)
        self.non_staff_user = User.objects.create_user(username="Someone", password="password", is_staff=False)
        AuditLog.log(user=self.staff_user, instance=self.non_staff_user, action=AuditLog.Actions.CREATE)

        user_2 = User.objects.create_user(username="2", password="password", is_staff=False)
        AuditLog.log(user=self.staff_user, instance=user_2, action=AuditLog.Actions.CREATE)
        AuditLog.log(user=self.staff_user, instance=user_2, action=AuditLog.Actions.UPDATE)
        AuditLog.log(user=self.staff_user, instance=user_2, action=AuditLog.Actions.DESTROY)

    def test_lists_log_for_staff(self):
        self.client.login(username=self.staff_user.username, password="password")
        response = self.client.get("/audit/")
        self.assertEqual(len(response.data["results"]), 4)
    
    def test_does_not_list_for_non_staff(self):
        self.client.login(username=self.non_staff_user.username, password="password")
        response = self.client.get("/audit/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_does_not_list_for_non_authenticated_user(self):
        response = self.client.get("/audit/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    