import json
import jwt
from datetime import datetime
from django.views import View
from django.http import (
    JsonResponse
)
from django.utils.decorators import method_decorator
from backend.settings import (
    SECRET_KEY,
    FRONTEND_HOST
)
from models.authentication import (
    User,
    Org
)
from .decorators import (
    jwt_token_required,
    access_user_allowance
)
from .utils import (
    send_verification_mail,
    urlsafe_base64_decode,
    custom_token_generator
)
from .validators import (
    is_valid_email
)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        email = data.get('email', None)
        password = data.get('password', None)
        if not is_valid_email(email):
            return JsonResponse({"msg": "Incorrect Email"}, status=400)
        try:
            user = User.authenticate(
                email=email,
                password=password
            )
            org = Org.exists_item(OrgID=user["OrgID"])
            if not org:
                raise Exception("Org Not Found")
            if user:
                iat = int(datetime.now().timestamp())
                payload = {
                    'user_id': user.get("UserID"),
                    'iat': iat,
                }
                token = jwt.encode(payload, SECRET_KEY.encode(), algorithm='HS256')
                return JsonResponse({
                    "msg": "Successfully Logged in", 
                    "token": token, 
                    'iat': iat, 
                    "username": user["UserName"], 
                    "email": user["Email"], 
                    "phone_number": user["PhoneNumber"], 
                    "account_type": org["AccountType"],
                    "organization_name": org["OrgName"]
                }, status=200)
            else:
                return JsonResponse({"msg": "Invaild Email or Password"}, status=401)    
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)    

class RegisterView(View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        instance_type = data.get('instance_type', "gov")
        account_type = data.get('account_type', "personal")
        domain_name = data.get('domain_name', None)
        team_size = data.get('team_size', '1-1')
        account_plan = data.get('account_plan', 'Organization')
        organization_name = data.get('organization_name', None)
        organization_description = data.get('organization_description', None)
        organization_type = data.get('organization_type', "Private Limited Company")
        # bussiness_description = data.get('bussiness_description', None)
        contact_email = data.get('contact_email') if data.get('contact_email', "") != "" else None
        first_name = data.get('first_name') if data.get('first_name', "") != "" else None
        last_name = data.get('last_name') if data.get('last_name', "") != "" else None
        username = data.get('username') if data.get('username', "") != "" else None
        email = data.get('email') if data.get('email', "") != "" else None
        password = data.get('password') if data.get('password', "") != "" else None
        phone_number = data.get('phone_number') if data.get('phone_number', "") != "" else None
        if not is_valid_email(email):
            return JsonResponse({"msg": "Incorrect Email"}, status=400)
        if username is None:
            username = email.split("@")[0]
        try:
            users = User.scan(condition_op='or', Email=email, UserName=username)
            if len(users):
                return JsonResponse({"msg": "User already exists"}, status=400)
            org = Org.exists_item(OrgName=organization_name)
            if not org:
                org_id = Org.put_item(
                    InstanceType=instance_type,
                    OrgName=organization_name,
                    Domain=domain_name,
                    AccountType=account_type,
                    Description=organization_description,
                    ContactEmail=contact_email,
                    OrganisationType=organization_type,
                    DomainName=domain_name,
                    TeamSize=team_size,
                    AccountPlan=account_plan
                )
            else:
                org_id = org["OrgID"]
            user_id = User.put_item(
                OrgID=org_id,
                FirstName=first_name,
                LastName=last_name,
                UserName=username,
                Email=email,
                PhoneNumber=phone_number,
                Password=password,
                UserOnLine=False,
                TermsAccepted=True,
            )
            return JsonResponse({"msg": "Successfully Registered", "user_id": user_id}, status=201)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

class UserView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            data = request.GET
            user_id = data.get("user_id") if data.get("user_id", "") != "" else None
            if not user_id:
                user_id = request.user_info.get("user_id", None)
            user = User.exists_item(
                UserID=user_id
            )
            if not user:
                raise IndexError
            org = Org.exists_item(OrgID=user["OrgID"])
            if not org:
                raise Exception("Org Not Found")
            return JsonResponse({"data": user, "org_data": org}, status=200)
        except AttributeError:
            return JsonResponse({"msg": "UserID not found."}, status=400)
        except IndexError:
            return JsonResponse({"msg": "UserID not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
    
    @method_decorator(jwt_token_required)
    def delete(self, request):
        try:
            user_id = request.user_info.get("user_id", None) if request.user_info else None
            user = User.exists_item(
                UserID=user_id
            )
            User.delete_item(UserID=user_id, OrgID=user["OrgID"])
            return JsonResponse({"msg": f"User {user_id} successfully deleted"}, status=200)
        except IndexError:
            return JsonResponse({"msg": "User not found."}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
class UserSearchView(View):
    @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            data = request.GET
            who = data.get("who") if data.get("who", "") != "" else None
            if not who:
                users = User.get_all()
                return JsonResponse({"data": users}, status=200)
            users = User.search(who=who)
            return JsonResponse({"data": users}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

class PasswordResetView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        email = data.get('email', None)
        try:
            user = User.exists_item(Email=email)
            if user:
                host = FRONTEND_HOST
                msg_id = send_verification_mail(host=host, user=user, email_template='password_reset_email_template.html', subject="Password Reset Requested")
                return JsonResponse({"msg": "Sent Successfully", "msg_id": msg_id}, status=200)
            else:
                return JsonResponse({"msg": "Not registered yet", "email": email}, status=400)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
    def get(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64)
        try:
            user = User.exists_item(UserID=uid.decode())
            if not user or not custom_token_generator.check_token(user["UserName"], token):
                return JsonResponse({"msg": "Invalid token", "token": token}, status=400)
            return JsonResponse({"msg": "Confirmed", "user_id": user["UserID"], "org_id": user["OrgID"]}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    def put(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        user_id = data.get('user_id', None)
        org_id = data.get("org_id", None)
        password = data.get('password', None)
        try:
            User.update_item(
                keys={
                    "UserID": user_id,
                    "OrgID": org_id
                },
                Password=password
            )
            return JsonResponse({"msg": "Reset Successfully"}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)