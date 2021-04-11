from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse
from allauth.account.models import EmailAddress
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserForm
from django.http import Http404
from django.shortcuts import get_list_or_404
from .models import Topic, Word, Userr, State
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, "index.html")


def topics(request,text = " "):
    user_au = User.objects.get(username=request.user)  # если новый пользователь добавляем в Userr
    cout = Userr.objects.count()
    if user_au.id > cout:
        us = Userr()
        us.id_login = user_au.id
        us.save()
    topics = Topic.objects.all()
    context = {"topic_list": topics, "userr": user_au.id, "cout": cout,"text":text}
    return render(request, "topic/topic_list.html", context)


def topic(request):
    return render(request, "topic/" + request.Topic.urls)


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, 'topic/topic_detail.html', {'topic': topic})


def mainpage(request):
    return render(request, 'topic/learn/start.html')


class Words_list(View):
    def __init__(self, idtopic, idword):
        self.i = 1
        self.dictwords = Word.objects.raw('SELECT * FROM wordsapp_word WHERE id_topic_id = %s AND id > %s ',
                                          [idtopic, idword])

    def nextval(self):
        self.i = self.i + 1
        value = self.dictwords[self.i - 1]
        return value


def start(request, idtopic, idword):

    endstudy = False
    curruser = request.user.id
    words_in_state_topic = Word.objects.filter(id_topic=idtopic).filter(state__id_user_id = curruser)
    #если только начал изучать тему
    if words_in_state_topic.count() == 0:
        all_words_topic = Word.objects.filter(id_topic=idtopic)
        for i in all_words_topic:
            State.objects.create(id_user_id=curruser,id_word_id=i.id,status=False)


    list_newword = Word.objects.filter(id_topic=idtopic).filter(state__id_user_id=curruser,state__status = False)
    # обработка ошибки если последнее слово
    try:
        nextword = list_newword[1]
    except IndexError:
        endstudy = True
    #перенаправление для выбора темы когда все слова выученны
    if endstudy == True :
        return HttpResponseRedirect(reverse('topics',))
    
    newword = list_newword[0]

        #все слова выученны скрыть надпись на выбор темы
        #text = "Все слова данного расдела выученны!"
        #return render(request, 'topic/learn/start.html',{"text":text} )

    ans = ""
    userform = UserForm()
    #если все слова выученны перенаправляем на выбор раздела

    if request.method == "POST":
        usword = request.POST.get("name")
        if usword == newword.translate:
            num = Userr.objects.get(id=curruser).balls
            Userr.objects.filter(id=curruser).update(balls=num + 10)
            ans = "ВЕРНО"
            #

            st = State.objects.filter(id_word_id=newword.id).filter(id_user_id=curruser)[0]
            st.status = True
            st.save()

            #
            context = {"wordone": nextword, "form": userform, "answer": ans}
            return render(request, 'topic/learn/start.html', context)
        else:
            ans = "НЕВЕРНО"
            #

            st = State.objects.filter(id_word_id=newword.id).filter(id_user_id=curruser)[0]
            st.status = False
            st.save()

            #
            context = {"wordone": nextword, "form": userform, "answer": ans}
            return render(request, 'topic/learn/start.html', context)


    context = {"wordone": newword, "form": userform, "answer": ans}
    return render(request, 'topic/learn/start.html', context)
