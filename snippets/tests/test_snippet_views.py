from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase
from rest_framework import status
from snippets.models.audit_log import AuditLog
from snippets.models.snippet import Snippet

class SnippetListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="A", password="password", is_staff=True)

    def test_creating_snippet_logs_to_audit_log(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.post("/snippets/", {"title": "x", "code": "print(\"hi\")"})
        log_item = AuditLog.objects.first()
        self.assertEqual(log_item.content_type, ContentType.objects.get_for_model(Snippet))
        self.assertEqual(log_item.object_id, 1)
        self.assertEqual(log_item.user.id, self.user.id)
        self.assertEqual(log_item.action, "CREATE")


class SnippetDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=1, username="A", password="password", is_staff=True)

    def test_destroying_snippet_logs_to_audit_log(self):
        Snippet.objects.create(id=1, title="x", code="print(\"hi\")", owner=self.user)
        self.client.login(username=self.user.username, password="password")
        response = self.client.delete("/snippets/1/")
        log_item = AuditLog.objects.first()
        self.assertEqual(log_item.content_type, ContentType.objects.get_for_model(Snippet))
        self.assertEqual(log_item.object_id, 1)
        self.assertEqual(log_item.user.id, self.user.id)
        self.assertEqual(log_item.action, "DESTROY")

    def test_updating_snippet_logs_to_audit_log(self):
        Snippet.objects.create(id=1, title="x", code="print(\"hi\")", owner=self.user)
        self.client.login(username=self.user.username, password="password")
        response = self.client.patch("/snippets/1/", {"title": "y"})
        log_item = AuditLog.objects.first()
        self.assertEqual(log_item.content_type, ContentType.objects.get_for_model(Snippet))
        self.assertEqual(log_item.object_id, 1)
        self.assertEqual(log_item.user.id, self.user.id)
        self.assertEqual(log_item.action, "UPDATE")