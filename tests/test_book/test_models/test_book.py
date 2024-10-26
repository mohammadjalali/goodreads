from goodreads.book.models import Book


def test_create_book():
    # Arrange
    book = Book(name="test-name", summery="test-summery")

    # Act
    book.save()

    # Assert
    assert Book.objects.count() == 1
    assert Book.objects.filter(id=1).name == "test-name"
