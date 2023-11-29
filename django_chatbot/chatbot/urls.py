from django.urls import path,include
from . import views 


urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('login/', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

#     path('social-auth/', include('social_django.urls', namespace='social')),
 ]