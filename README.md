# Capstone Final Project

## Casting Agency App

This app is a backend API which models a company that is responsible for creating movies and managing and assigning actors to those movies.

### Installing Dependencies to locally run app

1. **Python 3.9** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Environment** - This keeps your dependencies for each project separate and organised. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies:
```
pip install -r requirements.txt
```

4. **Environment Variables** You will first need to populate your `setup.sh` script with your own database credentials, e.g.:

```
#!/bin/bash
export DATABASE_URL="postgresql://joe@localhost:5432/capstone"
export TEST_DATABASE_URL="postgresql://joe@localhost:5432/capstone_test"
echo "setup.sh script executed successfully!"
```
Then run the `setup.sh` script to set up your database environment variables as well as auth0 parameters and sample JWT_TOKEN for `test_app.py`. 

### Local Database Setup


Assuming you have postgres running locally, create a local database called `capstone`:

```
dropdb capstone
createdb capstone
```

The dropdb command is only required if you wish to delete an already existing `capstone` database that you have created.

The app has been designed to populate the database with sample Movie and Actor data when it is run if the 'capstone' database is empty of records. See `sample_data.py` for the sample data. Uncomment the following section in `app.py` and run to populate the database on first run:

```
# #########################################
# # PREPOPULATE DATABASE WITH SAMPLE DATA IF EMPTY
# # Uncomment and run app to insert sample data

# # Add sample movies to db if empty
# if not Movie.query.order_by(Movie.id).all():
#   for movie in movies:
#     movie.insert()

# # Add sample actors to db if empty
# if not Actor.query.order_by(Actor.id).all():
#   for actor in actors:
#     actor.insert()
# #########################################
```

**Recomment the lines of code in `app.py` to ensure this does not run again.**


The app will create a movies and actors table to represent the Movie and Actor models. There is a many-to-many relationship between these models as one movie can have many actors and one actor can star in many movies.


### Tests

There have been tests that have been configured in `test_app.py`. A sample JWT for an Executive Producer has been included in the header for each test so that it will run. This JWT can be found in `setup.sh`.

Assuming you have postgres running locally, create a local database called `capstone_test`:

```
dropdb capstone_test
createdb capstone_test
```
The first time you run the tests, omit the dropdb command. 

As with the local database for running the app, the test database can be prepopulated by uncommenting a similar section of code in `test_app.py` on first run as described above.

In order to run tests in `test_app.py`, run the following command: 

```
pytest test_app.py
```


### Getting Started
- At present this app can be run locally. The app is hosted at the default: `http://127.0.0.1:8080/`

- Hosted: There is a version of this app currently hosted on Heroku at - `https://udacity-capstone-1537268.herokuapp.com/`

### Role Based Access Control (RBAC)

- Authentication: This version of the application does require authentication. Unit tests and a Postman collection (`udacity-capstone-heroku.postman_collection.json`) have been included for each of the available roles and these include a temporarily valid JWT for each role.

The credentials for the roles are below:

  - Casting Assistant
    - username: `thisisacastingassistant@gmail.com`
    - password: H3Ll0mYfR13nD
  - Casting Director
    - username: `thisisacastingdirector@gmail.com`
    - password: H3Ll0mYfR13nD
  - Executive Producer
    - username: `thisisanexecutivedirector@gmail.com`
    - password: H3Ll0mYfR13nD

To log in as one of the roles listed above and receive a JWT token, you must navigate to the following link in your browser:
`https://dev-zk1xgmkt.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=y0n2z3MULXxFOw4X1ytkvtfybzQ9M0d1&redirect_uri=https://127.0.0.1:8080/login-results`

### Postman Test Suite
- Two postman collections have been included as part of this project

- `udacity-capstone-final`: this will run the Role based access tests against the local deployment of the capstone project.

- `udacity-capstone-heroku`: this will run the Role based access tests against the Heroku hosted deployment of the app.

- Both collections have the necessary JWT tokens included for the particular roles. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return the following error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable 
- 500: Internal Server Error

#### GET /movies
- General:
    - Fetches a list of movies, with each movie having details such as title, release_date and actors
    - Request Arguments: None
    - Returns: A dictionary with a single key, movies, that contains a list of objects with actors, id, release_date and title 
