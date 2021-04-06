from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from .forms import UserForm
from django.shortcuts import get_list_or_404
from .models import Topic, Word, Userr
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404

def index(request):

    return render(request,"index.html")

def topics(request):
    user_au = User.objects.get(username=request.user) #если новый пользователь добавляем в Userr
    cout = Userr.objects.count()
    if user_au.id > cout:
        us = Userr()
        us.id_login = user_au.id
        us.save()
    #users = Users.objects.all()

    topics = Topic.objects.all()
    context = {"topic_list" : topics,"userr":user_au.id,"cout":cout}
    return render(request,"topic/topic_list.html",context)

def topic(request):
    return render(request,"topic/"+request.Topic.urls)


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, 'topic/topic_detail.html', {'topic': topic})

def mainpage(request):
    return render(request, 'topic/learn/start.html')

class Words_list(View):
    def __init__(self,idtopic,idword):
        self.i = 1
        self.dictwords = Word.objects.raw('SELECT * FROM wordsapp_word WHERE id_topic_id = %s AND id > %s ', [idtopic,idword])

    def nextval (self):
        self.i =self.i+1
        value = self.dictwords[self.i-1]
        return value

def start(request,idtopic,idword):
    x = Word.objects.raw('SELECT * FROM wordsapp_word WHERE id_topic_id = %s AND id > %s ', [idtopic,idword])[0]
    ans = ""
    userform = UserForm()
    if request.method == "POST":
        name = request.POST.get("name")
        if name == x.translate:
            curruser = User.objects.get(username=request.user.id)
            Userr.objects.filter(id=curruser).update(balls=+10)
            ans = "ВЕРНО"
            context = {"wordone": x, "form": userform, "answer": ans,"name":name,"x":x}
            return render(request, 'topic/learn/start.html',context)
        else:
            ans = "НЕВЕРНО"
            context = {"wordone": x, "form": userform, "answer": ans,"name":name,"x":x}
            return render(request, 'topic/learn/start.html',context)
    else:
        context = {"wordone":x,"form": userform,"answer":ans,"xtranslate":x.translate}
    return render(request, 'topic/learn/start.html',context)



