from django.urls import path
from book import views

urlpatterns = [
    path("books/", views.BookAPIView.as_view({"get": "list"}), name="books"),
    path(
        "detail/<int:pk>",
        views.BookDetailAPIView.as_view({"get": "retrieve"}),
        name="book-detail",
    ),
]
