import jwt
import json
from functools import wraps
from django.http import (
    JsonResponse
)
from models.user_manager import (
    Team,
    TeamMember
)

def access_team_allowance(view_func):
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
            team_id = data.get("team_id") if data.get("team_id", "") != "" else None
            if not team_id:
                return JsonResponse({"msg": "Team ID Required"}, status=400)
            team = Team.exists_item(TeamID=team_id)
            if not team:
                raise IndexError
            admin_id = team["AdminID"]
            if admin_id != user_id:
                return JsonResponse({"msg": "Access Denied"}, status=403)
            setattr(request, 'team', team)
            return view_func(request, *args, **kwargs)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"msg": "Invalid token"}, status=401)
        except IndexError:
            return JsonResponse({"msg": "Team Not Found"}, status=501)
    
    return wrapper

def access_teammember_allowance(view_func):
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
            team_member_id = data.get("team_member_id") if data.get("team_member_id", "") != "" else None
            if not team_member_id:
                return JsonResponse({"msg": "TeamMember ID Required"}, status=400)
            team_member = TeamMember.exists_item(TeamMemberID=team_member_id)
            if not team_member:
                raise IndexError
            team = Team.exists_item(TeamID=team_member["TeamID"])
            if not team:
                raise IndexError
            admin_id = team["AdminID"]
            if admin_id == user_id or user_id == team_member["UserID"]:
                setattr(request, 'team_member', team_member)
                return view_func(request, *args, **kwargs)    
            return JsonResponse({"msg": "Access Denied"}, status=403)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"msg": "Invalid token"}, status=401)
        except IndexError:
            return JsonResponse({"msg": "Team or TeamMember Not Found"}, status=501)
    
    return wrapper
