from django.urls import path

from api.views.book_review_views import *


app_name = 'book_review'

urlpatterns = [
    path('add/', add_review, name='add'),
    path('edit/<int:pk>/', edit_review, name='edit'),
]