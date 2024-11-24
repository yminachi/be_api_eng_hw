from django.contrib.auth.models import User
from rest_framework import generics, permissions
from snippets.serializers.user_serializer import UserSerializer
from snippets.permissions import IsStaffOrReadOnly
from snippets.models.audit_log import AuditLog

class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsStaffOrReadOnly,
    )

    def get_queryset(self):
        show_inactive_param = self.request.query_params.get('show_inactive', "false").lower() == "true"
        qs = User.objects.all() if show_inactive_param and self.request.user and self.request.user.is_staff else User.objects.filter(is_active=True)
        return qs.prefetch_related("snippets").order_by("id")

    def perform_create(self, serializer):
        instance = serializer.save()
        AuditLog.log(user=self.request.user, instance=instance, action=AuditLog.Actions.CREATE)


class UserDetail(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsStaffOrReadOnly,
    )

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        AuditLog.log(user=self.request.user, instance=instance, action=AuditLog.Actions.DESTROY)
