from django.urls import path, re_path
from .views import (
    RoleView,
    TeamView,
    TeamMemberView,
    TeamEditView,
    TeamMemberEditView,
    UserPermissionView
)

urlpatterns = [
    path('role', RoleView.as_view(), name='role'),   
    path('team', TeamView.as_view(), name='team'),
    path('team/edit', TeamEditView.as_view(), name='team_edit'),
    path('teammember', TeamMemberView.as_view(), name='teammember'),
    path('teammember/edit', TeamMemberEditView.as_view(), name='teammember_edit'),
    # path('user-permission', UserPermissionView.as_view(), name='user_permission'),
]
