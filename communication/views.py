import os
import json
from django.http import (
    JsonResponse,
    StreamingHttpResponse
)
from django.views import View
from django.utils.decorators import method_decorator
from azure.core.messaging import (
    CloudEvent
)
from azure.eventgrid import (
    EventGridEvent
)
from .utils import (
    cognitive_service,
    audio_processor,
    communication_call_automation_service,
    communication_chat_bot_service,
    communication_chat_service,
    communication_phone_number_service,
    twilio_service,
    DtmfTone
)
from authentication.decorators import (
    jwt_token_required
)
from .decorators import (
    access_channel_allowance
)
from models.authentication import (
    User
)
from models.communication import (
    ChatMessage,
    Channel
)

# Create your views here.

class SpeechToTextView(View):
    # @method_decorator(jwt_token_required)
    def post(self, request):
        audio_file = request.FILES.get("audio", None)
        try:
            file_path = audio_processor.export_to_wav(audio_file)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=400)
        try:
            result = cognitive_service.speech_to_text_from_file(file_path)
            os.remove(file_path)
            # with open(os.path.splitext(file_path)[0] + ".txt", "w") as file:
            #     file.write(result)
            return JsonResponse({"msg": result}, status=200)  
        except Exception as err:
            os.remove(file_path)
            return JsonResponse({"msg": str(err)}, status=500)  
        
