import imp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Room, Topic
from home.views import room
from .serializer import RoomSerializer,TopicSerializer



@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room,many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTopic(request,pk):
    topic = Topic.objects.get(id=pk)
    serializer = TopicSerializer(topic,many=False)
    return Response(serializer.data)
