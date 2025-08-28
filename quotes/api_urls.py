from django.urls import path
from . import api_views

urlpatterns = [
    path('quote/random/', api_views.RandomQuote.as_view()),
    path('quote/<int:pk>/vote/', api_views.VoteQuote.as_view()),
    path('quotes/add/', api_views.AddQuote.as_view()),
    path('quotes/top/', api_views.TopQuotes.as_view()),
]
