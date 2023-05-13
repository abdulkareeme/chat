from django.urls import path
from . import views
from django.views.generic.base import TemplateView
urlpatterns = [
    path('call/<str:username>',  views.ListMessages.as_view(), name='message-list'),
    path('test' , TemplateView.as_view(template_name = 'conversation/room.html') ),
    path('test2', TemplateView.as_view(template_name = 'conversation/room2.html'))
]