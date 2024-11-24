from rest_framework import generics
from snippets.models.audit_log import AuditLog
from snippets.serializers.audit_serializer import AuditLogSerializer
from snippets.permissions import IsStaff

class AuditList(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = (IsStaff,)
    queryset = AuditLog.objects.select_related("user", "content_type").order_by("-timestamp")
