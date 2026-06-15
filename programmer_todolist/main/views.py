from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import SignUpForm, ProfileUpdateForm, ProjectForm, ProjectSubmissionForm
from .models import ProgrammerProfile, Project, ProjectSubmission


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    profile = get_object_or_404(ProgrammerProfile, user=request.user)
    assigned_projects = Project.objects.filter(assigned_to=profile).order_by('-created_at')

    context = {
        'profile': profile,
        'assigned_projects': assigned_projects,
        'pending_projects': assigned_projects.filter(status='assigned'),
        'in_progress_projects': assigned_projects.filter(status='in_progress'),
        'completed_projects': assigned_projects.filter(status__in=['completed', 'approved']),
    }
    return render(request, 'dashboard.html', context)


@staff_member_required
def admin_dashboard(request):
    programmers = ProgrammerProfile.objects.all().order_by('-created_at')
    projects = Project.objects.all().order_by('-created_at')
    pending_submissions = ProjectSubmission.objects.filter(is_approved=False)

    context = {
        'programmers': programmers,
        'projects': projects,
        'pending_submissions': pending_submissions,
        'available_programmers': programmers.filter(is_available=True),
        'total_projects': projects.count(),
        'completed_projects': projects.filter(status='approved').count(),
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def profile_edit(request):
    profile = get_object_or_404(ProgrammerProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not request.user.is_staff and project.assigned_to and project.assigned_to.user != request.user:
        messages.error(request, 'You do not have access to this project.')
        return redirect('dashboard')

    return render(request, 'project_detail.html', {'project': project})


@login_required
def start_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, assigned_to__user=request.user)

    if project.status != 'assigned':
        messages.error(request, 'This project cannot be started.')
        return redirect('project_detail', project_id=project.id)

    project.status = 'in_progress'
    project.save()

    messages.success(request, f'Project "{project.title}" started! Happy coding!')
    return redirect('project_detail', project_id=project.id)


@login_required
def submit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, assigned_to__user=request.user)

    if project.status not in ['assigned', 'in_progress']:
        messages.error(request, 'This project cannot be submitted.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.project = project
            submission.save()

            project.status = 'completed'
            project.completed_at = timezone.now()
            project.save()

            messages.success(request, f'Project "{project.title}" submitted! Waiting for admin approval.')
            return redirect('dashboard')
    else:
        form = ProjectSubmissionForm()

    return render(request, 'submit_project.html', {'form': form, 'project': project})


@staff_member_required
def approve_submission(request, submission_id):
    submission = get_object_or_404(ProjectSubmission, id=submission_id)
    project = submission.project

    if request.method == 'POST':
        approval_notes = request.POST.get('approval_notes', '')

        submission.is_approved = True
        submission.approval_notes = approval_notes
        submission.save()

        project.status = 'approved'
        project.approved_at = timezone.now()
        project.save()

        programmer = project.assigned_to
        if programmer:
            programmer.is_available = True
            programmer.save()

        messages.success(request, f'Project "{project.title}" approved! {programmer.full_name} is now available again.')
        return redirect('admin_dashboard')

    return render(request, 'approve_submission.html', {'submission': submission})


@staff_member_required
def assign_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        programmer_id = request.POST.get('programmer_id')
        programmer = get_object_or_404(ProgrammerProfile, id=programmer_id)

        active_projects = Project.objects.filter(
            assigned_to=programmer,
            status__in=['assigned', 'in_progress', 'completed']
        )

        if active_projects.exists():
            messages.error(request, f'{programmer.full_name} still has an active project.')
            return redirect('assign_project', project_id=project.id)

        project.assigned_to = programmer
        project.status = 'assigned'
        project.save()

        messages.success(request, f'Project assigned to {programmer.full_name}!')
        return redirect('project_detail', project_id=project.id)
    else:
        available_programmers = ProgrammerProfile.objects.filter(is_available=True).exclude(
            project__status__in=['assigned', 'in_progress', 'completed']
        ).distinct()

        return render(request, 'assign_project.html', {
            'project': project,
            'available_programmers': available_programmers
        })


@staff_member_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user

            if project.assigned_to:
                active_projects = Project.objects.filter(
                    assigned_to=project.assigned_to,
                    status__in=['assigned', 'in_progress', 'completed']
                )

                if active_projects.exists():
                    messages.error(request, f'{project.assigned_to.full_name} still has an active project!')
                    available_programmers = ProgrammerProfile.objects.filter(is_available=True).exclude(
                        project__status__in=['assigned', 'in_progress', 'completed']
                    ).distinct()
                    return render(request, 'create_project.html', {
                        'form': form,
                        'available_programmers': available_programmers
                    })

                project.status = 'assigned'
            else:
                project.status = 'pending'

            project.save()
            messages.success(request, f'Project "{project.title}" created!')
            return redirect('admin_dashboard')
    else:
        form = ProjectForm()

    available_programmers = ProgrammerProfile.objects.filter(is_available=True).exclude(
        project__status__in=['assigned', 'in_progress', 'completed']
    ).distinct()

    return render(request, 'create_project.html', {
        'form': form,
        'available_programmers': available_programmers
    })


# ===== Management Pages =====

@staff_member_required
def programmer_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    programmers = ProgrammerProfile.objects.all()

    if search_query:
        programmers = programmers.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(skills__icontains=search_query)
        )

    if status_filter == 'available':
        programmers = programmers.filter(is_available=True)
    elif status_filter == 'unavailable':
        programmers = programmers.filter(is_available=False)

    programmers = programmers.annotate(
        total_projects=Count('project'),
        completed_projects=Count('project', filter=Q(project__status='approved'))
    ).order_by('-created_at')

    paginator = Paginator(programmers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_programmers': ProgrammerProfile.objects.count(),
        'available_programmers': ProgrammerProfile.objects.filter(is_available=True).count(),
    }
    return render(request, 'admin/programmer_list.html', context)


