import os
import uuid
import json
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator
from django.http import (
    JsonResponse,
)
from models.knowledge_base import (
    KnowledgeBase,
    KnowledgeBaseQuestion,
)
from models.file_manager import (
    ResourceFile,
    S3Object
)
from models.authentication import (
    User
)
from models.user_manager import (
    TeamMember
)
from backend.settings import (
    MEDIA_KNOWLEDGE_BASE,
    STATIC_ROOT,
)
from authentication.decorators import (
    jwt_token_required
)
from .decorators import (
    access_knowledge_base_allowance
)

# Create your views here.
class KnowledgeBaseView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.GET
            knowledge_base_id = data.get("knowledge_base_id") if data.get("knowledge_base_id", "") != "" else None
            if knowledge_base_id:
                knowledge_base = KnowledgeBase.get_item(
                    KnowledgeBaseID=knowledge_base_id
                )
                if not knowledge_base:
                    raise IndexError
                return JsonResponse({"msg": "Knowledge Base Found", "data": knowledge_base}, status=200)
            knowledge_bases = KnowledgeBase.scan(UserID=user_id)
            return JsonResponse({"msg": f"{len(knowledge_bases)} Knowledge Bases Found", "data": knowledge_bases}, status=200)
        except IndexError:
            return JsonResponse({"msg": "Knowledge Base not found."}, status=400)
        except AttributeError:
            return JsonResponse({"msg": "User not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    @method_decorator(jwt_token_required)
    def post(self, request):
        data = request.POST
        knowledge_base_type  = data.get("knowledge_base_type") if data.get("knowledge_base_type", "") != "" else None
        knowledge_base_parent  = data.get("knowledge_base_parent") if data.get("knowledge_base_parent", "") != "" else None
        knowledge_base_name  = data.get("knowledge_base_name") if data.get("knowledge_base_name", "") != "" else None
        knowledge_base_searchable  = bool(data.get("knowledge_base_searchable", True))
        knowledge_base_url  = json.loads(data.get("knowledge_base_url")) if data.get("knowledge_base_url", "") != "" else []
        knowledge_base_phone  = data.get("knowledge_base_phone") if data.get("knowledge_base_phone", "") != "" else None
        project_desc  = data.get("proj_description") if data.get("proj_description", "") != "" else None
        publish_date  = data.get("publish_date") if data.get("publish_date", "") != "" else None
        email_notification = bool(data.get("email_notification", False))
        phone_notification = bool(data.get("phone_notification", False))
        budget = int(data.get("budget", 0))
        budget_usage = data.get("budget_usage") if data.get("budget_usage", "") != "" else None
        allowance_change_budget = bool(data.get("allowance_change_budget", True))
        team_members = json.loads(data.get("team_members")) if data.get("team_members", "") != "" else []
        allowance_invite_by_members = bool(data.get("allowance_invite_by_members", False))
        target_title = data.get("target_title") if data.get("target_title", "") != "" else None
        target_owner_id = data.get("target_owner_id") if data.get("target_owner_id", "") != "" else None
        due_date = data.get("due_date") if data.get("due_date", "") != "" else None
        target_details = data.get("target_details") if data.get("target_details", "") != "" else None
        metrics = json.loads(data.get("metrics")) if data.get("metrics", "") != "" else []
        knowledge_files = request.FILES.getlist("knowledge_files", [])
        try:
            user_id = request.user_info.get("user_id", None)
            knowledge_bases = KnowledgeBase.scan(UserID=user_id, KnowledgeBaseName=knowledge_base_name)
            if len(knowledge_bases):
                return JsonResponse({"msg": "Knowledge Base already exists"}, status=400)
            knowledge_base_id = uuid.uuid4().hex
            if len(knowledge_files):
                # Upload Files
                for file in knowledge_files:
                    file_path = f"files/{user_id}/{file.name}"
                    files = ResourceFile.scan(FilePath=file_path)
                    if not len(files):
                        s3_obj = S3Object(s3_object_key=file_path)
                        s3_obj.put(file.read())
                        ResourceFile.put_item(
                            UserID=user_id,
                            KnowledgeBaseID=knowledge_base_id,
                            FileName=file.name,
                            FilePath=file_path,
                            FileSize=file.size
                        )
            knowledge_base_id = KnowledgeBase.put_item(
                KnowledgeBaseID=knowledge_base_id,
                UserID=user_id,
                KnowledgeBaseType=knowledge_base_type,
                KnowledgeBaseParent=knowledge_base_parent,
                KnowledgeBaseName=knowledge_base_name,
                KnowledgeBaseSearchable=knowledge_base_searchable,
                KnowledgeBasePhone=knowledge_base_phone,
                KnowledgeBaseURL=knowledge_base_url,
                ProjectDescription=project_desc,
                PublishDate=publish_date,
                EmailNotification=email_notification,
                PhoneNotification=phone_notification,
                Budget=budget,
                BudgetUsage=budget_usage,
                AllowanceChangeBudget=allowance_change_budget,
                AllowanceInviteByMembers=allowance_invite_by_members,
                FirstTarget={
                    "Title": target_title,
                    "OwnerID": target_owner_id,
                    "DueDate": due_date,
                    "Details": target_details,
                    "Metrics": metrics
                },
                Setting={
                    "Avatar": "",
                    "BotName": f"{knowledge_base_id}-bot",
                    "BotIntro": "",
                    "PublicSupportChat": "Welcome [Council name]. My name is [Bot name], and I specialise in [Entity name]. You can me ask me questions like [Inherit questions from the team], or any question related to Entity name]. How can I help?",
                    "StaffSupportChat": "Welcome [Council name]. Staff Support Chat. My name is [Bot name], and I specialise in [Entity name]. You can me ask me questions like [Inherit questions from the team], or any question related to Entity name]. How can I help?",
                    "PublicCalls": "Welcome [Council name]. 'Calls are recorded, press 1 if you agree, press 2 if you. do not agree [If they press 2 then we tell them they need to use the chat bot service on the website]. Thank you for confirming your ability for us to record the call. My name is [Bot name], and I specialise in [Entity name]. You can me ask me questions like [Inherit questions from the team], or any question related to Entity name]. How can I help?",
                    "StaffCalls": "Welcome [Council name]. Staff hotline. 'Calls are recorded, press 1 if you agree, press 2 if you. do not agree [If they press 2 then we tell them they need to use the chat bot service on the website]. Thank you for confirming your ability for us to record the call. My name is [Bot name], and I specialise in [Entity name]. You can me ask me questions like [Inherit questions from the team], or any question related to Entity name]. How can I help?"
                }
            )
            return JsonResponse({"msg": "Successfully Created", "knowledge_base_id": knowledge_base_id}, status=201)
        except AttributeError:
            return JsonResponse({"msg": "User not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
    
    @method_decorator([jwt_token_required, access_knowledge_base_allowance])
    def delete(self, request):
        try:
            knowledge_base = request.knowledge_base
            knowledge_base_id = knowledge_base["KnowledgeBaseID"]
            files = ResourceFile.scan(KnowledgeBaseID=knowledge_base_id)
            for file in files:
                s3_obj = S3Object(s3_object_key=file["FilePath"])
                if s3_obj.exists():
                    s3_obj.delete()
                ResourceFile.delete_item(FileID=file["FileID"])
            KnowledgeBase.delete_item(
                KnowledgeBaseID=knowledge_base_id,
            )
            return JsonResponse({"msg": f"Knowledge Base {knowledge_base_id} deleted"}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
class KnowledgeBaseAllView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            knowledge_bases = KnowledgeBase.get_all()
            return JsonResponse({"msg":f"{len(knowledge_bases)} Knowledge Bases Found", "data": knowledge_bases}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

class KnowledgeBaseQuestionView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            data = request.GET
            knowledge_base_question_id = data.get("knowledge_base_question_id") if data.get("knowledge_base_question_id", "") != "" else None
            knowledge_base_id = data.get("knowledge_base_id") if data.get("knowledge_base_id", "") != "" else None
            title = data.get("title") if data.get("title", "") != "" else None
            questions = []
            if knowledge_base_question_id:
                questions = KnowledgeBaseQuestion.scan(
                    KnowledgeBaseQuestionID=knowledge_base_question_id
                )
            if not knowledge_base_id:
                return JsonResponse({"msg": "knowledge_base_id required"}, status=400)
            if not title:
                questions = KnowledgeBaseQuestion.query(
                    KnowledgeBaseID=knowledge_base_id
                )
            else:
                questions = KnowledgeBaseQuestion.scan(
                    KnowledgeBaseID=knowledge_base_id,
                    Title=title
                )
            return JsonResponse({"msg": f"{len(questions)} Questions Found", "data": questions}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)       

    @method_decorator(jwt_token_required)
    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        knowledge_base_id = data.get("knowledge_base_id") if data.get("knowledge_base_id", "") != "" else None
        if not knowledge_base_id:
            return JsonResponse({"msg": "Knowledge Base ID required"}, status=400)
        title = data.get("title") if data.get("title", "") != "" else None
        question = data.get("question") if data.get("question", "") != "" else None
        triggers = data.get("triggers") if data.get("triggers", "") != "" else []
        tags = data.get("tags") if data.get("tags", "") != "" else []
        published = bool(data.get("published", True))
        connected_services = data.get("connected_service") if data.get("connected_service", "") != "" else []
        try:
            knowledge_base_questions = KnowledgeBaseQuestion.scan(
                Title=title,
                KnowledgeBaseID=knowledge_base_id
            )
            if len(knowledge_base_questions):
                return JsonResponse({"msg": "Question already exists"}, status=400)
            question_id = KnowledgeBaseQuestion.put_item(
                Title=title,
                KnowledgeBaseID=knowledge_base_id,
                Question=question,
                Triggers=triggers,
                Tags=tags,
                Published=published,
                ConnectedServices=connected_services
            )
            return JsonResponse({"msg": "Successfully Created", "knowledge_base_question_id": question_id}, status=201)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

class SettingView(View):
    @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.POST
            avatar = request.FILES.get("avatar", None)
            bot_name = data.get("bot_name", "")
            bot_intro = data.get("bot_intro", "") 
            public_support_chat = data.get("public_support_chat", "") 
            staff_support_chat = data.get("staff_support_chat", "") 
            public_calls = data.get("public_calls", "") 
            staff_calls = data.get("staff_calls", "") 
            knowledge_base_id = data.get("knowledge_base_id", "") if data.get("knowledge_base_id", "") != "" else None
            if not knowledge_base_id:
                return JsonResponse({"msg": "Knowledge Base ID required"}, status=400)
            if not KnowledgeBase.exists_knowledge(
                UserID=user_id,
                KnowledgeBaseID=knowledge_base_id
            ):
                return JsonResponse({"msg": "Knowledge Base Not Found"}, status=400)
            knowledge_base = KnowledgeBase.get_knowledgebases(
                KnowledgeBaseID=knowledge_base_id,
                UserID=user_id
            )[0]
            setting = knowledge_base["Setting"]
            if bot_name != "":
                setting["BotName"] = bot_name
            if bot_intro != "":
                setting["BotIntro"] = bot_intro
            if public_support_chat != "":
                setting["PublicSupportChat"] = public_support_chat
            if staff_support_chat != "":
                setting["StaffSupportChat"] = staff_support_chat
            if public_calls != "":
                setting["PublicCalls"] = public_calls
            if staff_calls != "":
                setting["StaffCalls"] = staff_calls
            if avatar:
                if not avatar.content_type.startswith('image'):
                    raise Exception("Invalid Avatar Image file")
                avatar_filename = setting["Avatar"]
                # Upload Avatar
                avatar_path = os.path.join(STATIC_ROOT, avatar_filename)
                if os.path.isfile(avatar_path):
                    os.remove(avatar_path)
                avatar_filename = uuid.uuid4().hex + "." + avatar.name.split(".")[-1]
                file_path = os.path.join(STATIC_ROOT, avatar_filename)
                with open(file_path, "wb") as f:
                    f.write(avatar.read())
                setting["Avatar"] = avatar_filename
            KnowledgeBase.update_knowledgebase(
                knowledge_base_id=knowledge_base_id,
                user_id=user_id,
                Setting=setting
            )
            return JsonResponse({"msg": f"Setting of the Knowledge Base {knowledge_base_id} updated"}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
