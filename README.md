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

# Technical details

## Setup

This project uses [poetry][poetry] as its buildtool as of May 2023.

```console
$ poetry install
$ poetry run alembic migrate
$ poetry run worblehat --help
```

## How to configure

See `config.template` for configurable settings.

Unless provided through the `--config` flag, program will automatically look for a config file in these locations:

- `./config.toml`
- `~/.config/worblehat/config.toml`
- `/var/lib/worblehat/config.toml`

Run `poetry run worblehat --help` for more info

## TODO List

### Setting up a database with all of PVVs books

- [ ] Create postgres database
- [ ] Model all bookshelfs
- [ ] Scan in all books

### Cli version of the program (this is currently being worked on)

- [X] Ability to pull data from online sources with ISBN
- [X] Ability to create and update bookcases
- [X] Ability to create and update bookcase shelfs
- [X] Ability to create and update bookcase items
- [X] Ability to borrow and deliver items
- [ ] Ability to borrow and deliver multiple items at a time
- [X] Ability to enter the queue for borrowing an item
- [ ] Ability to extend a borrowing, only if no one is behind you in the queue
- [ ] Ability to list borrowed items which are overdue
- [~] Ability to search for items
- [ ] Ability to print PVV-specific labels for items missing a label, or which for any other reason needs a custom one
- [ ] Ascii art of monkey with fingers in eyes

### Deadline daemon

- [X] Ability to be notified when deadlines are due
- [ ] Ability to be notified when books are available
- [ ] Ability to have expiring queue positions automatically expire

### Web version of the program

- [ ] Ability for PVV members to search for books through the PVV website

## Points of discussion

- Should this project run in a separate tty-instance on Dibblers interface, or should they share the tty with some kind of switching ability?
After some discussion with other PVV members, we came up with an idea where we run the programs in separate ttys, and use a set of large mechanical switches connected to a QMK-flashed microcontroller to switch between them.

- Workaround for not being able to represent items with same ISBN and different owner: if you are absolutely adamant about placing your item at PVV while still owning it, even though PVV already owns a copy of this item, please print out a new label with a "PVV-ISBN" for it