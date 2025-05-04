from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)

class Project(models.Model):
    TYPE_CHOICES = [('back', 'Back-end'), ('front', 'Front-end'), ('iOS', 'iOS'), ('android', 'Android')]
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

class Issue(models.Model):
    TAG_CHOICES = [('bug', 'Bug'), ('task', 'Task'), ('upgrade', 'Upgrade')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('to-do', 'To Do'), ('in-progress', 'In Progress'), ('done', 'Done')]
    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues_created')
    assignee_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues_assigned')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Comment(models.Model):
    description = models.TextField()
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
