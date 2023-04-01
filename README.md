# Worblehat

## What?
Worblehat is a simple library management system written specifically for Programvareverkstedet.

## Why?
Programvareverkstedet is a small community with many books and games. A simple web platform is needed to manage the library. We need to know who owns each item, if we can loan it out and where it is.

## How?
The entire application is written in flask. 

Flask functions as a web server, and uses an ORM(SQLAlchemy) to store the data in an SQLite database.

The resulting web page is rendered on the server by jinja templates in flask.


# Technical Details
## How to install

* Make a `.env` file with a secret key.
  * `$ echo "SECRET_KEY=<secret>" > .env`
* Make a virtualenv
  * `$ python3 -m venv venv`
* Activate the virtualenv
  * `$ source venv/bin/activate`
* Install the requirements
  * `$ pip install -r requirements.txt`

## How to configure

* Make changes in the function "`reset_db()`" in `worblehat/__init__.py` if needed
* run `$ flask --app worblehat --debug resetdb`


## Requirements
### System / Package Manager
* Python >= 3.6
* Pip 

### Python packages
* See [requirements.txt](requirements.txt)
