import jwt
import json
from backend.settings import (
    SECRET_KEY
)
from functools import wraps
from django.http import (
    JsonResponse
)
from models.file_manager import (
    ResourceFolder,
    ResourceFile
)

def access_folder_allowance(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.user_info.get("user_id", None) if request.user_info else None
            if not user_id:
                raise jwt.exceptions.InvalidTokenError
            data = json.loads(request.body.decode('utf-8')) if request.body else {} 
            folder_id = data.get("folder_id") if data.get("folder_id", "") != "" else None
            if not folder_id:
                return JsonResponse({"msg": "Folder ID Required"}, status=400)
            folder = ResourceFolder.exists_item(FolderID=folder_id)
            if not folder:
                raise IndexError
            if folder["UserID"] != user_id:
                return JsonResponse({"msg": "Access Denied"}, status=403)
            setattr(request, 'folder', folder)
            return view_func(request, *args, **kwargs)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"msg": "Invalid token"}, status=401)
        except IndexError:
            return JsonResponse({"msg": "Folder Not Found"}, status=501)
    
    return wrapper

def access_file_allowance(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.user_info.get("user_id", None) if request.user_info else None
            if not user_id:
                raise jwt.exceptions.InvalidTokenError
            data = json.loads(request.body.decode('utf-8')) if request.body else {} 
            file_id = data.get("file_id") if data.get("file_id", "") != "" else None
            if not file_id:
                return JsonResponse({"msg": "File ID Required"}, status=400)
            file = ResourceFile.exists_item(FileID=file_id)
            if not file:
                raise IndexError
            if file["UserID"] != user_id:
                return JsonResponse({"msg": "Access Denied"}, status=403)
            setattr(request, 'file', file)
            return view_func(request, *args, **kwargs)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"msg": "Invalid token"}, status=401)
        except IndexError:
            return JsonResponse({"msg": "File Not Found"}, status=501)
    
    return wrapper