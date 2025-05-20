from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)

    def is_minor(self):
        return self.age is not None and self.age < 15

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    TYPE_CHOICES = [('back', 'Back-end'), ('front', 'Front-end'), ('iOS', 'iOS'), ('android', 'Android')]
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue(models.Model):
    id = models.AutoField(primary_key=True)
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
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
