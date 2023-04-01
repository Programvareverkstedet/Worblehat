from data_fetcher import get_from_api

import json
from isbnlib import meta

if __name__ == "__main__":
    # fname = input("File to operate on: ")
    fname = "./bokhyller/arbeidsrom_smal_hylle_5.csv"

    with open(fname, "r") as f:
        fields = f.readline().strip("\n").split(", ")

        books = []

        for line in f:
            a = line.strip("\n").split(", ")
            d = {}
            for i in range(len(fields)):
                d[fields[i]] = a[i]
            books.append(d)

    # for b in books:
    #     print(b)
    book_infos = []
    # for book in books:
    #     bi = get_from_api(book["isbn"])
    #     if type(bi) is dict:
    #         bi["bookcase"] = book["bookcase"]
    #         bi["shelf"] = book["shelf"]
    #     book_infos.append(json.dumps(bi))

    for book in books:
        bi = json.dumps(meta(book["isbn"]))
        print(bi)
        book_infos.append(bi)

    # for bi in book_infos:
    #     print(bi)

