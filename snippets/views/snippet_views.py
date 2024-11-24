from rest_framework import generics, permissions, renderers
from rest_framework.response import Response
from snippets.models.snippet import Snippet
from snippets.models.audit_log import AuditLog
from snippets.serializers.snippet_serializer import SnippetSerializer
from snippets.permissions import IsOwnerOrReadOnly


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        AuditLog.log(user=self.request.user, instance=instance, action=AuditLog.Actions.CREATE)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def perform_update(self, serializer):
        instance = serializer.save(owner=self.request.user)
        AuditLog.log(user=self.request.user, instance=instance, action=AuditLog.Actions.UPDATE)

    def perform_destroy(self, instance):
        AuditLog.log(user=self.request.user, instance=instance, action=AuditLog.Actions.DESTROY)
        instance.delete()

