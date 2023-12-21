from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
	re_path(
		r'ws/users/(?P<user_id>\w+)/chat/$',
		ChatConsumer.as_asgi()
	),
]
