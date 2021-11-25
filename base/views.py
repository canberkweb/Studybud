from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm

# Create your views here.

    # rooms_dict = [
    #     {'id': 1, 'name':'id1 e girdiniz'},
    #     {'id': 2, 'name':'id2 e girdiniz'},
    #     {'id': 3, 'name':'id3 e girdiniz'},
    # ]
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    return render(request, 'base/login_register.html')
def home(request):
    q = request.GET.get('q')
    rooms = Room.objects.filter(topic__name=q)
    topic = Topic.objects.all()
    context = {'rooms_html': rooms, 'topics': topic}
    return render(request,'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}    
    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def createroom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
                form.save()
                return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('bunu yazan sen deglsin')
    if request.method =='POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('bunu yazan sen deglsin')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})