
from django.urls import path
from .views import check,home
urlpatterns = [
    path("",home),
    path('check/', check),
]