- Sample: `curl http://127.0.0.1:8080/movies`

``` 
{
    "movies": [
        {
            "actors": [],
            "id": 1,
            "release_date": "1999",
            "title": "Star Wars: Episode 1 - The Phantom Menace"
        },
        {
            "actors": [
                {
                    "id": 2,
                    "name": "Hayden Christensen"
                }
            ],
            "id": 2,
            "release_date": "2002",
            "title": "Star Wars: Episode 2 - Attack of the Clones"
        },
        {
            "actors": [],
            "id": 3,
            "release_date": "2005",
            "title": "Star Wars: Episode 3 - Revenge of the Sith"
        },
        {
            "actors": [
                {
                    "id": 5,
                    "name": "Harrison Ford"
                },
                {
                    "id": 4,
                    "name": "Mark Hamill - Hamill Himself"
                }
            ],
            "id": 5,
            "release_date": "1980",
            "title": "Star Wars: Episode 5 - The Empire Strikes Back"
        },
        {
            "actors": [
                {
                    "id": 5,
                    "name": "Harrison Ford"
                },
                {
                    "id": 4,
                    "name": "Mark Hamill - Hamill Himself"
                }
            ],
            "id": 6,
            "release_date": "1983",
            "title": "Star Wars: Episode 6 - Return of the Jedi"
        },
        {
            "actors": [
                {
                    "id": 6,
                    "name": "Daisy Ridley"
                }
            ],
            "id": 7,
            "release_date": "2015",
            "title": "Star Wars: Episode 7 - The Force Awakens"
        }
    ],
    "success": true
}
```

#### GET /actors
- General:
    - Fetches a list of actors, with each actor having details such as age, gender, name and movies
    - Request Arguments: None
    - Returns: An dictionary with a single key, actors, that contains a list of objects with age, gender, id, movies and name 
- Sample: `curl http://127.0.0.1:8080/actors`

``` 
{
    "actors": [
        {
            "age": 51,
            "gender": "male",
            "id": 1,
            "movies": [],
            "name": "Ewan Mcgregor"
        },
        {
            "age": 41,
            "gender": "male",
            "id": 2,
            "movies": [],
            "name": "Hayden Christensen"
        },
        {
            "age": 41,
            "gender": "female",
            "id": 3,
            "movies": [],
            "name": "Natalie Portman"
        },
        {
            "age": 71,
            "gender": "male",
            "id": 4,
            "movies": [],
            "name": "Mark Hamill"
        },
        {
            "age": 60,
            "gender": "male",
            "id": 5,
            "movies": [
                {
                    "id": 5,
                    "name": "Star Wars: Episode 5 - The Empire Strikes Back"
                },
                {
                    "id": 6,
                    "name": "Star Wars: Episode 6 - Return of the Jedi"
                }
            ],
            "name": "Harrison Ford"
        },
        {
            "age": 30,
            "gender": "female",
            "id": 6,
            "movies": [
                {
                    "id": 7,
                    "name": "Star Wars: Episode 7 - The Force Awakens"
                }
            ],
            "name": "Daisy Ridley"
        }
    ],
    "success": true
}
```

#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie with the given ID if it exists.
    - Request Arguments: movie ID
    - Returns: dictionary including success value and deleted movie ID. 
- Sample: `curl -X DELETE http://127.0.0.1:8080/movies/4`

``` 
{
    "deleted": 4,
    "success": true
}
```

#### DELETE /actors/{actor_id}
- General:
    - Deletes the actor with the given ID if it exists.
    - Request Arguments: actor ID
    - Returns: dictionary including success value and deleted actor ID. 
- Sample: `curl -X DELETE http://127.0.0.1:8080/actors/1`

``` 
{
    "deleted": 1,
    "success": true
}
```

#### POST /movies
- General:
    - Creates a new movie
    - Request Arguments: title, release_date, OPTIONAL: actors
    - Returns: dictionary including created movie id, success value, movie that was created
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title": "Star Wars: Return of the Jedi", "release_date": "1981", "actors": [4]}' 'http://127.0.0.1:8080/movies'`

