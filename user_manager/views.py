import json
from datetime import datetime
import uuid
from django.views import View
from django.utils.decorators import method_decorator
from utils.aws_s3 import S3Object
from django.http import (
    JsonResponse,
)
from authentication.decorators import (
    jwt_token_required
)
from models.authentication import (
    User
)
from models.user_manager import (
    Role,
    Team,
    TeamMember
)
from .decorators import (
    access_team_allowance,
    access_teammember_allowance
)
# Create your views here.
        
class RoleView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.GET
            role_id = data.get("role_id") if data.get("role_id", "") != "" else None
            if role_id:
                role = Role.exists_item(RoleID=role_id)
                if not role:
                    raise IndexError
                return JsonResponse({"data": role}, status=200)    
            else:
                roles = Role.get_all()
            return JsonResponse({"data": roles}, status=200)
        except IndexError:
            return JsonResponse({"msg": "Role Not Found"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
    @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            role_name = data.get("role_name") if data.get("role_name", "") != "" else None
            role_desc = data.get("role_desc") if data.get("role_desc", "") != "" else None
            if not role_name:
                return JsonResponse({"msg": "Role Name Required"}, status=400)
            role = Role.exists_item(RoleName=role_name)
            if role:
                return JsonResponse({"msg": "Role Already Exists"}, status=400)
            role_id = Role.put_item(
                RoleName=role_name,
                RoleDescription=role_desc
            )
            return JsonResponse({"msg": "Role Successfully created", "role_id": role_id}, status=201)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

class TeamView(View):
    @method_decorator(jwt_token_required)
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user_info.get("user_id")
            data = request.GET
            team_id = data.get("team_id") if data.get("team_id", "") != "" else None
            if not team_id:
                teams = Team.get_all()
                return JsonResponse({"msg": f"{len(teams)} Teams Found", "teams": teams}, status=200)
            else:
                team = Team.get_item(TeamID=team_id)
                return JsonResponse({"msg": "Team Found", "team": team}, status=200)
        except AttributeError:
            return JsonResponse({"msg": "User Info Not Matched"}, status=400)
        except IndexError:
            return JsonResponse({"msg": "User Not Found"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            data = request.POST
            admin_name = data.get("admin_name", "")
            admin_avatar = request.FILES.get("admin_avatar", None)
            admin_email = data.get("admin_email", "")
            team_name = data.get("team_name") if data.get("team_name", "") != "" else None
            knowledge_base_id = data.get("knowledge_base_id") if data.get("knowledge_base_id", "") != "" else None
            if not team_name:
                return JsonResponse({"msg": "Team Name required"}, status=400)
            team = Team.exists_item(TeamName=team_name)
            if team:
                return JsonResponse({"msg": "Team already Exists"}, status=400)
            admin = User.exists_item(Email=admin_email)
            if not admin:
                raise IndexError
            if admin["FirstName"] not in admin_name or admin["LastName"] not in admin_name:
                raise AttributeError
            admin_id = admin["UserID"]
            avatar_filename = ""
            if admin_avatar:
                if not admin_avatar.content_type.startswith('image'):
                    raise Exception("Invalid Avatar Image file")
                # avatar_filename = admin_avatar.name
                avatar_filename = uuid.uuid4().hex + "." + admin_avatar.name.split(".")[-1]
                # with open(os.path.join(TMP_DIR, avatar_filename), 'wb') as fp:
                #     fp.write(admin_avatar.read())
                #     fp.close()
                s3_object = S3Object(s3_object_key=f"avatars/{avatar_filename}")
                s3_object.put(admin_avatar.read())
            team_id = Team.put_item(
                KnowledgeBaseID=knowledge_base_id,
                TeamName=team_name,
                AdminID=admin_id,
                AdminName=admin_name,
                AdminEmail=admin_email,
                AdminAvatar=avatar_filename,
                NmberOfMemebers=0
            )
            return JsonResponse({"msg": "Successfully Created", "team_id": team_id}, status=201)
        except AttributeError:
            return JsonResponse({"msg": "Admin User Info Not Matched"}, status=400)
        except IndexError:
            return JsonResponse({"msg": "Admin User Not Found, incorrect Email address"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
    @method_decorator([jwt_token_required, access_team_allowance])
    def delete(self, request):
        try:
            team = request.team
            team_id = team["TeamID"]           
            s3_object = S3Object(s3_object_key=f"avatars/{team['AdminAvatar']}")
            s3_object.delete()
            team_members = TeamMember.scan(TeamID=team_id)
            for team_member in team_members:
                TeamMember.delete_item(TeamMemberID=team_member["TeamMemberID"])
            Team.delete_item(
                TeamID=team_id
            )
            return JsonResponse({"msg": "Successfully Deleted", "team_id": team_id}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err.args)}, status=500)

class TeamEditView(View):        
    @method_decorator([jwt_token_required, access_team_allowance])
    def post(self, request):
        try:
            data = request.POST
            team = request.team
            team_id = team["TeamID"]
            knowledge_base_id = data.get("knowledge_base_id") if data.get("knowledge_base_id", "") != "" else team["KnowledgeBaseID"]
            team_name = data.get("team_name") if data.get("team_name", "") != "" else team["TeamName"]
            admin_name = data.get("admin_name") if data.get("admin_name", "") != "" else team["AdminName"]
            admin_email = data.get("admin_email") if data.get("admin_email", "") != "" else team["AdminEmail"]
            admin_avatar = request.FILES.get("admin_avatar", None)
            avatar_filename = team["AdminAvatar"]
            admin = User.exists_item(Email=admin_email)
            if not admin:
                raise IndexError
            if admin["FirstName"] not in admin_name or admin["LastName"] not in admin_name:
                raise AttributeError
            admin_id = admin["UserID"]
            if admin_avatar:
                if not admin_avatar.content_type.startswith('image'):
                    raise Exception("Invalid Avatar Image file")
                if avatar_filename != "":
                    s3_object = S3Object(s3_object_key=f"avatars/{avatar_filename}")
                    s3_object.delete()
                # avatar_filename = admin_avatar.name
                avatar_filename = uuid.uuid4().hex + "." + admin_avatar.name.split(".")[-1]
                # with open(os.path.join(TMP_DIR, avatar_filename), 'wb') as fp:
                #     fp.write(admin_avatar.read())
                #     fp.close()
                s3_object = S3Object(s3_object_key=f"avatars/{avatar_filename}")
                s3_object.put(admin_avatar.read())
            Team.update_item(
                keys={"TeamID": team_id},
                KnowledgeBaseID=knowledge_base_id,
                TeamName=team_name,
                AdminID=admin_id,
                AdminName=admin_name,
                AdminEmail=admin_email,
                AdminAvatar=avatar_filename,
            )
            return JsonResponse({"msg": "Successfully Updated", "team_id": team_id}, status=200)
        except AttributeError:
            return JsonResponse({"msg": "Admin User Info Not Matched"}, status=400)
        except IndexError:
            return JsonResponse({"msg": "Admin User Not Found, incorrect Email Address"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
  
class TeamMemberView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            user_id = request.user_info.get("user_id", None)
            data = request.GET
            team_member_id = data.get("team_member_id") if data.get("team_member_id", "") != "" else None
            team_id = data.get("team_id") if data.get("team_id", "") != "" else None
            if team_member_id:
                team_member = TeamMember.get_item(TeamMemberID=team_member_id)
                return JsonResponse({"msg": "TeamMember Found", "data": team_member}, status=200)        
            if team_id:
                team_members = TeamMember.scan(TeamID=team_id)
                return JsonResponse({"msg": f"{len(team_members)} TeamMembers Found", "data": team_members}, status=200)        
            team_members = TeamMember.get_all()
            return JsonResponse({"msg": f"{len(team_members)} TeamMembers Found", "data": team_members}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            data = request.POST
            full_name = data.get("full_name", "")
            email = data.get("email", "")
            role_id = data.get("role_id") if data.get("role_id", "") != "" else None
            team_id = data.get("team_id") if data.get("team_id", "") != "" else None
            avatar = request.FILES.get("avatar", None)
            if not team_id or not role_id:
                return JsonResponse({"msg": "Team ID and Role ID Required"}, status=400)
            team = Team.exists_item(TeamID=team_id)
            if not team:
                return JsonResponse({"msg": "Team Not Found"}, status=400)
            user = User.exists_item(Email=email)
            if not user:
                raise IndexError
            if user["FirstName"] not in full_name or user["LastName"] not in full_name:
                raise AttributeError
            user_id = user["UserID"]
            org_id = user["OrgID"]
            avatar_filename = ""
            if avatar:
                if not avatar.content_type.startswith('image'):
                    raise Exception("Invalid Avatar Image file")
                # avatar_filename = avatar.name
                avatar_filename = uuid.uuid4().hex + "." + avatar.name.split(".")[-1]
                # with open(os.path.join(TMP_DIR, avatar_filename), 'wb') as fp:
                #     fp.write(avatar.read())
                #     fp.close()
                s3_object = S3Object(s3_object_key=f"avatars/{avatar_filename}")
                s3_object.put(avatar.read())
            teammember = TeamMember.exists_item(UserID=user_id)
            if teammember:
                return JsonResponse({"msg": "Member Already Exists in Team"}, status=400)
            teammember_id = TeamMember.put_item(
                TeamID=team_id,
                OrgID=org_id,
                UserID=user_id,
                RoleID=role_id,
                FullName=full_name,
                Email=email,
                Avatar=avatar_filename,
                MemberStatus="Pending",
                Amount=0
            )
            cnt_member = int(team["NmberOfMemebers"]) + 1
            Team.update_item(
                keys={"TeamID": team_id},
                NmberOfMemebers=str(cnt_member)
            )
            return JsonResponse({"msg": "Successfully Created", "teammember_id": teammember_id}, status=201)
        except AttributeError:
            return JsonResponse({"msg": "User Info Not Matched"}, status=400)
        except IndexError:
            return JsonResponse({"msg": "User Not Found, incorrect Email address"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
    @method_decorator([jwt_token_required, access_team_allowance])
    def delete(self, request):
        try:
            team = request.team
            team_id = team["TeamID"]           
            data = json.loads(request.body.decode('utf-8')) if request.body else {} 
            team_member_id = data.get("team_member_id") if data.get("team_member_id", "") != "" else None
            if not team_member_id:
                raise IndexError
            team_member = TeamMember.get_item(TeamMemberID=team_member_id)
            if not team_member:
                raise IndexError
            s3_object = S3Object(s3_object_key=f"avatars/{team_member['Avatar']}")
            s3_object.delete()
            TeamMember.delete_item(TeamMemberID=team_member_id)
            cnt_member = int(team["NmberOfMemebers"]) - 1
            Team.update_item(
                keys={"TeamID": team_id},
                NmberOfMemebers=str(cnt_member)
            )
            return JsonResponse({"msg": "Successfully Deleted", "team_member_id": team_member_id}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err.args)}, status=500)

class TeamMemberEditView(View):        
    @method_decorator([jwt_token_required, access_teammember_allowance])
    def post(self, request):
        try:
            data = request.POST
            team_member = request.team_member
            full_name = data.get("full_name") if data.get("full_name", "") != "" else team_member["FullName"]
            role_id = data.get("role_id") if data.get("role_id", "") != "" else team_member["RoleID"]
            # team_id = data.get("team_id") if data.get("team_id", "") != "" else team_member["TeamID"]
            status = data.get("status") if data.get("status", "") != "" else team_member["MemberStatus"]
            amount = float(data.get("amount")) if data.get("amount", 0) else team_member["Amount"]
            avatar = request.FILES.get("avatar", None)
            avatar_filename = team_member["Avatar"]
            user = User.exists_item(Email=team_member["Email"])
            if not user:
                raise IndexError
            if user["FirstName"] not in full_name or user["LastName"] not in full_name:
                raise AttributeError
            if avatar:
                if not avatar.content_type.startswith('image'):
                    raise Exception("Invalid Avatar Image file")
                if avatar_filename != "":
                    s3_object = S3Object(s3_object_key=f"avatars/{avatar_filename}")
                    s3_object.delete()
                # avatar_filename = avatar.name
                avatar_filename = uuid.uuid4().hex + "." + avatar.name.split(".")[-1]
                # with open(os.path.join(TMP_DIR, avatar_filename), 'wb') as fp:
                #     fp.write(avatar.read())
                #     fp.close()
                s3_object = S3Object(s3_object_key=f"avatars/{avatar_filename}")
                s3_object.put(avatar.read())
            TeamMember.update_item(
                keys={"TeamMemberID": team_member["TeamMemberID"]},
                # TeamID=team_id,
                RoleID=role_id,
                FullName=full_name,
                Avatar=avatar_filename,
                MemberStatus=status,
                Amount=amount
            )
            return JsonResponse({"msg": "Successfully Created", "teammember_id": team_member["TeamMemberID"]}, status=200)
        except AttributeError:
            return JsonResponse({"msg": "User Info Not Matched"}, status=400)
        except IndexError:
            return JsonResponse({"msg": "User Not Found, incorrect Email address"}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)