from django.urls import path
from user.views import SignupOrLoginAPIView

urlpatterns = [path("", SignupOrLoginAPIView.as_view())]
