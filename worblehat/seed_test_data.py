import csv
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy

from .models import (
    Bookcase,
    BookcaseLocation,
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
        Bookcase(name='A', description='The first bookcase'),
        Bookcase(name='B', description='The second bookcase'),
    ]

    locations = [
        BookcaseLocation(name='1-1', description='The first location', bookcase=bookcases[0]),
        BookcaseLocation(name='1-2', description='The second location', bookcase=bookcases[0]),
        BookcaseLocation(name='2-1', description='The third location', bookcase=bookcases[1]),
        BookcaseLocation(name='2-2', description='The fourth location', bookcase=bookcases[1]),
    ]

    with open(Path(__file__).parent.parent / 'data' / 'iso639_1.csv') as f:
      reader = csv.reader(f)
      languages = [Language(name, code) for (code, name) in reader]

    db.session.add_all(media_types)
    db.session.add_all(bookcases)
    db.session.add_all(locations)
    db.session.add_all(languages)
    db.session.commit()
    print("Added test media types, bookcases and locations.")