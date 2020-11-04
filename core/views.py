from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CreateUserForm, MessagePostForm
from .models import User, Chat, Message, Member
from .serializers import UserSerializer, MessageSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register
import json


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return 'Unknown chat'


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('/login')
    context = {

    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/login')


def register_view(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Account was created for {username}')
            return redirect('/login')

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def list_users(request):
    users = User.objects.all()
    serialized = [UserSerializer(user).data for user in users]
    return JsonResponse(serialized, status=200, safe=False)


@login_required(login_url='login')
def user_info(request, username):
    try:
        user = User.objects.get(username=username)
        response = UserSerializer(user).data
        status = 200
    except User.DoesNotExist:
        response = {'message': f"{username} does not exits"}
        status = 400
    return JsonResponse(response, status=status)


@login_required(login_url='login')
@csrf_exempt
def chats_view(request):
    chats = Chat.objects.filter(membership__user=request.user)
    dialogues = {}
    for chat in chats:
        dialogues[chat.id] = chat.membership.exclude(user=request.user).first().user.username
    context = {
        'chats': chats,
        'dialogues': dialogues,
        'recipient': False
    }
    if request.method == 'POST':
        members = request.POST.get('member', [])
        if request.user.username == members:
            return render(request, 'error.html', {'msg': 'You can not have chat with yourself'})
        if not User.objects.filter(username__in=[members]):
            return render(request, 'error.html', {'msg': 'User not found'})

        users = User.objects.filter(username__in=[members] + [request.user.username])

        for chat in Member.objects.values('chat').filter(user__in=users).annotate(total=Count('chat')):
            if chat.get('total') != 1:
                chat = Chat.objects.get(id=chat.get('chat'))
                return redirect(f'/chat/{chat.id}')

        chat = Chat.objects.create(host=request.user)
        chat.members.set(users)
        return redirect('chats')
    elif request.method == 'GET':
        return render(request, 'chats.html', context)


@login_required(login_url='login')
def chat_info(request, pk):
    chat = Chat.objects.get(id=pk)
    chats = Chat.objects.filter(membership__user=request.user)
    message_form = MessagePostForm()
    messages = Message.objects.filter(chat__id=pk)
    recipient = chat.membership.exclude(user=request.user).first().user.username
    dialogues = {}
    for chat in chats:
        dialogues[chat.id] = chat.membership.exclude(user=request.user).first().user.username

    if request.method == 'POST':
        message_form = MessagePostForm(request.POST)
        if message_form.is_valid():
            content = message_form.cleaned_data.get('content', '')
            if not content:
                pass
            Message.objects.create(chat=chat, sender=request.user, content=content)
            return redirect(f'/chat/{chat.id}')

    context = {
        'chats': chats,
        'messages': messages,
        'user': request.user,
        'message_form': message_form,
        'recipient': recipient,
        'dialogues': dialogues
    }
    return render(request, 'chats.html', context)


@login_required(login_url='login')
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        chat = Chat.objects.get(id=data.get('chat'))
        message = Message.objects.create(sender=request.user, content=data.get('content', ''), chat=chat)
        chat.last_message = message
        serialized = MessageSerializer(message).data
        return JsonResponse(serialized, status=200, safe=False)
