"""
This script is part of the initial database construction for Worblehat.
The idea is that the script will:
* Prompt the user for which bookcase and shelf we're scanning
* Scan ISBN's until the user says we're done
* Also take a note for each ISBN
* Dump a csv with the columns: ISBN, bookcase, shelf, note
"""

from isbnlib import is_isbn10, is_isbn13

def validate_isbn(isbn):
    if len(isbn) == 10:
        return is_isbn10(isbn)
    elif len(isbn) == 13:
        return is_isbn13(isbn)
    elif len(isbn) == 1:
        return isbn
    else:
        return False

def write_csv(bookcase, shelf, isbns, notes, fname="isbns"):
    f = open(fname + "_" + bookcase + "_" + shelf + ".csv", "w")
    f.write("isbn, note, bookcase, shelf\n")

    for isbn, note in zip(isbns, notes):
        f.write(f"{isbn}, {note}, {bookcase}, {shelf}\n")

    f.close()

if __name__ == "__main__":
    bookcase = input("Bookcase: ")
    shelf = input("Shelf: ")

    should_get_isbn = True
    isbns = []
    notes = []
    i = 0
    print("Input q as ISBN to quit.")
    while should_get_isbn:
        i += 1
        has_valid_isbn = False
        while not has_valid_isbn:
            isbn = input(f"ISBN no. {i}: ")
            has_valid_isbn = validate_isbn(isbn)
            if not has_valid_isbn:
                print("Invalid ISBN, trying again.")
        
        note = input(f"Note for ISBN {isbn}: ")

        if len(isbn) > 1:
            isbns.append(isbn)
            notes.append(note)
        else:
            should_get_isbn = False

    print(isbns)
    print(notes)

    write_csv(bookcase, shelf, isbns, notes)