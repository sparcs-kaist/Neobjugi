from django.conf.urls import include, url
from chatbot import views 


urlpatterns = [
    url(r'^6ee3e8678bcb1795ad6a221ca3ea16349947c4a492ae1dad40/?$', views.ChatView.as_view()),
]
