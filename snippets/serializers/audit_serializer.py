from rest_framework import serializers
from snippets.models.audit_log import AuditLog

class AuditLogSerializer(serializers.ModelSerializer): 
    user = serializers.CharField(source="user.username", read_only=True)
    content_type = serializers.CharField(source="content_type.model", read_only=True)

    class Meta:
        model = AuditLog
        fields = (
            "user",
            "content_type",
            "object_id",
            "action",
            "timestamp",
        )  

