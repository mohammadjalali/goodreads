from django.urls import path

from book import views

urlpatterns = [
    path("books/", views.BookAPIView.as_view({"get": "list"}), name="books"),
    path(
        "detail/<int:pk>/",
        views.BookDetailAPIView.as_view({"get": "retrieve"}),
        name="book-detail",
    ),
    path("bookmark/<int:book_pk>/", views.BookMarkModelView.as_view(), name="bookmark"),
    path(
        "bookmarks/",
        views.BookMarkAPIViewset.as_view({"get": "list"}),
        name="bookmarks",
    ),
    path("comment/", views.CommentAPIView.as_view(), name="comment"),
]
