import jwt
import json
from backend.settings import (
    SECRET_KEY
)
from functools import wraps
from django.http import (
    JsonResponse
)
from models.knowledge_base import (
    KnowledgeBase,
)

def access_knowledge_base_allowance(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.user_info.get("user_id", None) if request.user_info else None
            if not user_id:
                raise jwt.exceptions.InvalidTokenError
            try:
                data = json.loads(request.body.decode('utf-8')) if request.body else {} 
            except:
                data = request.POST
            knowledge_base_id = data.get("knowledge_base_id") if data.get("knowledge_base_id", "") != "" else None
            if not knowledge_base_id:
                return JsonResponse({"msg": "KnowledgeBase ID Required"}, status=400)
            knowledge_base = KnowledgeBase.exists_item(KnowledgeBaseID=knowledge_base_id)
            if not knowledge_base:
                raise IndexError
            knowledge_base_user_id = knowledge_base["UserID"]
            if knowledge_base_user_id != user_id:
                return JsonResponse({"msg": "Access Denied"}, status=403)
            setattr(request, 'knowledge_base', knowledge_base)
            return view_func(request, *args, **kwargs)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"msg": "Invalid token"}, status=401)
        except IndexError:
            return JsonResponse({"msg": "KnowledgeBase Not Found"}, status=501)
    
    return wrapper