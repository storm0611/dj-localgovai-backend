import jwt
import json
from backend.settings import (
    SECRET_KEY
)
from functools import wraps
from django.http import (
    JsonResponse
)
from models.communication import (
    Channel,
)

def access_channel_allowance(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.user_info.get("user_id", None) if request.user_info else None
            if not user_id:
                raise jwt.exceptions.InvalidTokenError
            data = json.loads(request.body.decode('utf-8')) if request.body else {} 
            channel_id = data.get("channel_id") if data.get("channel_id", "") != "" else None
            if not channel_id:
                return JsonResponse({"msg": "Channel ID Required"}, status=400)
            channel = Channel.exists_item(ChannelID=channel_id)
            if not channel:
                raise IndexError
            owner_id = channel["OwnerID"]
            if owner_id != user_id:
                return JsonResponse({"msg": "Access Denied"}, status=403)
            setattr(request, 'channel', channel)
            return view_func(request, *args, **kwargs)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"msg": "Invalid token"}, status=401)
        except IndexError:
            return JsonResponse({"msg": "Channel Not Found"}, status=501)
    
    return wrapper