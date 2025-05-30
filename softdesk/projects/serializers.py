from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from django.contrib.auth import get_user_model

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['author']

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

    def validate(self, data):
        # Validation si l'utilisateur assigné fait bien partie du projet
        assignee = data.get('assignee_user')
        project = data.get('project')
        if assignee and not Contributor.objects.filter(user=assignee, project=project).exists():
            raise serializers.ValidationError("L'utilisateur assigné n'est pas un contributeur de ce projet.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        issue = data.get('issue')
        author = data.get('author_user')

        # On vérifie que l’issue est bien définie
        if not issue:
            raise serializers.ValidationError("Une issue doit être spécifiée.")

        # Vérifier que l’auteur est contributeur du projet lié à l’issue
        project = issue.project
        if not Contributor.objects.filter(user=author, project=project).exists():
            raise serializers.ValidationError("L'auteur doit être un contributeur du projet lié à cette issue.")

        return data
