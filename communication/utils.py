import os
from datetime import (
    datetime,
    timedelta
)
from typing import List
import uuid
import tempfile
from utils.aws_s3 import s3_logger
from pydub import AudioSegment
from twilio.rest import Client
from twilio.base.exceptions import (
    TwilioRestException,
    TwilioException
)
from azure.cognitiveservices.speech import (
    SpeechConfig, 
    SpeechRecognizer, 
    ResultReason,
    CancellationReason,
    SpeechSynthesizer,
    SpeechSynthesisOutputFormat,
    AudioDataStream
)
from azure.cognitiveservices.speech.audio import (
    AudioConfig,
    AudioOutputConfig,
)
from azure.communication.identity import (
    CommunicationIdentityClient,
    CommunicationUserIdentifier
)
from azure.communication.chat import (
    ChatClient, 
    CommunicationTokenCredential,
    ChatParticipant,
    ChatMessageType,
)
from moviepy.audio.io.AudioFileClip import (
    AudioFileClip,
)
from azure.communication.phonenumbers import (
    PhoneNumbersClient,
    PhoneNumberCapabilities,
    PhoneNumberCapabilityType,
    PhoneNumberType,
    PhoneNumberAssignmentType,
)
from azure.communication.phonenumbers.siprouting import (
    SipRoutingClient,
    SipTrunk,
    SipTrunkRoute
)
from azure.communication.callautomation import (
    CallAutomationClient,
    CallInvite,
    PhoneNumberIdentifier,
    FileSource,
    ServerCallLocator,
    RecognizeInputType,
    DtmfTone,
    RecordingContent,
    RecordingChannel,
    RecordingFormat,
    ChannelAffinity
)
from utils.aws_s3 import S3Object
from backend.settings import (
    SPEECH_KEY,
    SERVICE_REGION,
    COMMUNICATION_ENDPOINT_URL,
    COMMUNICATION_IDENTITY,
    COMMUNICATION_ACCESS_TOKEN,
    CONNECTION_STRING,
    BOT_IDENTITY,
    NUMBERS_TO_DIAL,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_NUMBER,
    TWILIO_REGION,
    TWILIO_VOICE_URL,
    TWILIO_SMS_URL,
    TWILIO_API_KEY,
    TWILIO_API_SECRET,
    AZURE_NUMBER,
    CALLBACK_URI_HOST,
    BOT_CHAT_THREAD_ID,
    Path
)


""" Audio Processing """        
class AudioProcessor:

    def export_to_wav(self, audio_file):
        dst_full_path = ""
        try:
            if "mpeg" in audio_file.content_type:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    dst_full_path = f"{temp_file.name}.wav"
                    sound = AudioSegment.from_mp3(file=audio_file)
                    sound.export(dst_full_path, format="wav")
                return dst_full_path
            else:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(audio_file.read())
                    dst_full_path = f"{temp_file.name}.wav"
                audio_clip = AudioFileClip(temp_file.name)
                audio_clip.write_audiofile(dst_full_path)
                os.remove(temp_file.name)
                return dst_full_path
        except Exception as err:
            s3_logger.error(f"Failed Exporting to wav: {str(err)}")
            print(f"Failed Converting to wav: {str(err)}")
            raise Exception("Invalid Audio File")


