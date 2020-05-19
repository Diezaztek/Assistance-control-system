"""attendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from control import views

urlpatterns = [
    #Admin
    path('admin/', admin.site.urls),

    #Login handle
    path('', views.check_assitance, name='check'),
    path('login/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_admin, name='logout_admin'),

    #Progress
    path('progress/<str:id>', views.view_progress, name='progress'),

    #Platform management
    path('admin_check/', views.admin_check, name='admin_check'),
    path('edit/', views.edit_student, name='edit'),
    path('save/', views.save_student_changes, name='save_changes'),
    path('admin_check_in/', views.admin_check_in, name='admin_check_in'),
    path('admin_check_out/', views.admin_check_out, name='admin_check_out'),
    path('summary/', views.view_summary, name='summary')

]
