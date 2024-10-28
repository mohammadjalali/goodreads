from book import views
from django.urls import path

urlpatterns = [
    path("books/", views.BookAPIView.as_view({"get": "list"}), name="books"),
    path(
        "detail/<int:pk>/",
        views.BookDetailAPIView.as_view({"get": "retrieve"}),
        name="book-detail",
    ),
    path("bookmark/<int:book_pk>/", views.BookMarkAPIView.as_view(), name="bookmark"),
    path(
        "bookmarks/",
        views.BookMarkAPIViewset.as_view({"get": "list"}),
        name="bookmarks",
    ),
    path("comment/", views.CommentAPIView.as_view(), name="comment"),
]
