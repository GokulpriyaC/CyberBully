from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),  # Registration page as homepage
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('clear/', views.clear_chat, name='clear_chat'),
    path('report/', views.report_fake_profile, name='report'),
]
