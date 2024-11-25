from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets.views import snippet_views, user_views, api_root_views, audit_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("snippets/", snippet_views.SnippetList.as_view(), name="snippet-list"),
    path("snippets/<int:pk>/", snippet_views.SnippetDetail.as_view(), name="snippet-detail"),
    path(
        "snippets/<int:pk>/highlight/",
        snippet_views.SnippetHighlight.as_view(),
        name="snippet-highlight",
    ),  
    path("users/", user_views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", user_views.UserDetail.as_view(), name="user-detail"),
    path("audit/", audit_views.AuditList.as_view(), name="audit-list"),
    path("login/", obtain_auth_token),
    path("", api_root_views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)
