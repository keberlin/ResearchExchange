from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str


class Books:
    def __init__(self):
        # Initialise a set of books
        self.books = []
        self.books.append(Book(111, "Harry Potter"))
        self.books.append(Book(222, "War and Peace"))
        self.books.append(Book(333, "Terminator"))

    def find_by_id(self, id):
        for book in self.books:
            if book.id == id:
                return book
        return None

    def find_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None
