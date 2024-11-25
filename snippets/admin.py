from django.contrib import admin
from snippets.models.snippet import Snippet
from snippets.models.audit_log import AuditLog


class SnippetAdmin(admin.ModelAdmin):
    readonly_fields = ("highlighted",)

class AuditAdmin(admin.ModelAdmin):
    readonly_fields = ("content_type", "object_id", "user", "action", "timestamp")

admin.site.register(Snippet, SnippetAdmin)
admin.site.register(AuditLog, AuditAdmin)