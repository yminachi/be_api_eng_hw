from django.contrib.contenttypes.models import ContentType
from django.db import models

class AuditLog(models.Model):
    class Actions(models.TextChoices):
        CREATE = ("CREATE", "CREATE")
        UPDATE = ("UPDATE", "UPDATE")
        DESTROY = ("DESTROY", "DESTROY")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = object_id = models.PositiveIntegerField()
    user = models.ForeignKey("auth.User", related_name="audits", on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=16, choices=Actions.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def log(self, user, instance, action):
        content_type = ContentType.objects.get_for_model(instance)
        self.objects.create(
            content_type=content_type,
            user=user,
            object_id=instance.id,
            action=action
        )