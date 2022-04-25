from email import message
import email
from multiprocessing import context
import re
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .form import RoomForm, MessageForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# Create your views here.
def user_login(request):
    page = 'login'
    if request.user.is_authenticated:
       return redirect('home:home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist !')

        user = authenticate(request,email=email,password=password)  ##Kiểm tra thông tin đăng nhập có hơp lệ không
        
        if user is not None:
            login(request,user)
            return redirect ('home:home')
        else:
            messages.error(request, 'Username or Password does not exist !')

    context = {'page':page}
    return render(request,'home/login_form.html',context)

def user_logout(request):
    logout(request)
    return redirect('home:home')

def user_register(request):
    form = MyUserCreationForm()
    users = User.objects.all()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.username.lower()
            for user in users:
                if new_user.username == user.username:
                    messages.error(request, 'User already existed')
                else:
                    new_user.save()
            login(request, new_user)
            return redirect('home:home')
        else:
            messages.error(request, 'An error occured, please try again')
    return render(request, 'home/login_form.html',{'form': form})

def home(request):
    if request.GET.get('query') != None:
        query = request.GET.get('query')
    else:
         query = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(host__username__icontains=query)
        )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    rooms_messages = Message.objects.filter(room__topic__name__icontains=query)

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'rooms_messages': rooms_messages}
    return render(request,'home/home.html',context)

def room(request,pk):           
    room = Room.objects.get(id=pk)
    new_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('home:room', pk = room.id)
    context = {'room': room,'new_messages':new_messages,'participants':participants}
    return render(request,'home/room.html',context)

@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home:home')    
    context = {'form': form, 'topics' : topics}
    return render(request,'home/room_form.html', context)

@login_required(login_url='/login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home:home')
    context = {'form': form, 'topics': topics, 'room':room}
    return render(request,'home/room_form.html',context)

@login_required(login_url='/login')
def update_message(request,pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)
    if request.user != message.user:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('home:home')
    context = {'form': form}
    return render(request,'home/message_form.html',context)

@login_required(login_url='/login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    page = 'room'
    if request.user != room.host:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        room.delete()
        return redirect('home:home')
    context = {'obj': room, 'page': page}
    return render(request,'home/delete.html',context)

@login_required(login_url='/login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)
    page = 'message'
    if request.user != message.user:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        message.delete()
        return redirect('home:home')
    context = {'obj': message, 'page': page}
    return render(request,'home/delete.html',context)

"""def join_room(request):
    room = Object
    return redirect('home:room')"""

def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    rooms_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,'rooms':rooms,'rooms_messages':rooms_messages,'topics':topics}
    return render(request, 'home/profile.html', context)

def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES , instance=user)
        if form.is_valid():
            form.save()
            return redirect('home:user-profile', pk = user.id)
    context = {'form': form}
    return render(request,'home/update-user.html',context)

def topic_page(request):
    if request.GET.get('query') != None:
        query = request.GET.get('query')
    else:
         query = ''
    topics = Topic.objects.filter(name__icontains=query)
    context ={'topics': topics}
    return render(request,'home/topics.html',context)

def activity_page(request):
    rooms_messages = Message.objects.all()
    context ={'rooms_messages':rooms_messages}
    return render(request,'home/activity.html',context)