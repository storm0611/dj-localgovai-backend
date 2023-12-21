import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from models.authentication import (
	User
)
from models.communication import (
	ChatMessage,
	Channel,
	s3_logger
)

class ChatConsumer(AsyncWebsocketConsumer):
	def getUser(self, user_id):
		user = User.exists_item(UserID=user_id)
		return user

	def addOnlineUser(self, user_id):
		try:
			user = self.getUser(user_id=user_id)
			User.update_item(
				keys={
					"UserID": user_id,
					"OrgID": user["OrgID"]
				},
				UserOnLine=True
			)
		except Exception as err:
			print(err)

	def deleteOnlineUser(self, user_id):
		try:
			user = self.getUser(user_id=user_id)
			User.update_item(
				keys={
					"UserID": user_id,
					"OrgID": user["OrgID"]
				},
				UserOnLine=False
			)
		except:
			pass

	async def sendChannelList(self):
		channels = []
		for channel in self.channels:
			members = channel["Members"]
			member_list = []
			for member_id in members:
				if member_id != self.user_id:
					user = self.getUser(user_id=member_id)
					if user:
						member_list.append(user)
			if len(member_list):
				channels.append({
					"channel_id": channel["ChannelID"],
					"members": member_list
				})
		chatMessage = {
			'action': 'channel_list',
			'channel_list': channels
		}
		try:
			await self.send(text_data=json.dumps(chatMessage))
		except Exception as err:
			print(err)

	def saveMessage(self, message, user_id, channel_id):
		user = User.exists_item(UserID=user_id)
		message_id = ChatMessage.put_item(
			ChannelID=channel_id,
			MessageText=message,
			SenderID=user_id
		)
		message = ChatMessage.get_item(ChannelID=channel_id, MessageID=message_id)
		return {
			'action': 'message',
			'user_id': user_id,
			'channel_id': channel_id,
			'message': message,
			'user_image': user.get("Avatar", ""),
			'user_name': user.get("FirstName", "") + " " + user.get("LastName", ""),
			'created_on': str(message.get("CreatedOn", None))
		}

	async def connect(self):
		self.user_id = self.scope['url_route']['kwargs']['user_id']
		self.channels = await database_sync_to_async(
			list
		)(Channel.scan(comparison_op="contains", Members=self.user_id))
		for channel in self.channels:
			await self.channel_layer.group_add(
				channel["ChannelID"],
				self.channel_name
			)

		await database_sync_to_async(self.addOnlineUser)(self.user_id)
		self.user = await database_sync_to_async(self.getUser)(self.user_id)
		await self.accept()
		await self.sendChannelList()

	async def disconnect(self, close_code):
		await database_sync_to_async(self.deleteOnlineUser)(self.user_id)
		for channel in self.channels:
			await self.channel_layer.group_discard(
				channel["ChannelID"],
				self.channel_name
			)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		action = text_data_json['action']
		channel_id = text_data_json['channel_id']
		chatMessage = {}
		if action == 'message':
			message = text_data_json['message']
			user_id = text_data_json['user_id']
			chatMessage = await database_sync_to_async(
				self.saveMessage
			)(message, user_id, channel_id)
		elif action == 'typing':
			chatMessage = text_data_json
		await self.channel_layer.group_send(
			channel_id,
			{
				'type': 'chat_message',
				'message': chatMessage
			}
		)

	async def chat_message(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))
