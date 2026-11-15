from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.dashboard, name="dashboard"),
    path("projects/create/", views.create_project, name="create_project"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("projects/<int:pk>/edit/", views.edit_project, name="edit_project"),

    path("projects/<int:pk>/tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:pk>/update/", views.update_task, name="update_task"),
    path("tasks/<int:pk>/comment/", views.add_comment, name="add_task_comment"),
]