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

## TODO

### Funksjonalitet

* Høy prioritet:
  * Bokdatabase med alle PVVs bøker må lages
  * Bokdatabasebyggingsverktøy for å bygge bokdatabasen (sjekker online ISBN-database for informasjon om boken)
  * Utlånsmuligheter på PVVs lokaler for eksempel gjennom Dibbler sin strekkodescanner
* Lav prioritet:
  * Utlånsmuligheter gjennom nettportal på PVVs nettsider
  * Søkemuligheter gjennom en nettportal på PVVs nettsider
* Til diskusjon:
  * Skal Worblehat kjøre i en annen tty-instans på Dibbler sin Raspberry Pi ELLER skal man skifte mellom Worblehat-mode og Dibbler-mode i samme tty?

### Ellers

* Legge til håndtering av flere ISBN-databaser
* Legge til batch-prosessering av ISBN-er
  * For å kunne scanne en hel hylle og så dumpe hele listen av ISBN-er til databasene vi henter fra
* Lage en database vi kan lagre _våre_ bøker i
* Finne en måte å håndtere kollisjon dersom vi har flere eksemplarer av samme bok
  * Klistremerke med eksemplar-nummer ved siden av ISBN, kanskje
* Se om <https://pypi.org/project/isbntools/> er et nyttig verktøy for arbeidet vårt

## Tilfeldig

En relativt stor online ISBN-database er lokalisert:

* <https://openlibrary.org//>
  * Eksporterer json-objekter med alle mulig slags rare felter
* google books databasen er også mulig å benytte.
* Kanskje ISBNdb.com er mulig å benytte også.

Noen viktige felter til databasen er som følger:

* ISBN (faktisk eller pvv generert)
* Forfatter
* Tittel
* Utgivelsesår
* Antall sider
* Sjanger
* Språk
* Om boken er utlånbar
* Bruker som har lånt boken
* Dato på når boken ble lånt ut

Prosedyre for bokdatabasebygging:

* Systematisk arbeid, hylle for hylle
* Tre bunker: "ikke scannet", "scannet" og "manuell innlegging"
* Scanning sjekker live om info kan hentes fra online database(r)
* Dersom finnes: legg i "scannet", ellers legg i "manuell innlegging"
* Legg inn manuelle bøker
* Sett tilbake i hyllen og fortsett til neste

Ny (alternativ) prosedyre:

1. Ta ut alle bøker fra en hylle
2. Batch-scan isbner; skill så bøker med og uten isbn (scannet- og manuell-bunke)
3. Få isbntools til å hente metadata for listen med isbner; dersom den ikke finner noe, legg boken i manuell-bunken
4. Sett alle scannede bøker tilbake og gå gjennom manuell-bunken
5. Sett alt tilbake og ferdiggjør csv-en eller hva enn for den spesifike hyllen

Programmvare utviklet:

* Enkelt python og JS script for uthenting av data fra database(r) gitt isbn.

## TODO

* Legge til håndtering av flere ISBN-databaser
  * isbntools ser ut til å finne en del ting som openlibrary ikke finner alene
* Legge til batch-prosessering av ISBN-er
  * For å kunne scanne en hel hylle og så dumpe hele listen av ISBN-er til databasene vi henter fra
* Lage en database vi kan lagre _våre_ bøker i
* Finne en måte å håndtere kollisjon dersom vi har flere eksemplarer av samme bok
  * Klistremerke med eksemplar-nummer ved siden av ISBN, kanskje
* Se om <https://pypi.org/project/isbntools/> er et nyttig verktøy for arbeidet vårt
  * Ser nyttig ut
