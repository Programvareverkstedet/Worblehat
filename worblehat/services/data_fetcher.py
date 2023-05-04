# A simple script to fetch bookdata from multiple sources to the library format.
# Felter hver bok bør ha: (pr. 01.04.2023)
# ISBN
# Forfatter
# Tittel
# Utgivelsesår
# Antall sider
# Sjanger
# Språk
# Bruker som har lånt boken
# Dato på når boken ble lånt ut

import requests
import json

def get_isbn():
    # TODO: validate ISBN using checksums
    # TODO: wrap in a loop until either ISBN is valid or user quits
    # isbn = 9780135166307 #input gir ett isbn 10 eller 13 nummer   # kaster en error.
    # isbn = "0801859034" #input gir ett isbn 10 eller 13 nummer

    isbn = input("Scan a book or add manually: ") # input gir ett isbn 10 eller 13 nummer
    if (len(isbn) == 10 or len(isbn) == 13):
        return isbn
    else:
        return None

def get_from_api(isbn):
    try:
        json_input = json.loads(requests.get("https://openlibrary.org/isbn/"+str(isbn)+".json").text)
    except:
        return f"Error fetching data for: {isbn}"  # TODO: add more databases for fetching info from

    try:
        authors = json_input.get("authors")
        for i in range(len(authors)):
            authors[i] = json.loads(requests.get("https://openlibrary.org"+str(authors[i].get("key"))+".json").text).get("name") #henter navn fra api

        authors = list(set(authors))
        title = json_input.get("title")
        publish_date = json_input.get("publish_date")
        number_of_pages = json_input.get("number_of_pages")
        languages = json_input.get("languages")

        for i in range(len(languages)):
            languages[i] = json.loads(requests.get("https://openlibrary.org"+str(languages[i].get("key"))+".json").text).get("name")

        book_data = {
                    "isbn": isbn,
                    "authors": authors,
                    "title": title,
                    "publish_date": publish_date,
                    "number_of_pages": number_of_pages,
                    "languages": languages,
                    }

        return book_data

    except:
        return f"Error processing data for: {isbn}"

def push_to_database(book_info, db_file = "book_info.dat") -> None:
    print(f"Pushing to database: Writing to file {db_file}")  # TODO: actually connect to our database and push there
    f = open(db_file, "w")
    json.dump(book_info, f)
    f.close()


def validate_book_info_with_user(book_info) -> bool:
    """
    Takes a book_info dictionary and asks the user to update fields until they're satisfied with the information.
    Updates the inputted dictionary directly.

    Input:
    * book_info: dict holding fields of book information

    Returns:
    * bool: True if book is now valid, false if something went wrong
    """
    print("Is the following information correct?")
    print(book_info)

    answer = input("y/n: ")
    if answer == "n":
        print("What is wrong?")
        incorrrect_category = input("""
        1. Authors
        2. ...
        3. ...
        q. Quit (done/continue)
        """)
        is_corrected = False

        while not is_corrected:
            if incorrrect_category == "1":
                authors = input("Input correct authors separated by ',': ")
                #TODO: actually put the authors into the book info json thing
            elif incorrrect_category =="q":
                is_corrected = True
            else:
                print("No valid option supplied.")

        return True  # Book has been corrected and is (presumably) valid
    elif answer == "y":
        return True  # Book information is valid
    else:
        return False  # Something went wrong

def add_book_location(book_info) -> None:
    """
    Prompts the user for which bookcase and shelf the book came from and adds them to the book_info dictionary.

    Inputs:
    * book_info: dict holding the book information

    Returns:
    * None: the book_info dict is updated diretly
    """
    print("Where is the book located?")

    bookcase = input("Bookcase: ")
    shelf = input("Shelf: ")

    book_info["bookcase"] = bookcase
    book_info["shelf"] = shelf

if __name__ == '__main__':
    is_running = True
    while is_running:
        # Asking user for ISBN and fetching data online
        isbn = get_isbn()
        if isbn is not None:
            book_info = get_from_api(isbn)
            print(f"Fetched: {book_info}")
        else:
            book_info = {}
            print("Error: Inputted ISBN was invalid.")

        # Adding physical location (case, shelf) to the book
        add_book_location(book_info)

        # Ensuring the user is satisfied with the information
        book_is_correct = validate_book_info_with_user(book_info)

        # Pushing to the database to commit the valid book
        if book_is_correct:
            print("Should we push this book to the database?")
            push_answer = input("y/n: ")
            if push_answer == "y":
                push_to_database(book_info)
            else:
                pass
        else:
            print("Error: Book was not corrected properly, we might try again.")

        # Moving on to the next book which should be added to the library
        print("Should we continue?")
        cont_answer = input("y/n: ")
        if cont_answer == "y":
            is_running = True
        else:
            is_running = False