""" Azure Cognitive Service """
class CognitiveService(AudioProcessor):

    speech_recognition_lang = "en-US"
    speech_key = SPEECH_KEY
    service_region = SERVICE_REGION

    def __init__(self, _speech_key=None, _service_region=None, _speech_recognition_lang="en-US") -> None:
        super().__init__()
        if _speech_key:
            self.speech_key = _speech_key
        if _service_region:
            self.service_region = _service_region
        self.speech_recognition_lang = _speech_recognition_lang

    def speech_to_text_from_file(self, file_path):
        file_extension = os.path.splitext(file_path)[1]
        if not 'wav' in file_extension:
            s3_logger.error(f"Invalid WAV file extension: {file_extension}")
            raise Exception("Invalid WAV file extension")
        speech_config = SpeechConfig(subscription=self.speech_key, region=self.service_region, speech_recognition_language=self.speech_recognition_lang)
        audio_config = AudioConfig(filename=file_path)
        speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language=self.speech_recognition_lang)
        speech_recognition_result = speech_recognizer.recognize_once()

        if speech_recognition_result.reason == ResultReason.RecognizedSpeech:
            return speech_recognition_result.text
        elif speech_recognition_result.reason == ResultReason.NoMatch:
            s3_logger.error(f"No speech could be recognized: {speech_recognition_result.no_match_details}")
            print(f"No speech could be recognized: {speech_recognition_result.no_match_details}")
            raise Exception(f"No speech could be recognized: {speech_recognition_result.no_match_details}")
        elif speech_recognition_result.reason == ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            s3_logger.error(f"Speech Recognition canceled: {cancellation_details.reason}")
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
                print("Did you set the speech resource key and region values?")
                s3_logger.error(f"""Speech Recognition canceled: {cancellation_details.reason}
Error details: {cancellation_details.error_details}
Did you set the speech resource key and region values?""")
                raise Exception(f"""Speech Recognition canceled: {cancellation_details.reason}
Error details: {cancellation_details.error_details}
Did you set the speech resource key and region values?""")
            else:
                raise Exception(f"""Speech Recognition canceled: {cancellation_details.reason}""")
            
    def text_to_speech_file(self, text):
        speech_config = SpeechConfig(subscription=self.speech_key, region=self.service_region, speech_recognition_language=self.speech_recognition_lang)
        file_path = ""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_path = f"{temp_file.name}.wav"
        audio_config = AudioOutputConfig(filename=file_path)
        # audio_config = None
        speech_config.speech_synthesis_voice_name='en-US-EricNeural'
        speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
        speech_synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        stream = AudioDataStream(speech_synthesis_result)
        # stream.save_to_wav_file_async(file_name=file_path)

        if speech_synthesis_result.reason == ResultReason.SynthesizingAudioCompleted:
            return stream, file_path
        elif speech_synthesis_result.reason == ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
            raise Exception("Failed")
            

""" Azure Communication Service """
class CommunicationService:

    endpoint_url = COMMUNICATION_ENDPOINT_URL
    identity = COMMUNICATION_IDENTITY
    access_token = COMMUNICATION_ACCESS_TOKEN
    connection_string = CONNECTION_STRING
    chat_client = None
    user_identifier = None
    identity_client = None

    def __init__(self) -> None:
        if not self.identity_client:
            self.create_identity_client()
        if not self.user_identifier:
            self.create_user_identifier()
        if not self.access_token:
            self.create_user_access_token()
        if not self.chat_client:
            self.create_chat_client()
    
    ## Configuration
    def create_identity_client(self):
        self.identity_client = CommunicationIdentityClient.from_connection_string(self.connection_string)

    def create_user_identifier(self):
        self.user_identifier = CommunicationUserIdentifier(self.identity)
    
    def create_new_user_identifier(self):
        self.user_identifier = self.identity_client.create_user()

    def create_user_access_token(self):
        self.access_token = self.identity_client.get_token(self.user, scopes=["chat", "voip"])
    
    def create_chat_client(self):
        self.chat_client = ChatClient(self.endpoint_url, CommunicationTokenCredential(self.access_token))
    

