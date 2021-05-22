from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name='main'),
    path("topics/",views.topics,name='topics'),
    path("mystat/",views.mystat,name='mystat'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topic/learn/', views.mainpage),
    path('topic/learn/<int:idtopic>/<int:idword>/', views.start, name = 'start'),
    path('topic/repeat/<int:idtopic>/<int:idword>/', views.repeat, name = 'repeat'),
    path("topic/allearn", views.alllearn, name='alllearn'),









]