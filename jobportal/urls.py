"""jobportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from app1.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name="index"),
    path('contact', contact,name="contact"),
    path('admin_login',admin_login,name="admin_login"),
    path('admin_home',admin_home,name="admin_home"),
    path('admin_logout',admin_logout,name="admin_logout"),
    path('change_password_admin',change_password_admin,name="change_password_admin"),
    path('user_login',user_login,name="user_login"),
    path('change_password_user',change_password_user,name="change_password_user"),
    path('recruiter_login',recruiter_login,name="recruiter_login"),
    path('recruiter_logout',recruiter_logout,name="recruiter_logout"),
    path('recruiter_home',recruiter_home,name="recruiter_home"),
    path('change_password_recruiter',change_password_recruiter,name="change_password_recruiter"),
    path('user_signup',user_signup,name="user_signup"),
    path('recruiter_signup', recruiter_signup, name="recruiter_signup"),
    path('user_login',user_login,name="user_login"),
    path('user_home',user_home,name="user_home"),
    path('user_logout',user_logout,name="user_logout"),
    path('view_users',view_users,name="view_users"),
    path('delete_user/<int:pid>', delete_user, name="delete_user"),
    path('recruiter_pending', recruiter_pending, name="recruiter_pending"),
    path('change_status/<int:pid>', change_status, name="change_status"),
    path('recruiter_accepted', recruiter_accepted, name="recruiter_accepted"),
    path('recruiter_rejected', recruiter_rejected, name="recruiter_rejected"),
    path('recruiter_all', recruiter_all, name="recruiter_all"),
    path('candidates_applied', candidates_applied, name="candidates_applied"),
    path('add_job', add_job, name="add_job"),
    path('job_list', job_list, name="job_list"),
    path('edit_job/<int:pid>', edit_job, name="edit_job"),
    path('latest_jobs',latest_jobs,name="latest_jobs"),
    path('user_job_list',user_job_list,name="user_job_list"),
    path('job_detail/<int:pid>',job_detail,name="job_detail"),
    path('apply_for_job/<int:pid>',apply_for_job,name="apply_for_job"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
