from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from.models import  Topic, Room,Message
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .form import RoomForm, UserForm
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
         q=request.GET.get('q') if request.GET.get('q')!=None else ''
         rooms= Room.objects.filter(Q(topic__name__icontains=q)|
                               Q(name__icontains=q)|
                               Q(description__icontains=q)
                               
                               )
         topics=Topic.objects.all()[0:4]
         room_count=rooms.count()
         room_message=Message.objects.filter(Q(room__name__icontains=q))

         return render(request,'home.html',{'rooms':rooms,'topics':topics,'room_count':room_count,'room_message':room_message})
    else:
        return redirect('login')


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created_at')
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    return render(request, 'room.html', {'room': room, 'messages': messages, 'participants': participants})

def create_room(request):
    form=RoomForm()
    topics=Topic.objects.all()

    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form=RoomForm(request.POST)
        # if form.is_valid():
        #    room=form.save(commit=False)
        #    room.host=request.user
        #    room.save()
        return redirect('home')

    return render(request, 'room-add.html',{'form': form,'topics':topics})


def update_record(request, pk):
    if request.user.is_authenticated:
        curent = Room.objects.get(id=pk)  # Fetch the current room
        topics = Topic.objects.all()

        form = RoomForm(instance=curent)
        
        if request.method == "POST":
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            
            # Update the 'curent' instance, not 'room'
            curent.name = request.POST.get('name')
            curent.topic = topic
            curent.description = request.POST.get('description')
            
            # Save the updated room
            curent.save()  # Save the room instance after updating
            
            return redirect('home')
        
        return render(request, 'update.html', {'form': form, 'topics': topics, 'current': curent})
    else:
        return redirect('home')


# Create your views here.
def delete(request,pk):
    room= Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':room})


def login_user(request):
   

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'login successfully')
            return redirect('home')
        else:
            messages.success(request,'Wrong username or password combination')
            return redirect('login')
    else:
        return  render(request,'login.html')
    


def logout_user(request):
    logout(request)
    messages.success(request, 'you have log out............')
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password==password1:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.success(request, 'user is arleady exists')
                return redirect('register')
            elif len(password)<8 or len(password1)<8:
                messages.success(request, 'The password should contain 8 charater')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                messages.success(request, 'You have been registered to the system')
                return redirect('login')
        else:
            messages.success(request, 'Two password doesnot match.try again')
            return redirect('register')
    else:


        return render(request, 'register.html')
    



def delete_message(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse('Your not allowed here')
    if request.method=="POST":
        message.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':message})




def profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    return render(request,'profile.html',{'user':user,'rooms':rooms,'topics':topics,'room_message':room_messages})


def update_user(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=="POST":
        form=UserForm(request.POST,instance=user)
        if  form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)

    return render(request,'update-user.html',{'form':form})


def topics(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'topics.html',{"topics":topics})




def activities(request):
    messages=Message.objects.all()
    return render(request, 'activity.html',{'messages':messages})
