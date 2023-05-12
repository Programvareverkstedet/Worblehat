![worblehat](worblehat.png)

# 👉👁️👄👁️👈

# Worblehat

More information on  <https://www.pvv.ntnu.no/pvv/Bokhyllen/Worblehat/>

## What?

Worblehat is a simple library management system written specifically for Programvareverkstedet.

## Why?

Programvareverkstedet is a small community with many books and games. A simple web platform is needed to manage the library. We need to know who owns each item, if we can loan it out and where it is.

Programvareverkstedet har en rekke bøker, og en konstant tilstrøm av nye.
Teoretisk sett skal disse ryddes og kategoriseres jevntlig, men da dette ikke gjøres ofte nok kan det være et varig strev å finne ut hvor bøker står til enhver tid.
Styret har derfor tatt initiativ til å opprette et biblioteksystem for å systematisere bøkene.
Prosjektet har fått navn Worblehat etter en bibliotekar i Terry Pratchetts discworld serie.
Worblehatt har vært påbegynnt flere ganger opp gjennom historien uten å komme i noen form for funksjonell tilstand enda.

## How?

The application is split into frontend and backend. The frontend is written with react-scripts, and communicates with the backed through a REST api.

The backend is written in Flask, and uses an ORM(SQLAlchemy) to store the data in any kind of SQL database.

# Technical details

## Setup

This project uses [poetry][poetry] as its buildtool as of May 2023.

```console
$ poetry install
$ poetry run alembic migrate
$ poetry run cli
$ poetry run dev
```

## How to configure

See `worblehat/config.py` for configurable settings.

## TODO List

- [ ] High priority:
  - [X] Data ingestion logic, that will pull data from online databases based on ISBN.
  - [ ] Cli version of the program (this is currently being worked on).
  - [ ] Web version of the program
  - [ ] Setting up a database with all of PVVs books
    - [ ] Creating database with user and pw
    - [ ] Model all bookshelfs
    - [ ] Scan in all books
  - [ ] Inner workings
    - [X] Ability to create and update bookcases
    - [X] Ability to create and update bookcase shelfs
    - [X] Ability to create and update bookcase items
    - [X] Ability to request book loans for PVV members
    - [X] Ability to queue book loans for PVV members
    - [X] Ability to be notified when deadlines are due
    - [ ] Ability to be notified when books are available
    - [ ] Ability to search for books
    - [ ] Ability to print PVV-specific labels for items without a label, or for any other reason needs a new one
    - [ ] Ascii art of monkey
- [ ] Low priority:
  - [ ] Ability for PVV members to request book loans through the PVV website
  - [ ] Ability for PVV members to search for books through the PVV website
- [ ] Discussion
  - [ ] Should this project run in a separate tty-instance on Dibblers interface, or should they share the tty with some kind of switching ability?
  After some discussion with other PVV members, we came up with an idea where we run the programs in separate ttys, and use a set of large mechanical switches connected to a QMK-flashed microcontroller to switch between them.
  - [ ] Workaround for not being able to represent items with same ISBN and different owner: if you are absolutely adamant about placing your item at PVV while still owning it, even though PVV already owns a copy of this item, please print out a new label with a "PVV-ISBN" for it