""" Communication Service - Chat Bot Thread """
class CommunicationChatBotService(CommunicationService):

    bot_identity = BOT_IDENTITY
    bot_chat_thread_id = BOT_CHAT_THREAD_ID
    bot_identifier = None

    def __init__(self) -> None:
        super().__init__()
        if not self.bot_identifier:
            self.bot_identifier = CommunicationUserIdentifier(self.bot_identity)
        if not self.bot_chat_thread_id:
            self.create_bot_chat_thread()
            threads = self.chat_client.list_chat_threads()
            for thread in threads:
                print(thread)
                self.bot_chat_thread_id = thread.id
        # self.chat_client.get_chat_thread_client(thread_id=self.bot_chat_thread_id)
        # bot_chat_thread_client = self.chat_client.get_chat_thread_client(thread_id=self.bot_chat_thread_id)
        # for part in bot_chat_thread_client.list_participants():
        #     print(part.display_name)
        # msg_id = self.send_message_to_bot(thread_id=bot_chat_thread_client.thread_id, message_content="Hello", sender="me")
        # print(self.get_messages_from_bot(thread_id=bot_chat_thread_client.thread_id, days=1)[0]['content'])
        # return bot_chat_thread_client.thread_id

    # Add Chat bot to the communication service
    def create_bot_chat_thread(self, user_name=None, phone_number=None):
        if user_name:
            participant = ChatParticipant(identifier=self.identity_client.create_user(), display_name=user_name)
        elif phone_number:
            participant = ChatParticipant(identifier=self.identity_client.create_user(), display_name=phone_number)
        else:
            user_name = uuid.uuid4()
            participant = ChatParticipant(identifier=self.identity_client.create_user(), display_name=user_name)
        bot_participant = ChatParticipant(identifier=self.bot_identifier, display_name='support_bot', share_history_time=datetime.utcnow())
        chat_thread_client = self.chat_client.create_chat_thread(
            topic="Support Chat",
            thread_participants=[
                participant,
                bot_participant
            ]
        )
        return chat_thread_client.chat_thread.id
    
    # Send Message to Bot
    def send_message_to_bot(self, thread_id=None, message_content: str=None, sender=None):
        if not message_content or not sender:
            raise ValueError("Invalid Message")
        if not thread_id:
            thread_id = self.bot_chat_thread_id
        bot_chat_thread_client = self.chat_client.get_chat_thread_client(thread_id=thread_id)
        send_message_result = bot_chat_thread_client.send_message(
            message_content,
            sender_display_name=sender,
            chat_message_type=ChatMessageType.TEXT # equivalent to chat_message_type = 'text'
        )
        return send_message_result.id
    
    # Receive Message from Bot
    def get_messages_from_bot(self, thread_id=None, days=1, limit=2):
        if not thread_id:
            thread_id = self.bot_chat_thread_id
        bot_chat_thread_client = self.chat_client.get_chat_thread_client(thread_id=thread_id)
        start_time = datetime.utcnow() - timedelta(days=days)
        chat_messages = bot_chat_thread_client.list_messages(results_per_page=1, start_time=start_time)
        list_messages = []
        for chat_message_page in chat_messages.by_page():
            for chat_message in chat_message_page:
                list_messages.append({
                    "id": chat_message.id,
                    "content": chat_message.content.message
                })
                if len(list_messages) == limit:
                    break
        return list_messages
    

