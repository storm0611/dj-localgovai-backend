import json
import os
import mimetypes
import uuid
import tempfile
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import (
    JsonResponse,
    StreamingHttpResponse
)
from authentication.decorators import (
    jwt_token_required
)
from models.file_manager import (
    ResourceFolder,
    ResourceFile,
    S3Object
)
from .utils import (
    zip_folder,
)
from .decorators import (
    access_folder_allowance,
    access_file_allowance
)
from backend.settings import (
    TMP_DIR
)

# Create your views here.
class FolderView(View):
    @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            folder_name = data.get("folder_name", "") if data.get("folder_name", "") != "" else None
            knowledge_base_id = data.get("knowledge_base_id", "") if data.get("knowledge_base_id", "") != "" else None
            if not folder_name:
                raise AttributeError
            if ResourceFolder.exists_item(
                UserID=user_id,
                FolderName=folder_name
            ):
               return JsonResponse({"msg": "Folder already exists"}, status=400)
            folder_id = uuid.uuid4().hex
            ResourceFolder.put_item(
                FolderID=folder_id,
                UserID=user_id,
                FolderName=folder_name,
                KnowledgeBaseID=knowledge_base_id,
                FolderPath=f"files/{user_id}/{folder_id}/",
                FolderSize=0
            )
            return JsonResponse({"msg": "Folder is created", "folder_id": folder_id}, status=201)
        except AttributeError:
            return JsonResponse({"msg": "Folder Name required"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
    
    @method_decorator([jwt_token_required, access_folder_allowance])
    def put(self, request):
        try:
            folder = request.folder
            folder_id = folder["FolderID"]
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            folder_name = data.get("folder_name", "") if data.get("folder_name", "") != "" else folder["FolderName"]
            knowledge_base_id = data.get("knowledge_base_id", "") if data.get("knowledge_base_id", "") != "" else folder["KnowledgeBaseID"]
            ResourceFolder.update_item(
                keys={"FolderID": folder_id},
                FolderName=folder_name,
                KnowledgeBaseID=knowledge_base_id
            )
            return JsonResponse({"msg": "Folder Successfully updated", "folder_id": folder_id}, status=200)                
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.GET
            folder_id = data.get("folder_id", "") if data.get("folder_id", "") != "" else None
            knowledge_base_id = data.get("knowledge_base_id", "") if data.get("knowledge_base_id", "") != "" else None
            if folder_id:
                folder = ResourceFolder.exists_item(
                    FolderID=folder_id,
                )
                if not folder:
                    raise IndexError
                return JsonResponse({"msg": "Folder Found", "data": folder}, status=200)
            if knowledge_base_id:                
                folders = ResourceFolder.scan(
                    KnowledgeBaseID=knowledge_base_id
                )
            else:
                folders = ResourceFolder.scan(
                    UserID=user_id
                )
            return JsonResponse({"msg": f"{len(folders)} Folder Found", "data": folders}, status=200)
        except IndexError:
            return JsonResponse({"msg": "Folder Not Found"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
    @method_decorator([jwt_token_required, access_folder_allowance])
    def delete(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            folder = request.folder
            folder_id = folder["FolderID"]
            files = ResourceFile.scan(FolderID=folder_id)
            for file in files:
                s3_obj = S3Object(s3_object_key=file["FilePath"])
                if s3_obj.exists():
                    s3_obj.delete()
                ResourceFile.delete_item(FileID=file["FileID"])
            ResourceFolder.delete_item(
                FolderID=folder_id,
            )
            return JsonResponse({"msg": "Folder Successfully deleted", "folder_id": folder_id}, status=200)                
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
class FolderAllView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            folders = ResourceFolder.get_all()
            return JsonResponse({"data": folders}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

class FolderDownloadView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.GET
            folder_id = data.get("folder_id") if data.get("folder_id", "") != "" else None
            if not folder_id:
                return JsonResponse({"msg": "Folder ID required"}, status=400)
            folder = ResourceFolder.exists_item(FolderID=folder_id)
            if not folder:
                raise IndexError
            folder_name = folder["FolderName"]
            folder_path = folder["FolderPath"]
            temp_dir = os.path.join(TMP_DIR, uuid.uuid4().hex)
            os.mkdir(temp_dir)
            files = ResourceFile.scan(FolderID=folder_id)
            if not len(files):
                return JsonResponse({"msg": "Empty Folder"}, status=400)
            for file in files:
                file_name = file["FileName"]
                file_path = file["FilePath"]
                s3_obj = S3Object(s3_object_key=file_path)
                with open(os.path.join(temp_dir, file_name), 'wb') as file:
                    file.write(s3_obj.get())
            target_file_path = zip_folder(folder_path=temp_dir)
            if os.path.isfile(target_file_path):
                def iterfile():  # 
                    with open(target_file_path, mode="rb") as file_like:  # 
                        yield from file_like
                response = StreamingHttpResponse(streaming_content=iterfile(), content_type="application/zip", status=200)
                response['Content-Disposition'] = f'attachment; filename="{folder_name}.zip"'
                return response
            else:
                return JsonResponse({"msg": "Zip file Not Found"}, status=400)                       
        except IndexError:
            return JsonResponse({"msg": "Folder Not Found"}, status=400)
        except Exception as e:
            return JsonResponse({"msg": str(e)}, status=500)
        
class FileView(View):
    @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.POST
            folder_id = data.get("folder_id", "") if data.get("folder_id", "") != "" else None
            knowledge_base_id = data.get("knowledge_base_id", "") if data.get("knowledge_base_id", "") != "" else None
            files = request.FILES.getlist("files", []) 
            if not len(files):
                raise AttributeError
            file_parent_path = ""
            new_files = []
            duplicated_files = []
            folder = None
            if folder_id:
                folder = ResourceFolder.exists_item(FolderID=folder_id)
                if not folder:
                    raise IndexError
                file_parent_path = folder["FolderPath"]
            else:
                folder_id = None
                file_parent_path = f"files/{user_id}/"
            for file in files:
                rcs_files = ResourceFile.scan(FilePath=f"{file_parent_path}{file.name}")
                s3_obj_file = S3Object(s3_object_key=f"{file_parent_path}{file.name}")
                if len(rcs_files):
                    duplicated_files.append(file.name)
                else:
                    if s3_obj_file.exists():
                        s3_obj_file.delete()
                    s3_obj_file = S3Object(s3_object_key=f"{file_parent_path}{file.name}")
                    s3_obj_file.put(file.read())
                    file_id = ResourceFile.put_item(
                        UserID=user_id,
                        FolderID=folder_id,
                        FileName=file.name,
                        KnowledgeBaseID=knowledge_base_id,
                        FilePath=f"{file_parent_path}{file.name}",
                        FileSize=file.size
                    )
                    if folder:
                        folder_size = int(folder["FolderSize"])
                        ResourceFolder.update_item(
                            keys={"FolderID": folder_id},
                            FolderSize=folder_size + int(file.size)
                        )
                    new_files.append(file.name)
            return JsonResponse({"msg": f"({len(new_files)}) Files are uploaded and ({len(duplicated_files)}) are Duplicated", 
                                 "uploaded_data": new_files, "duplicated_data": duplicated_files}, status=201)
        except IndexError:
            return JsonResponse({"msg": "Folder Not Found"}, status=400)
        except AttributeError:
            return JsonResponse({"msg": "Files required"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
    
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.GET
            file_id = data.get("file_id", "") if data.get("file_id", "") != "" else None
            knowledge_base_id = data.get("knowledge_base_id", "") if data.get("knowledge_base_id", "") != "" else None
            folder_id = data.get("folder_id", "") if data.get("folder_id", "") != "" else None
            if file_id:
                file = ResourceFile.exists_item(FileID=file_id)
                if not file:
                    raise IndexError
                return JsonResponse({"msg": "File Found", "data": file}, status=200)
            elif knowledge_base_id:
                files = ResourceFile.scan(KnowledgeBaseID=knowledge_base_id)
            elif folder_id:
                files = ResourceFile.scan(FolderID=folder_id)
            else:
                files = ResourceFile.scan(UserID=user_id)
            return JsonResponse({"msg": f"{len(files)} Files Found", "data": files}, status=200)
        except IndexError:
            return JsonResponse({"msg": "File not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    @method_decorator([jwt_token_required, access_file_allowance])
    def put(self, request):
        try:
            file = request.file
            file_id = file["FileID"]
            file_path = file["FilePath"]
            file_name = file["FileName"]
            file_size = file["FileSize"]
            s3_obj = S3Object(s3_object_key=file_path)
            if not s3_obj.exists():
                return JsonResponse({"msg": "File does not exists in storage"}, status=400)
            user_id = request.user_info.get("user_id")
            data = json.loads(request.body.decode('utf-8')) if request.body else {} 
            type = data.get("type") if data.get("type", "") != "" else None
            dst_folder_id = data.get("dst_folder_id") if data.get("dst_folder_id", "") != "" else None
            if type == "cp" or type == "mv":
                if not dst_folder_id:
                    return JsonResponse({"msg": "Destination Folder ID Required"}, status=400)
                dst_folder = ResourceFolder.exists_item(FolderID=dst_folder_id)
                if not dst_folder:
                    return JsonResponse({"msg": "Destination Folder Not Found"}, status=400)
                dst_file_path = f"files/{user_id}/{dst_folder_id}/{file_name}"
                dst_file = ResourceFile.exists_item(
                    FilePath = dst_file_path,
                )
                if dst_file:
                    return JsonResponse({"msg": "Duplicated Destination File"}, status=400)
                dst_s3_obj = S3Object(s3_object_key=dst_file_path)
                dst_s3_obj.put(s3_obj.get())
                dst_file_id = ResourceFile.put_item(
                    FileName=file_name,
                    FilePath=dst_file_path,
                    UserID=user_id,
                    KnowledgeBaseID=dst_folder["KnowledgeBaseID"],
                    FileSize=file_size,
                    FolderID=dst_folder_id
                )
                if type == "mv":
                    s3_obj.delete()
                    ResourceFile.delete_item(FileID=file_id)
                    return JsonResponse({"msg": "File moved", "dst_file_id": dst_file_id}, status=200)
                return JsonResponse({"msg": "File copied", "dst_file_id": dst_file_id}, status=200)
            else:
                return JsonResponse({"msg": "Invalid Type"}, status=400)
        except IndexError:
            return JsonResponse({"msg": "ResourceFolder not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    @method_decorator([jwt_token_required, access_file_allowance])
    def delete(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            file = request.file
            file_id = file["FileID"]
            file_path = file["FilePath"]
            s3_obj = S3Object(s3_object_key=file_path)
            if s3_obj.exists():
                s3_obj.delete()
            ResourceFile.delete_item(FileID=file_id)
            return JsonResponse({"msg": "File Successfully deleted", "file_id": file_id}, status=200)
        except IndexError:
            return JsonResponse({"msg": "File not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
class FileAllView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            files = ResourceFile.get_all()
            return JsonResponse({"msg": f"{len(files)} Files Found", "data": files}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
class FileDownloadView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.GET
            file_id = data.get("file_id") if data.get("file_id", "") != "" else None
            if not file_id:
                return JsonResponse({"msg": "File ID required"}, status=400)
            file = ResourceFile.exists_item(FileID=file_id)
            if not file:
                raise IndexError
            file_name = file["FileName"]
            file_path = file["FilePath"]
            temp_dir = TMP_DIR
            s3_obj = S3Object(s3_object_key=file_path)
            temp_path = os.path.join(temp_dir, file_name)
            with open(temp_path, "wb") as fp:
                fp.write(s3_obj.get())
            if os.path.isfile(temp_path):
                def iterfile():  # 
                    with open(temp_path, mode="rb") as file_like:  # 
                        yield from file_like
                response = StreamingHttpResponse(streaming_content=iterfile(), status=200)
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
            else:
                return JsonResponse({"msg": "Temp File Not Found"}, status=400)                       
        except IndexError:
            return JsonResponse({"msg": "File Not Found"}, status=400)
        except Exception as e:
            return JsonResponse({"msg": str(e)}, status=500)
        
class AvatarDownloadView(View):
    def get(self, request, **kwargs):
        try:
            data = kwargs
            file_name = data.get("file_name") if data.get("file_name", "") != "" else None
            if not file_name:
                return JsonResponse({"msg": "File Name required"}, status=400)
            s3_obj = S3Object(s3_object_key=f"avatars/{file_name}")
            if not s3_obj.exists():
                return JsonResponse({"msg": "Not Found"}, status=404)
            temp_dir = TMP_DIR
            temp_path = os.path.join(temp_dir, file_name)
            with open(temp_path, "wb") as fp:
                fp.write(s3_obj.get())
            if os.path.isfile(temp_path):
                def iterfile():  # 
                    with open(temp_path, mode="rb") as file_like:  # 
                        yield from file_like
                response = StreamingHttpResponse(streaming_content=iterfile(), status=200)
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
            else:
                return JsonResponse({"msg": "Temp File Not Found"}, status=400)                       
        except IndexError:
            return JsonResponse({"msg": "File Not Found"}, status=400)
        except Exception as e:
            return JsonResponse({"msg": str(e)}, status=500)