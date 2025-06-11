from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from django.contrib.auth import get_user_model


class ProjectSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Project.
    Permet la création, lecture, mise à jour et suppression d’un projet.
    Le champ 'author' est en lecture seule : il est automatiquement défini dans la vue.
    """
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['author']  # L’auteur est défini automatiquement depuis la vue


class ContributorSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Contributor.
    Utilisé pour ajouter ou afficher des contributeurs à un projet.
    """
    class Meta:
        model = Contributor
        fields = ['user', 'project']


class IssueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Issue avec contrôle des permissions :
    - Création : l'utilisateur doit être contributeur du projet
    - Modification/Suppression : l'utilisateur doit être contributeur du projet
    """

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'assignee_user', 'project']

    def create(self, validated_data):
        """Création avec vérification que l'utilisateur est contributeur"""
        user = self.context['request'].user
        project = validated_data.get('project')

        if not Contributor.objects.filter(user=user, project=project).exists():
            raise serializers.ValidationError(
                {"Message": "Vous devez être contributeur du projet pour créer une issue."}
            )

        validated_data['author_user'] = user
        return super().create(validated_data)

    def validate(self, data):
        """Validation pour création ET modification"""
        user = self.context['request'].user
        project = data.get('project', getattr(self.instance, 'project', None))
        assignee = data.get('assignee_user')

        # Vérification que le projet existe
        if not project:
            raise serializers.ValidationError(
                {"Message": "Le projet doit être spécifié."}
            )

        # Vérification que l'utilisateur est contributeur
        if not Contributor.objects.filter(user=user, project=project).exists():
            raise serializers.ValidationError(
                {"Message": "Vous devez être contributeur du projet pour modifier cette issue."}
            )

        # Vérification que l'assigné est contributeur (si modification de l'assigné)
        if assignee and not Contributor.objects.filter(user=assignee, project=project).exists():
            raise serializers.ValidationError(
                {"Message": "L'utilisateur assigné n'est pas contributeur de ce projet."}
            )

        return data

    def update(self, instance, validated_data):
        """Mise à jour avec les mêmes vérifications que validate()"""
        # La méthode validate() est automatiquement appelée avant update()
        return super().update(instance, validated_data)

    def delete(self, instance):
        """Suppression avec vérification des permissions"""
        user = self.context['request'].user
        if not Contributor.objects.filter(user=user, project=instance.project).exists():
            raise serializers.ValidationError(
                {"Message": "Vous devez être contributeur du projet pour supprimer cette issue."}
            )
        instance.delete()


class CommentSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Comment.
    - L'issue est automatiquement récupérée depuis l'URL
    - L'auteur est automatiquement défini comme l'utilisateur connecté
    """

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_time', 'author_user', 'issue']
        read_only_fields = ['author_user', 'issue', 'created_time']

    def validate(self, data):
        """
        Validation personnalisée :
        - Vérifie que l'utilisateur est contributeur du projet
        """
        request = self.context.get('request')
        view = self.context.get('view')

        # Récupération de l'issue depuis l'URL
        issue_id = view.kwargs.get('issue_pk')
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            raise serializers.ValidationError({
                'detail': "L'issue spécifiée n'existe pas."
            })

        # Vérification des permissions
        if not Contributor.objects.filter(user=request.user, project=issue.project).exists():
            raise serializers.ValidationError({
                'detail': "Vous devez être contributeur du projet pour commenter cette issue."
            })

        return data

    def create(self, validated_data):
        """
        Création du commentaire :
        - Définit automatiquement l'issue depuis l'URL
        - Définit l'auteur comme l'utilisateur connecté
        """
        request = self.context.get('request')
        view = self.context.get('view')

        # Définition de l'issue depuis l'URL
        issue_id = view.kwargs.get('issue_pk')
        validated_data['issue'] = Issue.objects.get(pk=issue_id)

        # Définition de l'auteur
        validated_data['author_user'] = request.user

        return super().create(validated_data)