""" Communication Service - Chat """
class CommunicationChatService(CommunicationService):

    def __init__(self) -> None:
        super().__init__()
    
    # Thread Operations
    ## Creat Chat Thread By Topic and Thread Participants
    def create_chat_thread(self, _topic=None, _thread_participants=None):
        if not _thread_participants:
            _thread_participants = [
                ChatParticipant(identifier=self.user_identifier, display_name='@support_team', share_history_time=datetime.utcnow()),
            ]
        if not _topic:
            _topic = "Supporting"
        _idempotency_token = uuid.uuid4()
        create_chat_thread_result = self.chat_client.create_chat_thread(_topic, thread_participants=_thread_participants, idempotency_token=_idempotency_token)
        create_chat_thread_result = self.chat_client.create_chat_thread(_topic)
        chat_thread_client = self.chat_client.get_chat_thread_client(create_chat_thread_result.chat_thread.id)
        return chat_thread_client.thread_id
    
    ## Get Chat Thread By Thread Id
    def get_chat_thread_by_id(self, thread_id):
        chat_thread_client = self.chat_client.get_chat_thread_client(thread_id) # thread_id is the id of an existing chat thread
        return chat_thread_client
    
    ## Delete Chat Thread By Id
    def delete_chat_thread_by_id(self, thread_id):
        self.chat_client.delete_chat_thread(thread_id) # thread_id is the id of an existing chat thread
    
    ## Get List of Chat Threads
    def get_chat_threads(self, days=1):
        start_time = datetime.now() - timedelta(days=days)
        chat_threads = self.chat_client.list_chat_threads(results_per_page=5, start_time=start_time)
        list_chat_threads = []
        for chat_thread_item_page in chat_threads.by_page():
            for chat_thread_item in chat_thread_item_page:
                list_chat_threads.append(chat_thread_item)
                print("thread id:", chat_thread_item.id)
        return list_chat_threads

    ## Update Chat Thread Topic by Thread Id with New Topic
    def update_chat_thread_topic(self, thread_id, new_topic):
        chat_thread_client = self.get_chat_thread_by_id(thread_id)
        chat_thread_client.update_topic(new_topic)

    # Message Operations
    ## Send Message to Chat Thread by Thread Id
    def send_message(self, chat_thread_id, message, sender):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        send_chat_message_result = chat_thread_client.send_message(
            message,
            sender_display_name=sender,
            chat_message_type=ChatMessageType.TEXT # equivalent to chat_message_type = 'text'
        )
        print("Message sent: id: ", send_chat_message_result.id)  
        return send_chat_message_result

    ## Get Message in Thread Id by Message Id
    def get_message_by_id(self, chat_thread_id, message_id):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        chat_message = chat_thread_client.get_message(message_id=message_id)
        print("get_chat_message succeeded, message id:", chat_message.id, "content: ", chat_message.content)
        return chat_message
    
    ## Get List of Messages in Chat Thread by Thread Id
    def get_messages(self, chat_thread_id, days=1):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        start_time = datetime.now() - timedelta(days=days)
        chat_messages = chat_thread_client.list_messages(results_per_page=5, start_time=start_time)
        list_chat_messages = []
        for chat_message_page in chat_messages.by_page():
            for chat_message in chat_message_page:
                list_chat_messages.append(chat_message)
                print("ChatMessage: Id=", chat_message.id, "; Content=", chat_message.content.message)
        return list_chat_messages
    
    ## Update Message in Chat Thread by Thread Id and Message Id with New Content
    def update_message(self, chat_thread_id, message_id, new_content):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        chat_thread_client.update_message(message_id, content=new_content)

    ## Delete Message in Chat Thread by Thread Id and Message Id
    def delete_message(self, chat_thread_id, message_id):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        chat_thread_client.delete_message(message_id=message_id)

    # Thread Participant Operations
    ## Get List of Participants in Chat Thread by Thread Id
    def get_participants(self, chat_thread_id):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        chat_participants = chat_thread_client.list_participants(results_per_page=5)
        list_chat_participants = []
        for chat_participant_page in chat_participants.by_page():
            for chat_participant in chat_participant_page:
                list_chat_participants.append(chat_participant)
                print("ChatParticipant: ", chat_participant)
        return list_chat_participants
    
    ## Add Participant to Chat Thread by Thread Id
    def add_participant(self, chat_thread_id, chat_participant, user_identifier=None, display_name="Me"):
        if not user_identifier:
            user_identifier = self.user_identifier
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        chat_participant = ChatParticipant(
            identifier=user_identifier,
            display_name=display_name,
            share_history_time=datetime.utcnow()
        )
        chat_thread_client.add_participants([chat_participant])

    ## Remove the Specific Participant from Chat Thread by Thread Id
    def remove_participant(self, chat_thread_id, user_identifier=None):
        if not user_identifier:
            user_identifier = self.user_identifier
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        chat_thread_client.remove_participant(identifier=user_identifier)

    # Events Operations
    ## Send Typing Notification to Chat Thread by Thread Id
    def send_typing_notification(self, chat_thread_id, display_name=None):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        chat_thread_client.send_typing_notification(display_name=display_name)

    ## Send Read Receipt to Chat Thread by Thread Id and Message Id
    def send_read_receipt(self, chat_thread_id, message_id):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        chat_thread_client.send_read_receipt(message_id=message_id)

    ## Get List of Read Receipts in Chat Thread by Thread Id
    def get_read_receipts(self, chat_thread_id):
        chat_thread_client = self.get_chat_thread_by_id(chat_thread_id)
        read_receipts = chat_thread_client.list_read_receipts(results_per_page=5)
        list_receipts = []
        for read_receipt_page in read_receipts.by_page():
            for read_receipt in read_receipt_page:
                list_receipts.append(read_receipt)
                print(read_receipt)
                print(read_receipt.sender)
                print(read_receipt.chat_message_id)
                print(read_receipt.read_on)
        return list_receipts

