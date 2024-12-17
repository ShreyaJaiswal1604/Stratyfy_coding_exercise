# Stratyfy coding exercise

## Introduction

Attached is data representing sales at an ice cream parlor.  Please download the data and set up a database to store it and an API to access the database.

Please feel free to stop or contact us if you find the exercise taking more than a few hours; we don't want to use large amounts of your time.

## Template

Because setting up a backend stack can involve a lot of boilerplate, we've provided a template project for your convenience.  It uses:

* Python with packages managed by [Poetry](https://python-poetry.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [sqlite](https://www.sqlite.org/) (At Stratyfy we use Postgres; sqlite is standing in for it as a fully local analog.)

These happen to be some of the tools we use at Stratyfy, but we don't mind at all if you prefer different ones.  As long as your sample meets the objectives below, you are welcome to use as much or as little of the template as you like, as well as to bring in additional packages.

To use the template with Poetry, first install Poetry according to the instructions, then run
```
poetry install
poetry run fastapi dev exercise.py
```
If all is well, you should be able to browse to the template API's built-in documentation at http://localhost:8000/docs, and see its test endpoint at http://localhost:8000/test.


## Specification

### Database

The data contains two files:

* `sundaes.json` gives the menu of available sundaes.
* `sales.json` gives a set of sale transactions.  The `timestamp` column is a Unix timestamp.

Set up a database to hold this data and provide code to load the data into the database.  You should imagine that in practice a different service will be writing to this database continuously, so it is *not* appropriate to use the data directly without loading it into a database.

Note that during the interview we may replace these data files.  The template is set up to create a new temporary database in memory each time it is run, but if you choose to use a different database, you may need a fast way to update the schema and load the new data.

### API

Set up an API with two endpoints, both returning JSON:

* `GET /sundaes` should return all the available sundaes as an array of objects, like the original seed data.
* `GET /sundaes/{id}` should return a single sundae object with the following additional fields:
  - `volume`, the number of sundaes sold
  - `revenue`, the total revenue for this type of sundae over all available transactions

You should gracefully handle common error case(s) in an appropriate fashion.

When you're happy with your work, please share it with us, e.g. by sharing a GitHub repo.  Please don't hesitate to ask if anything is unclear or troublesome.

## Interview

Obviously, the initial implementation of a piece of code is only a small fraction of its life; as such, we are interested in your ability to adapt to changing requirements, like all coders face in the real world.

Please come to your interview with your code loaded in an environment where you are comfortable changing it and viewing the results, and be prepared to share your screen.
