# FSND Capstone Project  
This is the final project in the Full Stack Nanodegree. It will be an application of all concepts learned throughout this course. For this project, a Casting Agency API will be implemented  

[https://as-capstone.herokuapp.com/](https://as-capstone.herokuapp.com/)

---------
## Casting Agency API

The casting agency is a company that is responsible for creating movies and managing and assigning actors to those movies.

- Models:
    - Movies: title, release date
    - Actors: Name, Age, Gender
&nbsp;
- Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/
&nbsp;
- Roles:
    - Casting Director
        - Can view actors and movies
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database

## Getting Started
------------------
### Prerequisites
- Python3
- PIP

### Running The Server Locally
---------
**Virtual Environment**
- Create a Virtual Environment in backend directory
```bash
python3 -m venv /path/to/new/virtual/environment
```
- Activate venv
```bash
$ source <venv>/bin/activate
```
> [Creation and Activation of virtual environments](https://docs.python.org/3/library/venv.html)

**PIP Dependencies**

Now you have your venv created and activated, run the following command to install all required packages:

```bash
pip install -r requirements.txt
```

**Database Setup**
- Create capstone database, and restore the database provided 
```bash
dropdb capstone
createdb capstone
psql capstone < capstone.psql
```

**Running the server**
```bash
source setup.sh
flask run
```

### Testing
------
To run the tests, run the following:
```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```

## API Reference
------------
### Getting Started
- Base URL: The backend app is hosted at [https://as-capstone.herokuapp.com/](https://as-capstone.herokuapp.com/) or   
you can run it locally at ```127.0.0.1:5000```
- Authentication: Tokens can be found in the setup.sh file.
### Error Handling
Errors are returned as JSON objects as shown below:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found!"
}
```

The API will return one of the following error types when a request fails:
- 404: Not Found
- 422: Unprocessable
- 400: Bad Request
- 405: Method Not Allowed

### Endpoints
**GET /actors**
- General:
    - returns a list of actors and a success value
- Sample: 
```
curl 'https://as-capstone.herokuapp.com/actors'\
--header 'Authorization: Bearer {TOKEN}
```
```
 {
  "actors": [
    {
      "age": 47,
      "gender": "M",
      "name": "Leonardo Dicaprio"
    }
  ],
  "success": true
}
```
**GET /movies**
- General:
    - Returns a list of movies and a success value

- Sample: 
```
curl 'https://as-capstone.herokuapp.com/movies'\
--header 'Authorization: Bearer [TOKEN]
```
```
 {
  "movies": [
    {
      "release_date": "Sat, 01 May 2021 12:54:05 GMT",
      "title": "Inception"
    }
  ],
  "success": true
}
```

**POST /actors**
- General:
    - Creates a new actor
    - Returns a success value
- Sample:
```
curl -X POST 'https://as-capstone.herokuapp.com/actors' \
--header 'Authorization: Bearer [TOKEN] \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Leonardo DiCaprio",
    "age": 46,
    "gender": "M"
}'
```
```
{
  "success": true
}
```

**DELETE /actors/<actor_id>**
- General:
    - Deletes the actor of the given actor ID if it exists
    - Returns a success value
- Sample: 
```
curl -X DELETE 'https://as-capstone.herokuapp.com/actors/2' \
--header 'Authorization: Bearer [TOKEN]
```
```
{
  "success": true
}
```

**PATCH /actors/<actor_id>**
- General:
    - Updates a specified actor
    - Returns a success value and the updated actor
- Sample: 
```
curl -X PATCH 'https://as-capstone.herokuapp.com/actors/1' \
--header 'Authorization: Bearer [TOKEN] \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Leonardo Dicaprio",
    "age": 47,
    "gender": "M"
}'
```
```
{
    "actor": {
        "age": 47,
        "gender": "M",
        "name": "Leonardo Dicaprio"
    },
    "success": true
}
```

**POST /movies**
- General:
    - Creates a new movie
    - Returns a success value
- Sample: 
```
curl -X POST 'https://as-capstone.herokuapp.com/movies' \
--header 'Authorization: Bearer [TOKEN] \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "movie1",
    "release_date": "Sat, 01 May 2021 12:35:19 GMT"
}'
```
```
{
    "success": true
}
```

**DELETE /movies/<movie_id>**
- General:
    - Deletes the movie of the given movie ID if it exists
    - Returns a success value
- Sample: 
```
curl -X DELETE 'https://as-capstone.herokuapp.com/movie/1' \
--header 'Authorization: Bearer [TOKEN]
```
```
{
  "success": true
}
```

**PATCH /movies/<movie_id>**
- General:
    - Updates a specified movie
    - Returns a success value and the updated movie
- Sample: 
```
curl -X PATCH 'https://as-capstone.herokuapp.com/movies/1' \
--header 'Authorization: Bearer [TOKEN] \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Inception",
    "release_date": "Sat, 01 May 2021 12:35:19 GMT"
}'
```
```
{
    "movie": {
        "release_date": "Sat, 01 May 2021 12:54:05 GMT",
        "title": "Inception"
    },
    "success": true
}
```

> For easier testing for the hosted API, you can use the provided postman collection.