""" Communication Service - Phone Numbers """
class CommunicationPhoneNumberService(CommunicationService):

    phone_number = AZURE_NUMBER
    target_phone_number = NUMBERS_TO_DIAL
    phone_numbers_client = None
    sip_routing_client = None

    def __init__(self) -> None:
        super().__init__()
        if not self.phone_numbers_client:
            self.create_phone_numbers_client()
        if not self.sip_routing_client:
            self.create_sip_routing_client()

    ### Create Phone Numbers Client
    def create_phone_numbers_client(self):
        self.phone_numbers_client = PhoneNumbersClient.from_connection_string(self.connection_string)

    ### Create SIP Routing Client
    def create_sip_routing_client(self):
        self.sip_routing_client = SipRoutingClient.from_connection_string(self.connection_string)

    ## Phone Number Operations
    ### Get All Purchased Phone Numbers
    def get_all_purchased_phone_numbers(self):
        purchased_phone_numbers = self.phone_numbers_client.list_purchased_phone_numbers()
        list_phone_numbers = []
        for acquired_phone_number in purchased_phone_numbers:
            list_phone_numbers.append(acquired_phone_number.phone_number)
            print(acquired_phone_number.phone_number)
        return list_phone_numbers
    
    ### Get Purchased Phone Number - Gets the information from the specified phone number
    def get_purchased_phone_number(self, phone_number):
        result = self.phone_numbers_client.get_purchased_phone_number(phone_number)
        print(f"County Code: {result.country_code}, Phone Number: {result.phone_number}")
        return result
    
    ## Long Running Operations
    ### Search for Available Phone Number
    def get_available_phone_numbers(self, country_code="US"):
        capabilities = PhoneNumberCapabilities(
            calling = PhoneNumberCapabilityType.INBOUND,
            sms = PhoneNumberCapabilityType.INBOUND_OUTBOUND
        )
        poller = self.phone_numbers_client.begin_search_available_phone_numbers(
            country_code,
            PhoneNumberType.TOLL_FREE,
            PhoneNumberAssignmentType.APPLICATION,
            capabilities,
            polling = True
        )
        search_result = poller.result()
        return search_result
    
    ### Purchase Phone Numbers
    def purchase_phone_numbers(self, country_code="US"):
        search_result = self.get_available_phone_numbers(country_code)
        purchase_poller = self.phone_numbers_client.begin_purchase_phone_numbers(
            search_result.search_id,
            polling=True
        )
    
    ### Release Phone Number
    def release_phone_number(self, phone_number):
        poller = self.phone_numbers_client.begin_release_phone_number(
            phone_number,
            polling = True
        )
    
    ### Updating Phone Number Capabilities
    def update_phone_number_capabilities(self, phone_number, capabilities):
        poller = self.phone_numbers_client.begin_update_phone_number_capabilities(
            phone_number,
            PhoneNumberCapabilityType.INBOUND_OUTBOUND,
            PhoneNumberCapabilityType.INBOUND_OUTBOUND,
        )
    
    ### Look up operator information for a number
    def get_operator_information(self, phone_number):
        results = self.phone_numbers_client.search_operator_information(phone_number)
        return results.values[0]
    
    ## SipRoutingClient
    ### Retrieve SIP trunks
    def get_sip_trunks(self):
        trunks = self.sip_routing_client.list_trunks()
        list_sip_trunks = []
        for trunk in trunks:
            list_sip_trunks.append(trunk)
            print(trunk.fqdn)
            print(trunk.sip_signaling_port)
        return list_sip_trunks
    
    ### Retrieve SIP routes
    def get_sip_routes(self):
        routes = self.sip_routing_client.list_routes()
        list_sip_routes = []
        for route in routes:
            list_sip_routes.append(route)
            print(route.name)
            print(route.description)
            print(route.number_pattern)
            for trunk_fqdn in route.trunks:
                print(trunk_fqdn)
        return list_sip_routes
    
    ### Replace SIP trunks and routes
    def replace_sip_trunks_and_routes(self, new_trunks: List[SipTrunk], new_routes: List[SipTrunkRoute]):
        # new_trunks = [
        #     SipTrunk(fqdn="sbs1.contoso.com", sip_signaling_port=1122), 
        #     SipTrunk(fqdn="sbs2.contoso.com", sip_signaling_port=1123)
        # ]
        # new_routes = [
        #     SipTrunkRoute(name="First rule", description="Handle numbers starting with '+123'", number_pattern="\+123[0-9]+", trunks=["sbs1.sipconfigtest.com"])
        # ]
        self.sip_routing_client.set_trunks(new_trunks)
        self.sip_routing_client.set_routes(new_routes)
    
    ### Retrieve single trunk
    def get_retrive_single_sip_trunk(self, sip_trunk_fqdn):
        trunk = self.sip_routing_client.get_trunk(sip_trunk_fqdn)
        return trunk
    
    ### Set single trunk
    def set_single_trunk(self, new_trunk):
        # new_trunk = SipTrunk(fqdn="sbs3.contoso.com", sip_signaling_port=5555)
        self.sip_routing_client.set_trunk(new_trunk)
    
    ### Delete single trunk
    def delete_sip_trunks_and_routes(self, sip_trunk_fqdn):
        self.sip_routing_client.delete_trunk(sip_trunk_fqdn)