class TextToSpeechView(View):
    # @method_decorator(jwt_token_required)
    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        text = data.get("text", "")
        try:
            stream, file_path = cognitive_service.text_to_speech_file(text=text)
            # file = open(file_path, 'rb')
            # return FileResponse(file, status=200)
            # byte_stream = io.BytesIO()
    
            # for chunk in stream:
            #     byte_stream.write(chunk)
            
            # byte_stream.seek(0)
            # bytes_data = byte_stream.read()

            def iterfile():  # 
                with open(file_path, mode="rb") as file_like:  # 
                    yield from file_like
        
            return StreamingHttpResponse(streaming_content=iterfile(), content_type="audio/wav", status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
class SendMessageBotView(View):
    # @method_decorator(jwt_token_required)
    def post(self, request):
        # user_id = request.user_info.get("user_id", None)
        # if user_id is None:
        #     return JsonResponse({"msg": "Invalid Authentiation"}, status=421)
        # try:
        #     user = User.get_users(
        #         UserID=user_id
        #     )[0]
        # except Exception as err:
        #     return JsonResponse({"msg": str(err)}, status=500)
        # else:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            message_content = data.get("message_content", None)
            # sender = data.get("sender", user["UserName"])
            sender = data.get("sender", "Unknown User")
            try:
                message_id = communication_chat_bot_service.send_message_to_bot(message_content=message_content, sender=sender)
                messages = communication_chat_bot_service.get_messages_from_bot()
                while messages[0]["id"] <= message_id:
                    messages = communication_chat_bot_service.get_messages_from_bot()
                return JsonResponse({"req_msg": messages[1], "res_msg": messages[0]}, status=200)
            except Exception as err:
                return JsonResponse({"msg": str(err)}, status=400)

class PhoneNumberView(View):
    # @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            data = request.GET
            phone_number = data.get("phone_number", "")
            phone_number = phone_number if phone_number != "" else None
            if not phone_number:
                phone_numbers = communication_phone_number_service.get_available_phone_numbers(country_code="US").phone_numbers
                res_data = []
                for phone_number in phone_numbers:
                    operator_infomation = communication_phone_number_service.get_operator_information(phone_number)
                    res_data.append({
                        "phone_number": operator_infomation.phone_number,
                        "international_format": operator_infomation.additional_properties.get("internationalFormat", None),
                        "national_format": operator_infomation.additional_properties.get("nationalFormat", None),
                        "number_type": operator_infomation.number_type,
                        "operator_details": operator_infomation.operator_details.serialize()
                    })
                return JsonResponse({"results": res_data}, status=200)
            else:
                operator_infomation = communication_phone_number_service.get_operator_information(phone_number)
                res_data = {
                    "phone_number": operator_infomation.phone_number,
                    "international_format": operator_infomation.additional_properties.get("internationalFormat", None),
                    "national_format": operator_infomation.additional_properties.get("nationalFormat", None),
                    "number_type": operator_infomation.number_type,
                    "operator_details": operator_infomation.operator_details.serialize()
                }
                return JsonResponse({"results": [res_data]}, status=200)
        except Exception as err:
            print(err)
            return JsonResponse({"msg": "Failed"}, status=500)

    # @method_decorator(jwt_token_required)
    # def post(self, request):
    #     # data = json.loads(request.body.decode('utf-8')) if request.body else {}
    #     try:
    #         communication_phone_number_service.update_phone_number_capabilities(communication_phone_number_service.phone_number, None)
    #         return JsonResponse({"msg": "Updated capabilities"}, status=200)
    #     except Exception as err:
    #         print(err)
    #         return JsonResponse({"msg": "Failed"}, status=500)
        
class TwilioSendMessageView(View):

    @method_decorator(jwt_token_required)
    def post(self, request):
        msg_id = twilio_service.send_sms()
        if msg_id:
            return JsonResponse({"msg": "Message Sent", "msg_id": msg_id}, status=200)
        return JsonResponse({"msg": "Failed"}, status=500)
        
class CallAutomationView(View):
    
    # @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            call_connection_id = communication_call_automation_service.make_outbound_call()
            return JsonResponse({"msg": "Call Connection Created", "conn_id": call_connection_id}, status=201)
        except Exception as err:
            print(err)
            return JsonResponse({"msg": "Error"}, status=500)
    
    # @method_decorator(jwt_token_required)
    def get(self, request):
        try:
            data = request.GET
            call_connection_id = data.get("call_connection_id", None)
            if not call_connection_id:
                return JsonResponse({"msg": "Invaild Connection ID"}, status=400)
            call_connection_client = communication_call_automation_service.get_call_connection(call_connection_id=call_connection_id)
            call_connection_properties = call_connection_client.get_call_properties()
            res_data = {
                call_connection_properties.call_connection_id,
                call_connection_properties.answered_by,
                call_connection_properties.call_connection_state,
                call_connection_properties.callback_url,
                call_connection_properties.correlation_id,
                call_connection_properties.server_call_id,
                call_connection_properties.source,
                call_connection_properties.source_caller_id_number,
                call_connection_properties.source_display_name,
                call_connection_properties.targets
            }
            return JsonResponse({"properties": res_data}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
    
class CallAutomationHangUpView(View):
    # @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            call_connection_id = data.get("call_connection_id", None)
            if not call_connection_id:
                return JsonResponse({"msg": "Invaild Connection ID"}, status=400)
            communication_call_automation_service.hangup(hangout_call_connection_id=call_connection_id)
            return JsonResponse({"msg": "Missed Call"}, status=200)
        except Exception as err:
            print(err)
            return JsonResponse({"msg": "Error"}, status=500)

class CallAutomationCallBacksView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        if not isinstance(data, list):
            event = EventGridEvent.from_dict(data)
            print("EventGridEvent", event)
            event_type = event.additional_properties["type"]
            print(f"{event_type} event received")

            if event_type == "Microsoft.Communication.IncomingCall":
                correlation_id = event.data['correlationId']
                incoming_call_context = event.data['incomingCallContext']
                # print(f"Reject the call: correlationId: {call_connection_id}")
                # communication_call_automation_service.reject_call(incoming_call_context=incoming_call_context)
                print(f"Answer the call: correlationId: {correlation_id}")
                communication_call_automation_service.answer_call(incoming_call_context=incoming_call_context)
        else:
            for event_dict in json.loads(request.body.decode('utf-8')):
                # Parsing callback events
                event = CloudEvent.from_dict(event_dict)
                print("CloudEvent", event)
                event_type = event.type
                print(f"{event_type} event received")

                if event_type == "Microsoft.Communication.CallConnected":
                    call_connection_id = event.data['callConnectionId']
                    print(f"Call is connected: callConnectionId: {call_connection_id}")
                    participants = communication_call_automation_service.get_call_connection(call_connection_id=call_connection_id).list_participants()
                    target_phone = None
                    for participant in participants:
                        # print(type(participant.identifier.raw_id), participant.identifier.raw_id)
                        # print(type(participant.identifier.kind), participant.identifier.kind)
                        if not "communicationUser" in participant.identifier.kind:
                            print(f"Participant: {participant.identifier}")
                            if "phoneNumber" in participant.identifier.kind:
                                target_phone = participant.identifier.phone_number.value
                    print("target_phone: ", target_phone)
                    print("Starting recording")
                    recording_id = communication_call_automation_service.start_recording(event.data['serverCallId'], target_phone_number=target_phone)
                    communication_call_automation_service.recording_ids.append({
                        "call_connection_id": call_connection_id,
                        "recording_id": recording_id
                    })
                    print("Starting recognize")
                    communication_call_automation_service.start_recognize(call_connection_id=call_connection_id, target_phone_number=target_phone)

                elif event_type == "Microsoft.Communication.CallDisconnected":
                    call_connection_id = event.data['callConnectionId']
                    print(f"Call is disconnected: callConnectionId: {call_connection_id}")
                
                elif event_type == "Microsoft.Communication.ParticipantsUpdated":
                    call_connection_id = event.data['callConnectionId']
                    print(f"Call is disconnected: callConnectionId: {call_connection_id}")

                elif event_type == "Microsoft.Communication.RecognizeCompleted":
                    call_connection_id = event.data['callConnectionId']
                    selected_tone = event.data['dtmfResult']['tones'][0]
                    print(f"Received DTMF tone {selected_tone}")
                    communication_call_automation_service.play_media_by_tone(call_connection_id=call_connection_id, tone=selected_tone)                

                elif event_type == "Microsoft.Communication.RecognizeFailed":
                    call_connection_id = event.data['callConnectionId']
                    print("Failed to recognize tone")
                    communication_call_automation_service.play_media_by_tone(call_connection_id=call_connection_id, tone=DtmfTone.ZERO)

                elif event_type in ["Microsoft.Communication.PlayCompleted", "Microsoft.Communication.PlayFailed"]:
                    print("Terminating call")
                    call_connection_id = event.data['callConnectionId']
                    recording_id = None
                    for id in communication_call_automation_service.recording_ids:
                        if id["call_connection_id"] == call_connection_id:
                            recording_id = id["recording_id"]
                    communication_call_automation_service.hangup(recording_id=recording_id, hangout_call_connection_id=call_connection_id)

        return JsonResponse({"msg": "Success"}, status=200)            
    
    def options(self, request):
        response = JsonResponse({})
        print(request.headers)
        return response
    
class RecodingStateCallBacksView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        print("Recording State Data: ", data)
        return JsonResponse({})
    
class ChannelView(View):
    @method_decorator(jwt_token_required)
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user_info.get("user_id")
            data = kwargs
            channel_id = data.get("channel_id") if data.get("channel_id", "") != "" else None
            if channel_id:
                chat_channels = Channel.exists_item(
                    ChannelID=channel_id
                )
            else:
                member_id = data.get("member_id") if data.get("member_id", "") != "" else None
                members = []
                members.append(user_id)
                if member_id:
                    members.append(member_id)
                chat_channels = Channel.scan_contains_members(
                    members=members
                )
            return JsonResponse({"msg": f"{len(chat_channels)} Channels Found", "channels": chat_channels}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)

    @method_decorator(jwt_token_required)
    def post(self, request):
        try:
            user_id = request.user_info.get("user_id")
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            member_id = data.get("member_id") if data.get("member_id", "") != "" else None
            if not member_id or member_id == user_id:
                return JsonResponse({"msg": "Member Required"}, status=400)
            members = [user_id, member_id]
            chat_channels = Channel.scan_contains_members(
                members=members
            )
            if len(chat_channels):
                return JsonResponse({"msg": "Already Exists", "chat_channel": chat_channels}, status=409)
            channel_id = Channel.put_item(
                Members=members,
                OwnerID=user_id
            )
            return JsonResponse({"msg": "Successfully Created", "channel_id": channel_id}, status=201)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
    @method_decorator([jwt_token_required, access_channel_allowance])
    def put(self, request):
        try:
            data = json.loads(request.body.decode('utf-8')) if request.body else {} 
            type = data.get("type") if data.get("type", "") != "" else None
            member_id = data.get("member_id") if data.get("member_id", "") != "" else None
            new_name = data.get("new_name") if data.get("new_name", "") != "" else None
            channel = request.channel
            channel_id = channel["ChannelID"]
            members: list = channel["Members"]
            channel_name = channel["ChannelName"]
            if "rm" in type or "add" in type:
                if not member_id:
                    return JsonResponse({"msg": "Member ID required in this method"}, status=400)
                elif "rm" in type:
                    if member_id in members:
                        members.remove(member_id)
                elif "add" in type:
                    if not member_id in members:
                        members.append(member_id)
            elif "rem" in type:
                if not new_name:
                    return JsonResponse({"msg": "Name required in this method"}, status=400)
                channel_name = new_name
            Channel.update_item(
                keys={"ChannelID": channel_id},
                Members=members,
                ChannelName=channel_name
            )
            return JsonResponse({"msg": "Successfully Updated", "channel_id": channel_id}, status=200)
        except IndexError:
            return JsonResponse({"msg": "Channel Not Found"}, status=501)
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
        
    @method_decorator([jwt_token_required, access_channel_allowance])
    def delete(self, request):
        try:
            channel = request.channel
            channel_id = channel["ChannelID"]            
            Channel.delete_item(
                ChannelID=channel_id
            )
            return JsonResponse({"msg": "Successfully Deleted", "channel_id": channel_id}, status=200)
        except Exception as err:
            return JsonResponse({"msg": str(err.args)}, status=500)

class ChatMessageView(View):
    @method_decorator(jwt_token_required)
    def get(self, request, *args, **kwargs):
        try:
            channel_id = kwargs.get("channel_id") if kwargs.get("channel_id", "") != "" else None
            messages = ChatMessage.query(
                scan_index_forward=False,
                ChannelID=channel_id
            )
            return JsonResponse({"msg": f"{len(messages)} Messages are found", "messages": messages}, status=200)    
        except Exception as err:
            return JsonResponse({"msg": str(err)}, status=500)
