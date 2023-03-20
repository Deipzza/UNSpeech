from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from . import views

from render import bot

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('webhooks/bot/', csrf_exempt(bot.bot.as_view())),
]