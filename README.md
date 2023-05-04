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
$ poetry run scanner
$ poetry run dev
```

## How to configure

See `worblehat/config.py` for configurable settings.

## TODO List

- [ ] High priority:
  - [ ] Book ingestion tool in order to create the database in a quick manner. It should pull data from online ISBN databases (this is almost done)
  - [ ] A database with all of PVVs books should be created
  - [ ] Ability to request book loans for PVV members, e.g. through Dibblers interface.
- [ ] Low priority:
  - [ ] Ability for PVV members to request book loans through the PVV website
  - [ ] Ability for PVV members to search for books through the PVV website
- [ ] Discussion
  - [ ] Should this project run in a separate tty-instance on Dibblers interface, or should they share the tty with some kind of switching ability?