import csv
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy

from .models import (
    Bookcase,
    BookcaseShelf,
    Language,
    MediaType,
)

def seed_data(db: SQLAlchemy):
    media_types = [
        MediaType(name='Book', description='A physical book'),
        MediaType(name='Comic', description='A comic book'),
        MediaType(name='Video Game', description='A digital game for computers or games consoles'),
        MediaType(name='Tabletop Game', description='A physical game with cards, boards or similar')
    ]

    bookcases = [
        Bookcase(name='Unnamed A', description='White case across dibbler'),
        Bookcase(name='Unnamed B', description='Math case in the working room'),
        Bookcase(name='Unnamed C', description='Large case in the working room'),
        Bookcase(name='Unnamed D', description='White comics case in the hallway'),
        Bookcase(name='Unnamed E', description='Wooden comics case in the hallway'),
    ]

    shelfs = [
        BookcaseShelf(row=0, column=0, bookcase=bookcases[0]),
        BookcaseShelf(row=1, column=0, bookcase=bookcases[0]),
        BookcaseShelf(row=2, column=0, bookcase=bookcases[0]),
        BookcaseShelf(row=3, column=0, bookcase=bookcases[0], description="Hacking"),
        BookcaseShelf(row=4, column=0, bookcase=bookcases[0], description="Hacking"),

        BookcaseShelf(row=0, column=1, bookcase=bookcases[0]),
        BookcaseShelf(row=1, column=1, bookcase=bookcases[0]),
        BookcaseShelf(row=2, column=1, bookcase=bookcases[0], description="DOS"),
        BookcaseShelf(row=3, column=1, bookcase=bookcases[0], description="Food for thought"),
        BookcaseShelf(row=4, column=1, bookcase=bookcases[0], description="CPP"),

        BookcaseShelf(row=0, column=2, bookcase=bookcases[0]),
        BookcaseShelf(row=1, column=2, bookcase=bookcases[0]),
        BookcaseShelf(row=2, column=2, bookcase=bookcases[0], description="E = mc2"),
        BookcaseShelf(row=3, column=2, bookcase=bookcases[0], description="OBJECTION!"),
        BookcaseShelf(row=4, column=2, bookcase=bookcases[0], description="/home"),

        BookcaseShelf(row=0, column=3, bookcase=bookcases[0]),
        BookcaseShelf(row=1, column=3, bookcase=bookcases[0], description="Big indonisian island"),
        BookcaseShelf(row=2, column=3, bookcase=bookcases[0]),
        BookcaseShelf(row=3, column=3, bookcase=bookcases[0], description="Div science"),
        BookcaseShelf(row=4, column=3, bookcase=bookcases[0], description="/home"),

        BookcaseShelf(row=0, column=4, bookcase=bookcases[0]),
        BookcaseShelf(row=1, column=4, bookcase=bookcases[0]),
        BookcaseShelf(row=2, column=4, bookcase=bookcases[0], description="(not) computer vision"),
        BookcaseShelf(row=3, column=4, bookcase=bookcases[0], description="Low voltage"),
        BookcaseShelf(row=4, column=4, bookcase=bookcases[0], description="/home"),

        BookcaseShelf(row=0, column=5, bookcase=bookcases[0]),
        BookcaseShelf(row=1, column=5, bookcase=bookcases[0]),
        BookcaseShelf(row=2, column=5, bookcase=bookcases[0], description="/home"),
        BookcaseShelf(row=3, column=5, bookcase=bookcases[0], description="/home"),

        BookcaseShelf(row=0, column=0, bookcase=bookcases[1]),
        BookcaseShelf(row=1, column=0, bookcase=bookcases[1], description="Kjellerarealer og komodovaraner"),
        BookcaseShelf(row=2, column=0, bookcase=bookcases[1]),
        BookcaseShelf(row=3, column=0, bookcase=bookcases[1], description="Quick mafs"),
        BookcaseShelf(row=4, column=0, bookcase=bookcases[1]),

        BookcaseShelf(row=0, column=0, bookcase=bookcases[2]),
        BookcaseShelf(row=1, column=0, bookcase=bookcases[2]),
        BookcaseShelf(row=2, column=0, bookcase=bookcases[2], description="AI"),
        BookcaseShelf(row=3, column=0, bookcase=bookcases[2], description="X86"),
        BookcaseShelf(row=4, column=0, bookcase=bookcases[2], description="Humanoira"),
        BookcaseShelf(row=5, column=0, bookcase=bookcases[2], description="Hvem monterte rørforsterker?"),

        BookcaseShelf(row=0, column=1, bookcase=bookcases[2]),
        BookcaseShelf(row=1, column=1, bookcase=bookcases[2], description="Div data"),
        BookcaseShelf(row=2, column=1, bookcase=bookcases[2], description="Chemistry"),
        BookcaseShelf(row=3, column=1, bookcase=bookcases[2], description="Soviet Phys. Techn. Phys"),
        BookcaseShelf(row=4, column=1, bookcase=bookcases[2], description="Digitalteknikk"),
        BookcaseShelf(row=5, column=1, bookcase=bookcases[2], description="Material"),

        BookcaseShelf(row=0, column=2, bookcase=bookcases[2]),
        BookcaseShelf(row=1, column=2, bookcase=bookcases[2], description="Assembler / APL"),
        BookcaseShelf(row=2, column=2, bookcase=bookcases[2], description="Internet"),
        BookcaseShelf(row=3, column=2, bookcase=bookcases[2], description="Algorithms"),
        BookcaseShelf(row=4, column=2, bookcase=bookcases[2], description="Soviet Physics Jetp"),
        BookcaseShelf(row=5, column=2, bookcase=bookcases[2], description="Død og pine"),

        BookcaseShelf(row=0, column=3, bookcase=bookcases[2]),
        BookcaseShelf(row=1, column=3, bookcase=bookcases[2], description="Web"),
        BookcaseShelf(row=2, column=3, bookcase=bookcases[2], description="Div languages"),
        BookcaseShelf(row=3, column=3, bookcase=bookcases[2], description="Python"),
        BookcaseShelf(row=4, column=3, bookcase=bookcases[2], description="D&D Minis"),
        BookcaseShelf(row=5, column=3, bookcase=bookcases[2], description="Perl"),

        BookcaseShelf(row=0, column=4, bookcase=bookcases[2]),
        BookcaseShelf(row=1, column=4, bookcase=bookcases[2], description="Knuth on programming"),
        BookcaseShelf(row=2, column=4, bookcase=bookcases[2], description="Div languages"),
        BookcaseShelf(row=3, column=4, bookcase=bookcases[2], description="Typesetting"),
        BookcaseShelf(row=4, column=4, bookcase=bookcases[2]),

        BookcaseShelf(row=0, column=0, bookcase=bookcases[3]),
        BookcaseShelf(row=0, column=1, bookcase=bookcases[3]),
        BookcaseShelf(row=0, column=2, bookcase=bookcases[3]),
        BookcaseShelf(row=0, column=3, bookcase=bookcases[3]),
        BookcaseShelf(row=0, column=4, bookcase=bookcases[3]),

        BookcaseShelf(row=0, column=0, bookcase=bookcases[4]),
        BookcaseShelf(row=0, column=1, bookcase=bookcases[4]),
        BookcaseShelf(row=0, column=2, bookcase=bookcases[4]),
        BookcaseShelf(row=0, column=3, bookcase=bookcases[4]),
        BookcaseShelf(row=0, column=4, bookcase=bookcases[4], description="Religion"),
    ]

    with open(Path(__file__).parent.parent / 'data' / 'iso639_1.csv') as f:
      reader = csv.reader(f)
      languages = [Language(name, code) for (code, name) in reader]

    db.session.add_all(media_types)
    db.session.add_all(bookcases)
    db.session.add_all(shelfs)
    db.session.add_all(languages)
    db.session.commit()
    print("Added test media types, bookcases and shelfs.")