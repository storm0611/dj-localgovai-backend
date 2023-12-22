from django.urls import path, re_path
from django.views.static import serve
from backend.settings import (
    MEDIA_COMMUNICATION
)
from .views import (
    SpeechToTextView,
    TextToSpeechView,
    SendMessageBotView,
    PhoneNumberView,
    TwilioSendMessageView,
    CallAutomationView,
    CallAutomationCallBacksView,
    CallAutomationHangUpView,
    RecodingStateCallBacksView,
    ChannelView,
    ChatMessageView,
    FeedbackView
)

urlpatterns = [
    path('msg/speech-to-text', SpeechToTextView.as_view(), name='speech_to_text'),
    path('msg/text-to-speech', TextToSpeechView.as_view(), name='text_to_speech'),
    path('msg/send-message-bot', SendMessageBotView.as_view(), name='send_message_bot'),
    path('msg/feedback', FeedbackView.as_view(), name='feedback'),
    # re_path(r'^phone/available-phone/(?P<phone_number>\+\d+)$', PhoneNumberView.as_view(), name='available_phone'),
    path('phone/available-phone', PhoneNumberView.as_view(), name='available_phone'),
    path('call/make-outbound-call', CallAutomationView.as_view(), name='make_outbound_call'),
    path('call/hang-up', CallAutomationHangUpView.as_view(), name='hang_up'),
    path('call/callbacks', CallAutomationCallBacksView.as_view(), name='callbacks'),
    path('call/recording-state-callbacks', RecodingStateCallBacksView.as_view(), name='recording-state-callbacks'),
    re_path(r'^call/audio/(?P<path>.*)$', serve, {'document_root': MEDIA_COMMUNICATION}),
    path('phone/send-sms-message-twilio', TwilioSendMessageView.as_view(), name='send_twilio_sms_message'),

    # chat platform
    path('chats/channel', ChannelView.as_view(), name='chat_channel'),
    path('chats/<str:member_id>/channel', ChannelView.as_view(), name='chat_channel_member_id'),
    path('chats/channel/<str:channel_id>', ChannelView.as_view(), name='chat_channel_channel_id'),
	path('chats/<str:channel_id>/messages', ChatMessageView.as_view(), name='chat_message'),
]