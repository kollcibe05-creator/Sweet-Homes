# Sweet Homes

##### A full-stack web application for managing Airbnb's, featuring a React frontend and a RESTful Flask backend!

## Description
Sweet Homes is Flask-SQLAlchemy + PostgreSQL + React software aimed at resolving the complexity of making reservations while maintainig  data consistency and persisting the changes to the Database. It implements flask-sqlalchemy, relational databases, API best practices using flask-restful and OOP to model the database and ensure accuracy while accessing the data.

The ideological business requirements are:

1. A `User `has many  `Roles`s but generally restricted to some via authorization.
2. A `User` can have  many `Houses`s through `Bookings`.
3. An `User` can have many `review`.
4. A `house` can have many `reviews`.
5. A `User` can have many `favorites`.
6. A `House` can only have *one* `Booking`.
7. A `User` can have many `Booking`s. 
_______
The ERD model of the relationships;
![alt text](https://dbdiagram.io/d/6964500ed6e030a024b68fca)
_______
The models incorporate serialize_rules and association_proxies to limit recursion depth and simplify cross-model data access.
## Tech Stack
- Python
- SQL
- Markdown
- React
- PostgreSQL
- Render

## File Structure

Take a look at the directory structure:

```console
    .
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── domain.png
└── server
    ├── app.py
    ├── instance
    │   └── app.db
    ├── migrations
    │   ├── README
    │   ├── alembic.ini
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions
    │       └── 4e55fcdd2cde_initial_migration.py
    ├── models.py
    └── seed.py
```


## Generating Your Environment

You might have noticed in the file structure- there's  a Pipfile!

Install  the dependencies  you'll need to navigate the file by 
adding them to the `Pipfile`. Run the commands:

```console
pipenv install
pipenv shell
```


## Environment Configurations Setup
To start working with the data  you need to:
1. Navigate to */server* dir:
```
cd server

```
2. Configure the flask environment commands:
```
    export FLASK_APP=app.py
    export FLASK_RUN_PORT=5555

```
This will allow you to start the server using :
```
flask run

```    
The commands below have been run for you:
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade head
python seed.py

```
To run the app and benefit from the debugger, use:
```shell
python app.py

```
Running it requires that you are in the */server* dir;
```bash
    cd server

```

## Functionality
# models.py
Our models import from `db.Model` and `SerializerMixin`.
The have similar constructors such as:
1. *__repr__*: In it is the modified output of a class instance to improve clarity.
2. *__tablename__*: Specifies the table in the database that the objects will be mapped to.
3. *serialize_rules*: It states the fields to be excluded to prevent recursion depth.
4. *association_proxy*: It simplifies access to the cross-model fields and data. 
5. @validates : a decorator that ensures that rating is between 1 and 5.

The models are:
- Guest
- Appearance ~ The association object.
- Episode


# app.py
The views are Resources from `flask-restful` which ensures they are RESTful registration to routes.
The basic functionalities that can be ensued are:
1. (GET)*episodes()*: GET request to */episodes*.
2. (GET)*get_episodes(id)*: Takes id as an argument and implements GET to the */episodes/:id*.
3. (GET)*guests()*: GET request to */guests*.
4. (GET, PATCH)*get_guests(id)*: Takes id as an argument and implements GET and PATCH to the */powers/:id*.
5. (GET, POST)*post()*: POST to *appearances*. 

# seed.py
It contains the data seeded to the `app.db`

# app.db
It holds our SQL database.





# Author
*Collins Kibet*

## [License](LICENSE)

MIT License
Copyright (c) 2025 Collins Kibet


# Contact info
* Email : kollcibe05@gmail.com


`(**Thank you**)`