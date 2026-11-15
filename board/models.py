from django.conf import settings
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_projects")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="board_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self): return self.name

class Task(models.Model):
    STATUS = [("todo","To do"),("doing","In progress"),("done","Done")]
    PRIORITY = [("low","Low"),("medium","Medium"),("high","High")]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tasks")
    status = models.CharField(max_length=10, choices=STATUS, default="todo")
    priority = models.CharField(max_length=10, choices=PRIORITY, default="medium")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["status", "due_date", "-created_at"]
    def __str__(self): return self.title

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]