""" Communication Service - Call Automation """
class CommunicationCallAutomationService(CommunicationPhoneNumberService):

    call_automation_client = None
    callback_url_host = CALLBACK_URI_HOST
    audio_file_path = "/audio"
    main_menu_prompt_uri = callback_url_host + audio_file_path + "/MainMenu.wav"
    confirmed_prompt_uri = callback_url_host + audio_file_path + "/Confirmed.wav"
    goodbye_prompt_uri = callback_url_host + audio_file_path + "/Goodbye.wav"
    invalid_prompt_uri = callback_url_host + audio_file_path + "/Invalid.wav"
    timeout_prompt_uri = callback_url_host + audio_file_path + "/Timeout.wav"
    recording_state_callback_url = CALLBACK_URI_HOST + "/recording-state-callbacks"
    recording_ids = []

    def __init__(self) -> None:
        super().__init__()
        self.s3_obj_main_menu = S3Object(s3_object_key="callautopromptaudio/MainMenu.wav")
        if not self.s3_obj_main_menu.exists():
            self.s3_obj_main_menu.put(os.path.join(Path(__file__).parent, 'audio', 'MainMenu.wav'))
        self.s3_obj_confirmed = S3Object(s3_object_key="callautopromptaudio/Confirmed.wav")
        if not self.s3_obj_confirmed.exists():
            self.s3_obj_confirmed.put(os.path.join(Path(__file__).parent, 'audio', 'Confirmed.wav'))
        self.s3_obj_goodbye = S3Object(s3_object_key="callautopromptaudio/Goodbye.wav")
        if not self.s3_obj_goodbye.exists():
            self.s3_obj_goodbye.put(os.path.join(Path(__file__).parent, 'audio', 'Goodbye.wav'))
        self.s3_obj_invalid = S3Object(s3_object_key="callautopromptaudio/Invalid.wav")
        if not self.s3_obj_invalid.exists():
            self.s3_obj_invalid.put(os.path.join(Path(__file__).parent, 'audio', 'Invalid.wav'))
        self.s3_obj_timeout = S3Object(s3_object_key="callautopromptaudio/Timeout.wav")
        if not self.s3_obj_timeout.exists():
            self.s3_obj_timeout.put(os.path.join(Path(__file__).parent, 'audio', 'Timeout.wav'))
        if not self.call_automation_client:
            self.create_call_automation_client()

    def create_call_automation_client(self):
        self.call_automation_client = CallAutomationClient.from_connection_string(self.connection_string)

    # Create Call
    def create_call(self, target_participant=None, source_caller=None):
        if not target_participant:
            target_participant = PhoneNumberIdentifier(self.phone_number)
        if not source_caller:
            source_caller = PhoneNumberIdentifier(self.target_phone_number)
        call_invite = CallInvite(target=target_participant, source_caller_id_number=source_caller)
        result = self.call_automation_client.create_call(call_invite, f"{self.callback_url_host}/callbacks")
        return result.call_connection_id
    
    # Play media
    def play_media(self, call_connection_id, file_url=None):
        if not file_url:
            raise FileNotFoundError("File Not Found")
        # using call connection id, get call connection
        call_connection = self.call_automation_client.get_call_connection(call_connection_id)

        # from callconnection of result above, play media to all participants
        my_file = FileSource(url=file_url)
        call_connection.play_media_to_all(my_file)

    # Play media by Tone
    def play_media_by_tone(self, call_connection_id, tone):
        if tone == DtmfTone.ZERO:
            try:
                print("Playing timeout prompt from s3")
                self.play_media(call_connection_id=call_connection_id, file_url=self.s3_obj_timeout.get_object_url())
            except:
                print("Playing timeout prompt from local")
                self.play_media(call_connection_id=call_connection_id, file_url=self.timeout_prompt_uri)
        if tone == DtmfTone.ONE:
            try:
                print("Playing confirm prompt from s3")
                self.play_media(call_connection_id=call_connection_id, file_url=self.s3_obj_confirmed.get_object_url())
            except:
                print("Playing confirm prompt from local")
                self.play_media(call_connection_id=call_connection_id, file_url=self.confirmed_prompt_uri)
        elif tone == DtmfTone.TWO:
            try:
                print("Playing goodbye prompt from s3")
                self.play_media(call_connection_id=call_connection_id, file_url=self.s3_obj_goodbye.get_object_url())
            except:
                print("Playing goodbye prompt from local")
                self.play_media(call_connection_id=call_connection_id, file_url=self.goodbye_prompt_uri)
        else:
            try:
                print("Playing invalid prompt from s3")
                self.play_media(call_connection_id=call_connection_id, file_url=self.s3_obj_invalid.get_object_url())
            except:
                print("Playing invalid prompt from local")
                self.play_media(call_connection_id=call_connection_id, file_url=self.invalid_prompt_uri)
            
    
    # Stop recording
    def hangup(self, recording_id=None, hangout_call_connection_id=None):
        if recording_id:
            self.call_automation_client.stop_recording(recording_id)
        for id in self.recording_ids:
            if id["call_connection_id"] == hangout_call_connection_id:
                try:
                    self.recording_ids.remove(id)
                except:
                    pass
        call_connection_client = self.get_call_connection(call_connection_id=hangout_call_connection_id)
        call_connection_client.hang_up(is_for_everyone=True)
    
    # Get All Connection
    def get_call_connection(self, call_connection_id):
        call_connection = self.call_automation_client.get_call_connection(call_connection_id)
        return call_connection

    # Make a call
    def make_outbound_call(self, from_number=None, to_number=None):
        if not from_number:
            from_number = self.phone_number
        if not to_number:
            to_number = self.target_phone_number
        target_participant = PhoneNumberIdentifier(to_number)
        source_caller = PhoneNumberIdentifier(from_number)
        call_connection_id = self.create_call(target_participant=target_participant, source_caller=source_caller)
        s3_logger.info("Created call with connection id: %s" % (call_connection_id))
        print("Created call with connection id: %s", call_connection_id)
        return call_connection_id
    
    # Start Recording
    def start_recording(self, server_call_id, target_phone_number=None):
        if not target_phone_number:
            target_phone_number = self.phone_number
        _channel_affinity = ChannelAffinity(target_participant=PhoneNumberIdentifier(target_phone_number), channel=0)
        recording_properties = self.call_automation_client.start_recording(
            ServerCallLocator(server_call_id=server_call_id),
            recording_content_type = RecordingContent.AUDIO,
            recording_channel_type = RecordingChannel.UNMIXED,
            recording_format_type = RecordingFormat.WAV,
            recording_state_callback_url=self.recording_state_callback_url,
            channel_affinity=[_channel_affinity]
        )
        recording_id = recording_properties.recording_id
        return recording_id
    
    # Start Recognize
    def start_recognize(self, call_connection_id, target_phone_number=None):
        if not target_phone_number:
            target_phone_number = self.target_phone_number
        target_participant = PhoneNumberIdentifier(target_phone_number)
        # main_menu_prompt = FileSource(self.main_menu_prompt_uri)
        main_menu_prompt = FileSource(self.s3_obj_main_menu.get_object_url())
        call_connection_client = self.get_call_connection(call_connection_id)
        call_connection_client.start_recognizing_media(input_type=RecognizeInputType.DTMF,
                                                        target_participant=target_participant,
                                                        play_prompt=main_menu_prompt,
                                                        interrupt_prompt=True,
                                                        initial_silence_timeout=10,
                                                        dtmf_max_tones_to_collect=1)
        
    # Answer the Call
    def answer_call(self, incoming_call_context):
        call_connection_properties = self.call_automation_client.answer_call(incoming_call_context=incoming_call_context, callback_url=self.callback_url_host + "/callbacks")
        return call_connection_properties
    
    # Reject the call
    def reject_call(self, incoming_call_context):
        call_connection_properties = self.call_automation_client.reject_call(incoming_call_context=incoming_call_context)
        return call_connection_properties
        

