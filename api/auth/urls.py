from django.urls import path

from .views import LoginUser

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
]
