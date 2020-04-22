# FSND Capstone Project

**APPLICATION ROOTS**: 

- Production App Root:

```txt
https://castingfsnd.herokuapp.com/
```

- Local Development App Root:

```shell
http://127.0.0.1:5000/
```



## Getting Started

---

### Installing Dependencies:

**Python 3.7**

Follow instructions to install the version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

**Virtual Environment**

It is recommended to utilize a virtual environment to run this project locally. This will allow us to ensure that your project can wrap it's particular set of dependencies to the project scope, and ensures you're not polluting the global python installation on your local machine. Complete instructions for setting up a proper virtual environment can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

> **Virtual Environment Quick Start**
>
> ```shell
> python -m venv venv
> ```
>
> ```shell
> source venv/bin/activate
> ```
>



**Install Dependencies**

```shell
pip install -r requirements.txt
```

- This will install all of the required packages we defined in `requirements.txt`.



### Setup Primary Database

```shell
createdb casting
```

- Setup environment variable for primary local database path:

```shell
export DATABASE_URL=<URI_TO_DATABASE> 
```

> **NOTE**: For easy operation, you can reset and seed the local database by [clicking here](http://127.0.0.1:5000/api/seed) or navigating to:
>
> http://127.0.0.1:5000/seed
>
> This will generate the initial data needed for the application, and will reset the database if data has already been seeded. 
>
> **NOTE**: you do not need to be authenticated to trigger this endpoint



### Setup Testing Database

```shell
createdb casting_test
```

- Setup environment variable for local test database path:

```shell
export TEST_DATABASE_URL=<URI_TO_DATABASE> 
```

> Any tests being run will get executed by default against this secondary database. 



**Running The Server**





> **NOTE:**  <u>Production database paths are already configured via Heroku</u>
>
> 
>
> You can also manually set the following if they differ for your purposes:
>
> ```shell
> # set default app entry-point:
> export FLASK_APP=app.py
> # set development mode to monitor and refresh app on file changes:
> export FLASKENV=development
> ```
>
> - Runs the Flask server :
>
> ```shell
> # used to fire up the server:
> flask run --reload
> ```



**Running Tests**

> Run tests against local testing database:
>
> ```shell
> python test_api.py
> ```
>
> **NOTE**: `TEST_DATABASE_URL` must be set locally. See[ `Setup Local Testing Database`](#setup-testing-database)







### All Available Endpoints:

| Endpoint:            | Available Methods: | Details:                                                     |
| -------------------- | ------------------ | ------------------------------------------------------------ |
| `/`                  | `GET`              | returns the application index route                          |
| `/seed`              | `GET`              | used to seed/re-seed the database with default records       |
| `/actors`            | [`GET, POST`]      | used to `GET` a `list` of all `actors` and `POST` new `actors` |
| `/movies`            | [`GET, POST`]      | used to `GET` a `list` of all `movies` and `POST` new `movies` |
| `/actors/<actor_id>` | [PATCH, DELETE`]   | used to `GET` a single `actor` by `actor_id`, or `PATCH`  a single `actor` by `actor_id` or `DELETE` a single `actor` by `actor_id` |
| `/movies/<movie_id>` | [PATCH, DELETE`]   | used to `GET` a single `movie` by `movie_id`, or `PATCH`  a single `movie` by `movie_id` or `DELETE` a single `movie` by `movie_id` |



### Permissions By Role:

| Permissions     | Roles                                                       |
| --------------- | ----------------------------------------------------------- |
| `get:actors`    | [`executive_producer, casting_director, casting_assistant`] |
| `get:movies`    | [`executive_producer, casting_director, casting_assistant`] |
| `post:actors`   | [`executive_producer, casting_director`]                    |
| `post:movies`   | [`executive_producer`]                                      |
| `patch:actors`  | [`executive_producer, casting_director`]                    |
| `patch:movies`  | [`executive_producer, casting_director`]                    |
| `delete:actors` | [`executive_producer, casting_director`]                    |
| `delete:movies` | [`executive_producer`]                                      |



## Endpoint Usage

**`GET /actors`**

> - Fetch a list of `actors`
> - Args: `none`
> - Returns: `JSON` containing all info related to each actor
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "actors": [
>     {
>       "age": 25,
>       "gender": "m",
>       "id": 1,
>       "name": "Sam Jones"
>     },
>     {
>       "age": 22,
>       "gender": "f",
>       "id": 2,
>       "name": "Cynthia Jones"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 3,
>       "name": "Vanna White"
>     }
>   ],
>   "success": true
> }
> ```



**`GET /movies`**

> - Fetch a list of `movies`
> - Args: `none`
> - Returns: `JSON` containing all info related to each movie
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "movies": [
>     {
>       "id": 1,
>       "title": "The Movie",
>       "year": 2015
>     },
>     {
>       "id": 2,
>       "title": "The Movie 2",
>       "year": 2016
>     },
>     {
>       "id": 3,
>       "title": "The Movie 3",
>       "year": 2017
>     }
>   ],
>   "success": true
> }
> ```



**`POST /actors`**

> - Insert new actor record into database
> - Args: `name, age, gender`
> - Returns: `JSON`new actor details
>
> **EXAMPLE RESPONSE**
>
> ```json
> {
>   "actors": [
>     {
>       "age": 25,
>       "gender": "m",
>       "id": 1,
>       "name": "Sam Jones"
>     },
>     {
>       "age": 22,
>       "gender": "f",
>       "id": 2,
>       "name": "Cynthia Jones"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 3,
>       "name": "Vanna White"
>     },
>     {
>       "age": 24,
>       "gender": "m",
>       "id": 4,
>       "name": "Tim Adams"
>     }
>   ],
>   "success": true
> }
> ```





**`POST /movies`**

> - Insert new movie record into database
> - Args: `title, year`
> - Returns: `JSON`new movie details
>
> **EXAMPLE RESPONSE**
>
> ```json
> {
>   "movies": [
>     {
>       "id": 1,
>       "title": "The Movie",
>       "year": 2015
>     },
>     {
>       "id": 2,
>       "title": "The Movie 2",
>       "year": 2016
>     },
>     {
>       "id": 3,
>       "title": "The Movie 3",
>       "year": 2017
>     },
>   	{
>       "id": 4,
>       "title": "The Movie 4",
>       "year": 2017
>   }
>   "success": true
> }
> ```



**`PATCH /actors/<int:actor_id>`**

> - Fetch a single `actor` by `actor_id`
> - Args: `actor_id`
> - Returns: `JSON` repsonse containing request status and updated actor details
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "actors": [
>      {
>       "age": 25,
>       "gender": "m",
>       "id": 1,
>       "name": "Sam Jones"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 2,
>       "name": "Samantha Adams"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 3,
>       "name": "Vanna White"
>     },
> 	{
>       "age": 24,
>       "gender": "m",
>       "id": 4,
>       "name": "Tim Adams"
>   	}
>   ],
>   "success": true
> }
> ```
>
> 



**`PATCH /movies/<int:movie_id>`**

> - Fetch a single `movie` by `movie_id`
> - Args: `movie_id`
> - Returns: `JSON` repsonse containing request status and updated movie details
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "movies": [
>      {
>       "id": 1,
>       "title": "The Movie",
>       "year": 2015
>     },
>     {
>       "id": 2,
>       "title": "The Movie 4.1",
>       "year": 2018
>     },
>     {
>       "id": 3,
>       "title": "The Movie 3",
>       "year": 2017
>     },
>   	{
>       "id": 4,
>       "title": "The Movie 4",
>       "year": 2017
>   	}
>   ],
>   "success": true
> }
> ```



**`DELETE /actors/<int:actor_id>`**

> - Delete a single `actor` by `actor_id`
> - Args: `actor_id`
> - Returns: `JSON` repsonse containing request status and deleted `actor_id`
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "actors": [
>      {
>       "age": 25,
>       "gender": "m",
>       "id": 1,
>       "name": "Sam Jones"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 2,
>       "name": "Samantha Adams"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 3,
>       "name": "Vanna White"
>     },
>   ],
>   "success": true
> }
> ```



**`DELETE /movies/<int:movie_id>`**

> - Delete a single `movie` by `movie_id`
> - Args: `movie_id`
> - Returns: `JSON` repsonse containing request status, and deleted `movie_id`
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "movies": [
>      {
>       "id": 1,
>       "title": "The Movie",
>       "year": 2015
>     },
>     {
>       "id": 2,
>       "title": "The Movie 4.1",
>       "year": 2018
>     },
>     {
>       "id": 3,
>       "title": "The Movie 3",
>       "year": 2017
>     },
>   ],
>   "success": true
> }
> ```