""" Twilio Configuration """
class TwilioService:
    
    account_sid = TWILIO_ACCOUNT_SID
    api_key = TWILIO_API_KEY
    api_secret = TWILIO_API_SECRET
    auth_token = TWILIO_AUTH_TOKEN
    from_number = TWILIO_NUMBER
    to_number = NUMBERS_TO_DIAL
    region = TWILIO_REGION
    voice_url = TWILIO_VOICE_URL
    sms_url = TWILIO_SMS_URL
    client = None

    def __init__(self) -> None:
        if not self.client:
            self.client = Client(username=self.account_sid, password=self.auth_token)

    # Send SMS
    def send_sms(self, to_number=None, msg_txt=None):
        if not to_number:
            to_number = self.to_number
        if not msg_txt:
            msg_txt = "Hello from LocalGov.ai!"
        try:
            for sms in self.client.messages.list():
                print(sms.to)
            message = self.client.messages.create(
                to=to_number,
                from_=self.from_number,
                body=msg_txt
            )
            return message.sid
        except TwilioRestException as err:
            print(err)
            return None
        except TwilioException as err:
            print(err)
            return None


audio_processor = AudioProcessor()
cognitive_service = CognitiveService()
communication_chat_bot_service = CommunicationChatBotService()
communication_chat_service = CommunicationChatService()
communication_phone_number_service = CommunicationPhoneNumberService()
communication_call_automation_service = CommunicationCallAutomationService()
twilio_service = TwilioService()