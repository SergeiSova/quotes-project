from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_quote, name='add_quote'),
    path('top/', views.top_quotes, name='top_quotes'),
    path('quote/<int:pk>/like/', views.like_quote, name='like_quote'),
    path('quote/<int:pk>/dislike/', views.dislike_quote, name='dislike_quote'),
]