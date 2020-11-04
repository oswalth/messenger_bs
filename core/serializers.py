from rest_framework import serializers
from .models import User, Chat, Message, Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'last_read_message')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    members = MemberSerializer('members', many=True)
    last_message = MessageSerializer('last_message')

    class Meta:
        model = Chat
        fields = '__all__'

