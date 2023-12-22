from django.urls import path, re_path
from .views import (
    FolderView,
    FolderAllView,
    FileView,
    FileAllView,
    FolderDownloadView,
    FileDownloadView,
    AvatarDownloadView
)

urlpatterns = [
    path('mkdir', FolderView.as_view(), name='make_folder'),
    path('rmdir', FolderView.as_view(), name='delete_folder'),
    path('rem', FolderView.as_view(), name='rename_folder'),
    path('dir', FolderView.as_view(), name='get_folder'),
    path('dir/download', FolderDownloadView.as_view(), name='download_folder'),
    path('dir/all', FolderAllView.as_view(), name='get_all_folders'),
    path('files/upload', FileView.as_view(), name='upload_files'),
    path('files/del', FileView.as_view(), name='delete_files'),
    path('files', FileView.as_view(), name='files'),
    path('files/download', FileDownloadView.as_view(), name='download_files'),
    path('files/all', FileAllView.as_view(), name='get_all_files'),
    path('avatar/<str:file_name>', AvatarDownloadView.as_view(), name='get_avatar'),
]