import isbnlib

from ..models import (
    Author,
    BookcaseItem,
)

def is_valid_isbn(isbn: str) -> bool:
    return any([
        isbnlib.is_isbn10(isbn),
        isbnlib.is_isbn13(isbn),
    ])

def create_bookcase_item_from_isbn(isbn: str) -> BookcaseItem | None:
    metadata = isbnlib.meta(isbn)
    if len(metadata.keys()) == 0:
        return None

    bookcase_item = BookcaseItem(
        name = metadata.get('Title'),
        isbn = int(isbn.replace('-', '')),
    )

    if len(authors := metadata.get('Authors')) > 0:
        for author in authors:
            bookcase_item.authors.add(Author(author))

    if (language := metadata.get('language')):
        bookcase_item.language = language

    return bookcase_item