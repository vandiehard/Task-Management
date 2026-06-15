from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LoginView.as_view(template_name='login.html'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # Profile
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/programmers/', views.programmer_list, name='programmer_list'),
    path('manage/programmer/<int:programmer_id>/', views.programmer_detail, name='programmer_detail'),
    path('manage/projects/', views.project_list, name='project_list'),
    path('manage/statistics/', views.project_statistics, name='project_statistics'),

    # Projects
    path('create-project/', views.create_project, name='create_project'),
    path('assign-project/<int:project_id>/', views.assign_project, name='assign_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/start/', views.start_project, name='start_project'),
    path('project/<int:project_id>/submit/', views.submit_project, name='submit_project'),
    path('approve-submission/<int:submission_id>/', views.approve_submission, name='approve_submission'),

    # AJAX
    path('delete-programmer/<int:programmer_id>/', views.delete_programmer, name='delete_programmer'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('toggle-availability/<int:programmer_id>/', views.toggle_programmer_availability, name='toggle_programmer_availability'),
]
