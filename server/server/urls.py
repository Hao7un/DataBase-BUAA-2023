"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from apis.views import user_views
from apis.views import team_views
from apis.views import recruit_views
from apis.views import project_views

urlpatterns = [
    # 用户系统
    path("register_info", user_views.register_info, name="register_info"),
    path("login_info", user_views.login_info, name="login_info"),
    path("update_user_info", user_views.update_user_info, name="update_user_info"),
    path("change_password", user_views.change_password, name="change_password"),
    path("get_user_info", user_views.get_user_info, name="get_user_info"),
    path("user_get_message", user_views.user_get_message, name="user_get_message"),
    path("user_read_message", user_views.user_read_message, name="user_read_message"),
    path("get_user_avatar",user_views.get_user_avatar,name="get_user_avatar"),
    path("upload_user_avatar",user_views.upload_user_avatar,name="upload_user_avatar"),

    # 团队系统
    path("admin_create_team", team_views.admin_create_team, name="admin_create_team"),
    path("admin_get_all_teams", team_views.admin_get_all_teams, name="admin_get_all_teams"),
    path("admin_get_specific_team_details", team_views.admin_get_specific_team_details,
         name="admin_get_specific_team_details"),
    path("admin_update_team_info", team_views.admin_update_team_info, name="admin_update_team_info"),
    path("admin_remove_team_member", team_views.admin_remove_team_member, name="admin_remove_team_member"),
    path("admin_review_team_application", team_views.admin_review_team_application,
         name="admin_review_team_application"),
    path("admin_get_team_projects", team_views.admin_get_team_projects, name="admin_get_team_projects"),

    path("user_apply_to_join_team", team_views.user_apply_to_join_team, name="user_apply_to_join_team"),
    path("user_get_all_teams_info", team_views.user_get_all_teams_info, name="user_get_all_teams_info"),
    path("user_get_specific_team_details", team_views.user_get_specific_team_details,
         name="user_get_specific_team_details"),
    path("user_get_all_my_teams", team_views.user_get_all_my_teams, name="user_get_all_my_teams"),
    path("get_team_avatar", team_views.get_team_avatar, name="get_team_avatar"),
    path("upload_team_avatar", team_views.upload_team_avatar, name="upload_team_avatar"),

    # 项目系统
    path("admin_create_project", project_views.admin_create_project, name="admin_create_project"),
    path("admin_update_project_info", project_views.admin_update_project_info, name="admin_update_project_info"),
    path("admin_get_project_details", project_views.admin_get_project_details, name="admin_get_project_details"),
    path("admin_create_tutorial", project_views.admin_create_tutorial, name="admin_create_tutorial"),
    path("admin_delete_tutorial", project_views.admin_delete_tutorial, name="admin_delete_tutorial"),
    path("admin_update_tutorial", project_views.admin_update_tutorial, name="admin_update_tutorial"),
    path("admin_reply_question", project_views.admin_reply_question, name="admin_reply_question"),
    path("admin_get_project_recruitments", project_views.admin_get_project_recruitments,
         name="admin_get_project_recruitments"),

    path("user_get_all_projects", project_views.user_get_all_projects, name="user_get_all_projects"),
    path("user_get_favorite_projects", project_views.user_get_favorite_projects, name="user_get_favorite_projects"),
    path("user_toggle_favorite_project", project_views.user_toggle_favorite_project,
         name="user_toggle_favorite_project"),
    path("user_get_specific_project", project_views.user_get_specific_project, name="user_get_specific_project"),
    path("user_post_question", project_views.user_post_question, name="user_post_question"),
    path("get_project_avatar", project_views.get_project_avatar, name="get_project_avatar"),
    path("upload_project_avatar", project_views.upload_project_avatar, name="upload_project_avatar"),

    # 招募系统
    path("admin_create_recruitment", recruit_views.admin_create_recruitment, name="admin_create_recruitment"),
    path("admin_get_recruitment_applicants", recruit_views.admin_get_recruitment_applicants,
         name="admin_get_recruitment_applicants"),
    path("user_get_my_recruitments", recruit_views.user_get_my_recruitments, name="user_get_my_recruitments"),
    path("user_get_recruitment_list", recruit_views.user_get_recruitment_list, name="user_get_recruitment_list"),
    path("user_apply_for_recruitment", recruit_views.user_apply_for_recruitment, name="user_apply_for_recruitment")
]
