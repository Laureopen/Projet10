from django.db import models
from users.models import User


class Project(models.Model):
    """
    Modèle représentant un projet logiciel.
    Contient des informations générales comme le titre, la description, le type,
    et l'auteur qui est le créateur du projet.
    """
    TYPE_CHOICES = [
        ('back', 'Back-end'),
        ('front', 'Front-end'),
        ('iOS', 'iOS'),
        ('android', 'Android')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # L'auteur du projet ; suppression cascade si l'utilisateur est supprimé
    created_time = models.DateTimeField(auto_now_add=True)

class Contributor(models.Model):
    """
    Modèle définissant la relation entre un utilisateur et un projet.
    Un contributeur est un utilisateur autorisé à collaborer sur un projet.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # Aucun rôle ou permission ici, mais ce modèle sert de base pour les vérifications d'accès
    created_time = models.DateTimeField(auto_now_add=True)

class Issue(models.Model):
    """
    Modèle représentant une issue (bug, tâche, amélioration) liée à un projet.
    Chaque issue a un auteur, un assigné, une priorité, un statut, et appartient à un projet.
    """
    TAG_CHOICES = [
        ('bug', 'Bug'),
        ('task', 'Task'),
        ('upgrade', 'Upgrade')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('done', 'Done')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues_created')
    # L'utilisateur ayant créé l'issue
    assignee_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues_assigned')
    # L'utilisateur assigné à résoudre l'issue
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # Projet auquel l'issue appartient
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    """
    Modèle représentant un commentaire lié à une issue.
    Chaque commentaire a un auteur, une date de création automatique, et appartient à une issue.
    """
    description = models.TextField()
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    # Date de création automatiquement définie à l'enregistrement
