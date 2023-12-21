import jwt
import json
from datetime import datetime
from backend.settings import (
    SECRET_KEY,
    JWT_TOKEN_TIMESTAMP
)
from functools import wraps
from django.http import (
    JsonResponse
)

def get_user_info_from_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY.encode(), algorithms=['HS256'])
        user_id = decoded_token['user_id']
        iat = decoded_token['iat']
        # if int(datetime.now().timestamp()) - iat > JWT_TOKEN_TIMESTAMP:
        #     raise jwt.exceptions.InvalidTokenError("Timeout")
        return {"user_id": user_id, "iat": iat}
    except IndexError:
        raise jwt.exceptions.InvalidTokenError("Invalid token")
    except jwt.exceptions.InvalidTokenError:
        raise jwt.exceptions.InvalidTokenError("Invalid token")

def jwt_token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            auth = request.META.get('HTTP_AUTHORIZATION', '').split(' ')
            token = auth[1] if len(auth) == 2 and auth[0].lower() == 'bearer' else None
            if not token: 
                return JsonResponse({"msg": "Token is not Correct form"}, status=401)
            user_info = get_user_info_from_token(token)
            if not user_info or not user_info.get("user_id", None):
                return JsonResponse({"msg": "Invalid token"}, status=401)
            setattr(request, 'user_info', user_info)
            return view_func(request, *args, **kwargs)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"msg": "Invalid token"}, status=401)
    
    return wrapper

def access_user_allowance(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.user_info.get("user_id", None) if request.user_info else None
            if not user_id:
                raise jwt.exceptions.InvalidTokenError
            data = json.loads(request.body.decode('utf-8')) if request.body else {} 
            user_id1 = data.get("user_id") if data.get("user_id", "") != "" else None
            if not user_id1:
                return JsonResponse({"msg": "User ID Required"}, status=400)
            if user_id1 != user_id:
                return JsonResponse({"msg": "Access Denied"}, status=403)
            return view_func(request, *args, **kwargs)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"msg": "Invalid token"}, status=401)
        except IndexError:
            return JsonResponse({"msg": "Room Not Found"}, status=501)
    
    return wrapper