@staff_member_required
def programmer_detail(request, programmer_id):
    programmer = get_object_or_404(ProgrammerProfile, id=programmer_id)
    projects = Project.objects.filter(assigned_to=programmer).order_by('-created_at')

    context = {
        'programmer': programmer,
        'projects': projects,
        'total_projects': projects.count(),
        'completed_projects': projects.filter(status='approved').count(),
        'in_progress_projects': projects.filter(status='in_progress').count(),
        'pending_projects': projects.filter(status='assigned').count(),
    }
    return render(request, 'admin/programmer_detail.html', context)


@staff_member_required
def project_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    projects = Project.objects.select_related('assigned_to', 'created_by').all()

    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(assigned_to__full_name__icontains=search_query)
        )

    if status_filter:
        projects = projects.filter(status=status_filter)
    if priority_filter:
        projects = projects.filter(priority=priority_filter)

    projects = projects.order_by('-created_at')

    paginator = Paginator(projects, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    stats = {
        'total_projects': Project.objects.count(),
        'pending_projects': Project.objects.filter(status='pending').count(),
        'assigned_projects': Project.objects.filter(status='assigned').count(),
        'in_progress_projects': Project.objects.filter(status='in_progress').count(),
        'completed_projects': Project.objects.filter(status='completed').count(),
        'approved_projects': Project.objects.filter(status='approved').count(),
    }

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'stats': stats,
    }
    return render(request, 'admin/project_list.html', context)


@staff_member_required
def delete_programmer(request, programmer_id):
    if request.method == 'POST':
        programmer = get_object_or_404(ProgrammerProfile, id=programmer_id)
        user = programmer.user
        programmer.delete()
        user.delete()
        messages.success(request, f'Programmer {programmer.full_name} has been deleted.')
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@staff_member_required
def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project_title = project.title
        project.delete()
        messages.success(request, f'Project "{project_title}" has been deleted.')
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@staff_member_required
def toggle_programmer_availability(request, programmer_id):
    if request.method == 'POST':
        programmer = get_object_or_404(ProgrammerProfile, id=programmer_id)
        programmer.is_available = not programmer.is_available
        programmer.save()
        status = 'available' if programmer.is_available else 'unavailable'
        messages.success(request, f'{programmer.full_name} is now {status}.')
        return JsonResponse({
            'success': True,
            'is_available': programmer.is_available,
            'status': status
        })
    return JsonResponse({'success': False})


@staff_member_required
def project_statistics(request):
    projects_by_status = {}
    for status, _ in Project.STATUS_CHOICES:
        projects_by_status[status] = Project.objects.filter(status=status).count()

    projects_by_priority = {}
    for priority, _ in Project.PRIORITY_CHOICES:
        projects_by_priority[priority] = Project.objects.filter(priority=priority).count()

    recent_projects = Project.objects.select_related('assigned_to', 'created_by').order_by('-created_at')[:5]
    recent_submissions = ProjectSubmission.objects.select_related('project').order_by('-submitted_at')[:5]

    context = {
        'projects_by_status': projects_by_status,
        'projects_by_priority': projects_by_priority,
        'recent_projects': recent_projects,
        'recent_submissions': recent_submissions,
    }
    return render(request, 'admin/statistics.html', context)
