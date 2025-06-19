from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.save(author=user)
        Contributor.objects.get_or_create(user=user, project=project)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.author != request.user:
            return Response({"Message": "Vous n'êtes pas l’auteur de ce projet."}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.author != request.user:
            return Response({"Message": "Vous n'êtes pas l’auteur de ce projet."}, status=403)
        return super().destroy(request, *args, **kwargs)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        if project_id:
            return Contributor.objects.filter(project__id=project_id)
        return Contributor.objects.all()


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assignee_user']

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk') or self.request.query_params.get('project')
        user = self.request.user
        if project_id:
            if not Contributor.objects.filter(user=user, project_id=project_id).exists():
                raise PermissionDenied("Vous devez être contributeur du projet.")
            return Issue.objects.filter(project_id=project_id).order_by('id')
        return Issue.objects.all()

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionDenied("Vous devez être contributeur du projet.")
        serializer.save(author_user=self.request.user)

    def perform_update(self, serializer):
        issue = self.get_object()
        if issue.author_user != self.request.user:
            raise PermissionDenied("Seul l'auteur de l'issue peut la modifier.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.author_user != request.user:
            raise PermissionDenied("Seul l'auteur de l'issue peut la supprimer.")
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author_user']  # <-- filtrage par auteur

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_pk')
        print(Comment.objects.filter(issue__id=issue_id))
        return Comment.objects.filter(issue__id=issue_id)

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        user = self.request.user
        project = comment.issue.project

        if comment.author_user != user:
            raise PermissionDenied("Seul l'auteur du commentaire peut le modifier.")

        if not Contributor.objects.filter(user=user, project=project).exists():
            raise PermissionDenied("Vous devez être contributeur du projet.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        user = request.user
        project = comment.issue.project

        if comment.author_user != user:
            raise PermissionDenied("Seul l'auteur du commentaire peut le supprimer.")

        if not Contributor.objects.filter(user=user, project=project).exists():
            raise PermissionDenied("Vous devez être contributeur du projet.")
        return super().destroy(request, *args, **kwargs)
