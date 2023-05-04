import json
import isbnlib
from data_fetcher import get_from_api

def make_isbnlib_comliant(meta):
    if meta:
        book_info = {
            "isbn": meta["ISBN-13"],
            "authors": meta["Authors"],
            "title": meta["Title"],
            "publish_date": meta["Year"],
            "number_of_pages": None,
            "languages": [meta["Language"]],
        }

        return book_info
    else:
        return meta


if __name__ == "__main__":
    fname = input("File to operate on: ")
    # fname = "./bokhyller/arbeidsrom_smal_hylle_5.csv"
    # fname = ".\\bokhyller\\arbeidsrom_smal_hylle_5"

    with open(fname + ".csv", "r") as f:
        fields = f.readline().strip("\n").split(", ")
        books = []
        for line in f:
            values = line.strip("\n").split(", ")
            book = {}
            for i in range(len(fields)):
                book[fields[i]] = values[i]
            books.append(book)

    book_infos = []

    for book in books:
        print(f"Attempting to fetch information for: {book['isbn']}")
        book_info = get_from_api(book["isbn"])

        if type(book_info) is not dict:
            try:
                book_info = make_isbnlib_comliant(isbnlib.meta(book["isbn"]))
            except:
                print(f"isbnlib failed for book: {book['isbn']}")

        if not book_info:
            book_info = book

        book_info["bookcase"] = book["bookcase"]
        book_info["shelf"] = book["shelf"]
        book_infos.append(json.dumps(book_info))

    with open(fname + ".dat", "w") as f:
        for book_info in book_infos:
            f.write(book_info + "\n")
