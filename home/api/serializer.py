from dataclasses import field
from rest_framework.serializers import ModelSerializer
from home.models import Room,Topic

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'