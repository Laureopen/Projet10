from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from api.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Route principale : /api/projects/
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

# Routes imbriquées : /api/projects/{project_id}/contributors/
project_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
project_router.register(r'contributors', ContributorViewSet, basename='project-contributors')
project_router.register(r'issues', IssueViewSet, basename='project-issues')

# Nested under issues: /api/projects/{project_id}/issues/{issue_id}/comments/
issue_router = routers.NestedDefaultRouter(project_router, r'issues', lookup='issue')
issue_router.register(r'comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(project_router.urls)),
    path('api/', include(issue_router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
