from django.urls import path
from . import tests

urlpatterns = [
    path('test/', tests.testdb),
]