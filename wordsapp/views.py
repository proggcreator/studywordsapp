
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserForm
from .models import Topic, Word, Userr, State,Synonym
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404



def index(request):
    return render(request, "index.html")

def mystat(request):
    curruser = request.user.id
    cwords =  State.objects.filter(id_user_id=curruser).filter(status__gte = 1).count()
    x= Userr.objects.filter(id=curruser)[0]
    cballs = x.balls
    context = {"words_count": cwords, "balls_count": cballs}
    return render(request, "topic/mystat.html",context)

def topics(request):
    user_au = User.objects.get(username=request.user)  # если новый пользователь добавляем в Userr
    cout = Userr.objects.count()
    if user_au.id > cout:
        us = Userr()
        us.id_login = user_au.id
        us.save()
    topics = Topic.objects.all()
    context = {"topic_list": topics, "userr": user_au.id, "cout": cout}
    return render(request, "topic/topic_list.html", context)


def topic(request):
    return render(request, "topic/" + request.Topic.urls)


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, 'topic/topic_detail.html', {'topic': topic})


def mainpage(request):
    return render(request, 'topic/learn/start.html')



def start(request, idtopic, idword):
    curruser = request.user.id
    words_in_state_topic = Word.objects.filter(id_topic=idtopic).filter(state__id_user_id = curruser)
    #если только начал изучать тему
    if words_in_state_topic.count() == 0:
        all_words_topic = Word.objects.filter(id_topic=idtopic)
        for i in all_words_topic:
            State.objects.create(id_user_id=curruser,id_word_id=i.id,status=0)
#слово правильно вовторено 3 раза
    list_newword = Word.objects.filter(id_topic=idtopic).filter(id__gt=idword).filter(state__status__lt = 1,
                                                                                       state__id_user_id=curruser)
    # обработка ошибки если последнее слово
    try:
        newword = list_newword[0]
    except IndexError:
        return HttpResponseRedirect(reverse('alllearn'))
    #перенаправление для выбора темы когда все слова выученны
    ans = ""
    userform = UserForm()
    #если все слова выученны перенаправляем на выбор раздела
    if request.method == "POST":
        usword = request.POST.get("translate")
        if usword == newword.translate:
            num = Userr.objects.get(id=curruser).balls
            Userr.objects.filter(id=curruser).update(balls=num + 10)
            ans = str("Верно")
            #
            st = State.objects.filter(id_word_id=newword.id).filter(id_user_id=curruser)[0]
            st.status = st.status+1
            st.save()
            try:
                nextword = list_newword[0]
            except IndexError:
                return HttpResponseRedirect(reverse('alllearn'))
            #
            context = {"wordone": nextword, "form": userform, "answer": ans}
            return render(request, 'topic/learn/start.html', context)
        else:
            try:
                nextword = list_newword[1]
            except IndexError:
                return HttpResponseRedirect(reverse('alllearn'))
            ans = "Неверно"
            context = {"wordone": nextword, "form": userform, "answer": ans}
            return render(request, 'topic/learn/start.html', context)


    context = {"wordone": newword, "form": userform, "answer": ans}
    return render(request, 'topic/learn/start.html', context)
#
#
#
def repeat(request, idtopic, idword):
    curruser = request.user.id
    words_in_state_topic = Word.objects.filter(state__id_user_id = curruser).filter(id_topic=idtopic)
    #если только начал изучать тему
    if words_in_state_topic.count() == 0:
        return HttpResponseRedirect(reverse('alllearn' ))
    list_newword = Word.objects.filter(id_topic=idtopic).filter(id__gte=idword).filter(state__id_user_id=curruser)
    syn = Synonym.objects.filter(id_word__word_syn=idword)
    # обработка ошибки если последнее слово
    try:
        newword = list_newword[0]
    except IndexError:
        return HttpResponseRedirect(reverse('alllearn',))
    #перенаправление для выбора темы когда все слова выученны
    ans = ""
    userform = UserForm()
    #если все слова выученны перенаправляем на выбор раздела
    if request.method == "POST" :

        usword = request.POST.get("translate")
        # проверка на последнее слово
        try:
            nextword = list_newword[1]
        except IndexError:
            return HttpResponseRedirect(reverse('alllearn' ))
        if usword == newword.translate:
            num = Userr.objects.get(id=curruser).balls
            Userr.objects.filter(id=curruser).update(balls=num + 10)
            ans = str("Верно")
            context = {"wordone": nextword, "form": userform, "answer": ans,"sin_list":syn}
            return render(request, 'topic/learn/repeat.html', context)
        else:
            ans = "Неверно"
            context = {"wordone": nextword, "form": userform, "answer": ans,"sin_list":syn}
            return render(request, 'topic/learn/repeat.html', context)


    context = {"wordone": newword, "form": userform, "answer": ans,"sin_list":syn}
    return render(request, 'topic/learn/repeat.html', context)

def alllearn(request):
    return render(request, "topic/alllearn/alllearn.html")