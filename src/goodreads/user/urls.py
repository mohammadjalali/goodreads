from django.urls import path

from goodreads.user.views import SignupOrLoginAPIView


urlpatterns = [path("", SignupOrLoginAPIView.as_view())]
