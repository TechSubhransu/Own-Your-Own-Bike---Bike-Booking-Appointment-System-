from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Message

@login_required
def chat_view(request):
    return render(request, 'chat/chat.html')

@staff_member_required
def admin_chat_view(request):
    messages = Message.objects.all().order_by('timestamp')
    return render(request, 'chat/admin_chat.html', {'messages': messages})
