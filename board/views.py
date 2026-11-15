from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Project, Task, TaskComment

@login_required
def dashboard(request):
    projects = Project.objects.filter(owner=request.user) | Project.objects.filter(members=request.user)
    return render(request, "board/dashboard.html", {"projects": projects.distinct()})

@login_required
@require_POST
def create_project(request):
    name = request.POST.get("name", "").strip()
    description = request.POST.get("description", "").strip()
    if name:
        project = Project.objects.create(name=name[:120], description=description[:2000], owner=request.user)
        project.members.add(request.user)
        messages.success(request, "Project created.")
        return redirect("project_detail", pk=project.pk)
    messages.error(request, "Project name is required.")
    return redirect("dashboard")

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner_id != request.user.id and not project.members.filter(pk=request.user.pk).exists():
        messages.error(request, "You don't have access to this project.")
        return redirect("dashboard")
    tasks = project.tasks.select_related("assigned_to").prefetch_related("comments__author")
    users = project.members.all()
    return render(request, "board/project_detail.html", {"project": project, "tasks": tasks, "users": users})

@login_required
@require_POST
def create_task(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner_id != request.user.id and not project.members.filter(pk=request.user.pk).exists():
        return redirect("dashboard")
    title = request.POST.get("title", "").strip()
    if not title:
        messages.error(request, "Task title is required.")
        return redirect("project_detail", pk=pk)
    assigned = None
    assigned_id = request.POST.get("assigned_to")
    if assigned_id:
        assigned = project.members.filter(pk=assigned_id).first()
    due = request.POST.get("due_date") or None
    Task.objects.create(project=project, title=title[:160], description=request.POST.get("description","")[:2000],
                        assigned_to=assigned, status=request.POST.get("status","todo") if request.POST.get("status") in ["todo","doing","done"] else "todo",
                        priority=request.POST.get("priority","medium") if request.POST.get("priority") in ["low","medium","high"] else "medium",
                        due_date=due)
    messages.success(request, "Task added.")
    return redirect("project_detail", pk=pk)

@login_required
@require_POST
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if project.owner_id != request.user.id and not project.members.filter(pk=request.user.pk).exists():
        return redirect("dashboard")
    status = request.POST.get("status")
    priority = request.POST.get("priority")
    if status in ["todo","doing","done"]: task.status = status
    if priority in ["low","medium","high"]: task.priority = priority
    task.save()
    return redirect("project_detail", pk=project.pk)

@login_required
@require_POST
def add_comment(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if project.owner_id != request.user.id and not project.members.filter(pk=request.user.pk).exists():
        return redirect("dashboard")
    text = request.POST.get("text","").strip()
    if text:
        TaskComment.objects.create(task=task, author=request.user, text=text[:500])
    return redirect("project_detail", pk=project.pk)
def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "board/register.html", {"form": form})
@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner_id != request.user.id:
        messages.error(request, "You cannot edit this project.")
        return redirect("dashboard")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if name:
            project.name = name[:120]
            project.description = description[:2000]
            project.save()
            messages.success(request, "Project updated successfully!")
            return redirect("project_detail", pk=pk)

        messages.error(request, "Project name is required.")

    return render(request, "board/edit_project.html", {"project": project})