``` 
{
    "created": 10,
    "movie": {
        "actors": [
            {
                "id": 4,
                "name": "Mark Hamill"
            }
        ],
        "id": 10,
        "release_date": "1981",
        "title": "Star Wars: Return of the Jedi"
    },
    "success": true
}
```

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title": "Star Wars: Episode 7 - The Force Awakens", "release_date": "2015"}' http://127.0.0.1:8080/movies`

``` 
{
    "created": 11,
    "movie": {
        "actors": [],
        "id": 11,
        "release_date": "2015",
        "title": "Star Wars: Episode 7 - The Force Awakens"
    },
    "success": true
}
```

#### POST /actors
- General:
    - Creates a new actor
    - Request Arguments: title, release_date, OPTIONAL: movies
    - Returns: dictionary including created actor ID, success value, actor that was created
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"name": "Hayden Christensen", "age": 41, "gender": "male", "movies": [1,2]}' 'http://127.0.0.1:8080/actors'`

``` 
{
    "actor": {
        "age": 41,
        "gender": "male",
        "id": 10,
        "movies": [
            {
                "id": 1,
                "name": "Star Wars: Episode 1 - The Phantom Menace"
            },
            {
                "id": 2,
                "name": "Star Wars: Episode 2 - Attack of the Clones"
            }
        ],
        "name": "Hayden Christensen"
    },
    "created": 10,
    "success": true
}
```

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"name": "Daisy Ridley", "age": 30, "gender": "female"}' http://127.0.0.1:8080/actors`

``` 
{
    "actor": {
        "age": 30,
        "gender": "female",
        "id": 8,
        "movies": [],
        "name": "Daisy Ridley"
    },
    "created": 8,
    "success": true
}
```

#### PATCH /movies/{movie_id}
- General:
    - Updates an existing movie
    - OPTIONAL Request Arguments: title, release_date, actors
    - Returns: dictionary including success value and movie that was created
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title": "Star Wars: Episode 7 - The Force Awakens", "release_date": "2015", "actors": [6]}' 'http://127.0.0.1:8080/movies/7'`

```
{
    "movie": {
        "actors": [
            {
                "id": 6,
                "name": "Diasy Ridley"
            }
        ],
        "id": 7,
        "release_date": "2015",
        "title": "Star Wars: Episode 7 - The Force Awakens"
    },
    "success": true
}
```

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title": "Star Wars: Episode 7 - The Force Awakens Director's Cut"}' 'http://127.0.0.1:8080/movies/7'`

``` 
{
    "movie": {
        "actors": [
            {
                "id": 6,
                "name": "Daisy Ridley"
            }
        ],
        "id": 7,
        "release_date": "2015",
        "title": "Star Wars: Episode 7 - The Force Awakens Director's Cut"
    },
    "success": true
}
```

#### PATCH /actors/{actor_id}
- General:
    - Updates an existing actor
    - OPTIONAL Request Arguments: name, age, gender, movies
    - Returns: dictionary including success value and actor that was created
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"name": "Harrison Ford","age": 60,"gender": "male","movies": [5,6]}' 'http://127.0.0.1:8080/actors/5'`

``` 
{
    "actor": {
        "age": 60,
        "gender": "male",
        "id": 5,
        "movies": [
            {
                "id": 5,
                "name": "Star Wars: Episode 5 - The Empire Strikes Back"
            },
            {
                "id": 6,
                "name": "Star Wars: Episode 6 - Return of the Jedi"
            }
        ],
        "name": "Harrison Ford"
    },
    "success": true
}
```

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"name": "Harrison Ford - (Han Solo)"}' 'http://127.0.0.1:8080/actors/5'`

```
{
    "actor": {
        "age": 60,
        "gender": "male",
        "id": 5,
        "movies": [
            {
                "id": 5,
                "name": "Star Wars: Episode 5 - The Empire Strikes Back"
            },
            {
                "id": 6,
                "name": "Star Wars: Episode 6 - Return of the Jedi"
            }
        ],
        "name": "Harrison Ford - (Han Solo)"
    },
    "success": true
}
```

## Deployment

The app has been deployed on Heroku at: `https://udacity-capstone-1537268.herokuapp.com/`

## Authors
Joseph Doogan

## Acknowledgements 
The team at Udacity
