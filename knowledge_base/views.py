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
    S3Object
)
from models.authentication import (
    User
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
                return JsonResponse({"msg": "Knowledge Base Found", "data": knowledge_base}, status=200)
            knowledge_bases = KnowledgeBase.scan(UserID=user_id)
            return JsonResponse({"msg": f"{len(knowledge_bases)} Knowledge Bases Found", "data": knowledge_bases}, status=200)
        except AttributeError:
            return JsonResponse({"msg": "UserID not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    @method_decorator(jwt_token_required)
    def post(self, request):
        data = request.POST
        knowledge_base_type  = data.get("knowledge_base_type", None)
        knowledge_base_parent  = data.get("knowledge_base_parent", None)
        knowledge_base_name  = data.get("knowledge_base_name", None)
        # knowledge_base_name = re.sub(r'-+', '-', re.sub(r'[^\w\s-]|(?<=\s)-(?=\s)|_', '-', knowledge_base_name)).strip("-")
        knowledge_base_searchable  = bool(data.get("knowledge_base_searchable", True))
        knowledge_base_phone  = data.get("knowledge_base_phone", None)
        project_desc  = data.get("project_desc", None)
        publish_date  = data.get("publish_date", None)
        email_notification = bool(data.get("email_notification", False))
        phone_notification = bool(data.get("phone_notification", False))
        budget = float(data.get("budget", 0))
        budget_usage = data.get("budget_usage", None)
        allowance_change_budget = bool(data.get("allowance_change_budget", True))
        invitation_link = data.get("invitation_link", None)
        team_members = data.get("team_members", [])
        allowance_invite_by_members = bool(data.get("allowance_invite_by_members", False))
        knowledge_files = request.FILES.getlist("knowledge_files", []) 
        target_title = data.get("target_title", None)
        target_owner_id = data.get("target_owner_id", None)
        due_date = data.get("due_date", None)
        target_details = data.get("target_details", None)
        metrics = data.get("metrics", [])
        try:
            user_id = request.user_info.get("user_id", None)
            knowledge_bases = KnowledgeBase.scan(UserID=user_id, KnowledgeBaseName=knowledge_base_name)
            if len(knowledge_bases):
                return JsonResponse({"msg": "Knowledge Base already exists"}, status=400)
            metric_list = []
            if len(metrics):
                for metric in metrics.split(","):
                    metric_list.append(metric.strip())
            knowledge_base_id = uuid.uuid4().hex
            knowledge_base_id = KnowledgeBase.put_item(
                files=knowledge_files,
                KnowledgeBaseID=knowledge_base_id,
                UserID=user_id,
                KnowledgeBaseType=knowledge_base_type,
                KnowledgeBaseParent=knowledge_base_parent,
                KnowledgeBaseName=knowledge_base_name,
                KnowledgeBaseSearchable=knowledge_base_searchable,
                KnowledgeBasePhone=knowledge_base_phone,
                ProjectDescription=project_desc,
                PublishDate=publish_date,
                EmailNotification=email_notification,
                PhoneNotification=phone_notification,
                Budget=budget,
                BudgetUsage=budget_usage,
                AllowanceChangeBudget=allowance_change_budget,
                InvitationLink=invitation_link,
                TeamMembers=team_members,
                AllowanceInviteByMembers=allowance_invite_by_members,
                TargetTitle=target_title,
                TargetOwnerID=target_owner_id,
                TargetDueDate=due_date,
                TargetDetails=target_details,
                Metrics=metric_list,
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
    
    @method_decorator(jwt_token_required, access_knowledge_base_allowance)
    def delete(self, request):
        try:
            knowledge_base = request.knowledge_base
            knowledge_base_id = knowledge_base["KnowledgeBaseID"]
            KnowledgeBase.delete_item(
                KnowledgeBaseID=knowledge_base_id,
            )
            return JsonResponse({"msg": f"Knowledge Base {knowledge_base_id} deleted"}, status=200)
        except AttributeError:
            return JsonResponse({"msg": "UserID not found."}, status=400)
        except IndexError:
            return JsonResponse({"msg": "UserID not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

class KnowledgeBaseEditView(View):
    @method_decorator(jwt_token_required, access_knowledge_base_allowance)
    def post(self, request):
        data = request.POST
        knowledge_base = request.knowledge_base
        knowledge_base_id = knowledge_base["KnowledgeBaseID"]
        knowledge_base_type  = data.get("knowledge_base_type") if data.get("knowledge_base_type", None) else knowledge_base["KnowledgeBaseType"]
        knowledge_base_parent  = data.get("knowledge_base_parent") if data.get("knowledge_base_parent", None) else knowledge_base["KnowledgeBaseParent"]
        knowledge_base_name  = data.get("knowledge_base_name") if data.get("knowledge_base_name", None) else knowledge_base["KnowledgeBaseName"]
        # knowledge_base_name = re.sub(r'-+', '-', re.sub(r'[^\w\s-]|(?<=\s)-(?=\s)|_', '-', knowledge_base_name)).strip("-")
        knowledge_base_searchable  = bool(data.get("knowledge_base_searchable")) if data.get("knowledge_base_searchable", None) else knowledge_base["KnowledgeBaseSearchable"]
        knowledge_base_phone  = data.get("knowledge_base_phone") if data.get("knowledge_base_phone", None) else knowledge_base["KnowledgeBasePhone"]
        project_desc  = data.get("project_desc") if data.get("project_desc", None) else knowledge_base["ProjectDescription"]
        publish_date  = data.get("publish_date") if data.get("publish_date", None) else knowledge_base["PublishDate"]
        email_notification = bool(data.get("email_notification")) if data.get("email_notification", None) else knowledge_base["EmailNotification"]
        phone_notification = bool(data.get("phone_notification")) if data.get("phone_notification", None) else knowledge_base["PhoneNotification"]
        budget = float(data.get("budget")) if data.get("budget", None) else knowledge_base["Budget"]
        budget_usage = data.get("budget_usage") if data.get("budget_usage", None) else knowledge_base["BudgetUsage"]
        allowance_change_budget = bool(data.get("allowance_change_budget")) if data.get("allowance_change_budget", None) else knowledge_base["AllowanceChangeBudget"]
        invitation_link = data.get("invitation_link") if data.get("invitation_link", None) else knowledge_base["InvitationLink"]
        allowance_invite_by_members = bool(data.get("allowance_invite_by_members")) if data.get("allowance_invite_by_members", None) else knowledge_base["AllowanceInviteByMembers"]
        knowledge_files = request.FILES.getlist("knowledge_files", []) 
        target_title = data.get("target_title") if data.get("target_title", None) else knowledge_base["TargetTitle"]
        target_owner_id = data.get("target_owner_id") if data.get("target_owner_id", None) else knowledge_base["TargetOwnerID"]
        due_date = data.get("due_date") if data.get("due_date", None) else knowledge_base["TargetDueDate"]
        target_details = data.get("target_details") if data.get("target_details", None) else knowledge_base["TargetDetails"]
        metrics = data.get("metrics", [])
        try:
            user_id = request.user_info.get("user_id", None)
            knowledge_bases = KnowledgeBase.scan(UserID=user_id, KnowledgeBaseName=knowledge_base_name)
            if len(knowledge_bases):
                return JsonResponse({"msg": "Knowledge Base already exists"}, status=400)
            metric_list = []
            if len(metrics):
                for metric in metrics.split(","):
                    metric_list.append(metric.strip())
            knowledge_base_id = uuid.uuid4().hex
            knowledge_base_id = KnowledgeBase.put_item(
                files=knowledge_files,
                KnowledgeBaseID=knowledge_base_id,
                UserID=user_id,
                KnowledgeBaseType=knowledge_base_type,
                KnowledgeBaseParent=knowledge_base_parent,
                KnowledgeBaseName=knowledge_base_name,
                KnowledgeBaseSearchable=knowledge_base_searchable,
                KnowledgeBasePhone=knowledge_base_phone,
                ProjectDescription=project_desc,
                PublishDate=publish_date,
                EmailNotification=email_notification,
                PhoneNotification=phone_notification,
                Budget=budget,
                BudgetUsage=budget_usage,
                AllowanceChangeBudget=allowance_change_budget,
                InvitationLink=invitation_link,
                AllowanceInviteByMembers=allowance_invite_by_members,
                TargetTitle=target_title,
                TargetOwnerID=target_owner_id,
                TargetDueDate=due_date,
                TargetDetails=target_details,
                Metrics=metric_list,
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

class KnowledgeBaseAllView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            knowledge_bases = KnowledgeBase.get_all()
            return JsonResponse({"data": knowledge_bases}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

class KnowledgeBaseQuestionView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            data = request.GET
            knowledge_base_question_id = data.get("knowledge_base_question_id", "")
            knowledge_base_id = data.get("knowledge_base_id", "")
            title = data.get("title", "")
            knowledge_base_question_id = knowledge_base_question_id if knowledge_base_question_id != "" else None
            knowledge_base_id = knowledge_base_id if knowledge_base_id != "" else None
            title = title if title != "" else None
            if knowledge_base_question_id:
                questions = KnowledgeBaseQuestion.get_questions(
                    KnowledgeBaseQuestionID=knowledge_base_question_id
                )
                return JsonResponse({"data": questions}, status=200)
            if not knowledge_base_id:
                return JsonResponse({"msg": "knowledge_base_id required"}, status=400)
            if not title:
                questions = KnowledgeBaseQuestion.get_questions(
                    KnowledgeBaseID=knowledge_base_id
                )
                return JsonResponse({"data": questions}, status=200)
            else:
                questions = KnowledgeBaseQuestion.get_questions(
                    KnowledgeBaseID=knowledge_base_id,
                    Title=title
                )
                return JsonResponse({"data": questions}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)       

    @method_decorator(jwt_token_required)
    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        knowledge_base_id = data.get("knowledge_base_id", None)
        if not knowledge_base_id:
            return JsonResponse({"msg": "Knowledge Base ID required"}, status=400)
        title = data.get("title", None)
        question = data.get("question", None)
        triggers = data.get("triggers", None)
        tags = data.get("tags", None)
        published = bool(data.get("published", True))
        connected_services = data.get("connected_service", [])
        try:
            if KnowledgeBaseQuestion.exists_question(
                Title=title,
                KnowledgeBaseID=knowledge_base_id
            ):
                return JsonResponse({"msg": "Question already exists"}, status=400)
            question_id = KnowledgeBaseQuestion.create_question(
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
