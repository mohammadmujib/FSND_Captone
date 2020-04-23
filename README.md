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

## Demo Page  

https://casting-agency001.herokuapp.com

Test each endpoint with the link above ,and different role's Jwts. 
JWTs for different role can be accessed by login to the link with username and password provided as follows.
https://capstone-casting.auth0.com/authorize?audience=casting&response_type=token&client_id=1WOTxcL9BI2MY7bF3poP8bfTWh6o4ZnN&redirect_uri=https://castingfsnd.herokuapp.com/	

```
- Casting Assistant
    - UserName: assistant@test.com
    - Password: Root1234
- Casting Director
    - UserName: director@gmail.com
    - Password: Root1234
- Executive Producer
    - UserName: producer@gmail.com
    - Password: Root1234 
```



**Running Tests**

> Run tests against local testing database:
>
> ```shell
> python test_api.py
> ```
>
> **NOTE**: `TEST_DATABASE_URL` must be set locally. See[ `Setup Local Testing Database`](#setup-testing-database)
>
> 

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
>       "name": "Robert De Niro"
>     },
>     {
>       "age": 22,
>       "gender": "f",
>       "id": 2,
>       "name": "Angelina Jolie"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 3,
>       "name": "Nick Jonas"
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
>       "release_date": "Mon, 01 Jan 2018 00:00:00 GMT",
>       "title": "Titanic"
>     },
>     {
>       "id": 2,
>       "release_date": "Tue, 01 Jan 2019 00:00:00 GMT",
>       "title": "Avenger"
>     },
>     {
>       "id": 3,
>       "release_date": "Wed, 01 Jan 2020 00:00:00 GMT",
>       "title": "Amazing Spider man"
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
>       "name": "Robert De Niro"
>     },
>     {
>       "age": 22,
>       "gender": "f",
>       "id": 2,
>       "name": "Angelina Jolie"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 3,
>       "name": "Nick Jonas"
>     },
>     {
>       "age": 25,
>       "gender": "m",
>       "id": 4,
>       "name": "crisso"
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
>       "release_date": "Mon, 01 Jan 2018 00:00:00 GMT",
>       "title": "Titanic"
>     },
>     {
>       "id": 2,
>       "release_date": "Tue, 01 Jan 2019 00:00:00 GMT",
>       "title": "Avenger"
>     },
>     {
>       "id": 3,
>       "release_date": "Wed, 01 Jan 2020 00:00:00 GMT",
>       "title": "Amazing Spider man"
>     },
>     {
>       "id": 4,
>       "release_date": "Fri, 01 Mar 2019 00:00:00 GMT",
>       "title": "Avenger"
>     }
>   ],
>    "success": true
> }
> ```



**`PATCH /actors/<int:actor_id>`**

> - Fetch a single `actor` by `actor_id`
> - Args: `actor_id`
> - Returns: `JSON` updated actor details
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
> - Returns: `JSON`  updated movie details
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "movies": [
>     {
>       "id": 1,
>       "release_date": "Tue, 01 Jan 2019 00:00:00 GMT",
>       "title": "Avenger End Game"
>     },
>     {
>       "id": 2,
>       "release_date": "Tue, 01 Jan 2019 00:00:00 GMT",
>       "title": "Avenger"
>     },
>     {
>       "id": 3,
>       "release_date": "Wed, 01 Jan 2020 00:00:00 GMT",
>       "title": "Amazing Spider man"
>     },
>     {
>       "id": 4,
>       "release_date": "Fri, 01 Mar 2019 00:00:00 GMT",
>       "title": "Avenger"
>     }
>   ],
>   "success": true
> }
> ```



**`DELETE /actors/<int:actor_id>`**

> - Delete a single `actor` by `actor_id`
> - Args: `actor_id`
> - Returns: `JSON` updated actor details
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
>     }
>   ],
>   "success": true
> }
> ```



**`DELETE /movies/<int:movie_id>`**

> - Delete a single `movie` by `movie_id`
> - Args: `movie_id`
> - Returns: `JSON` updated movie details
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "movies": [
>     {
>       "id": 1,
>       "release_date": "Tue, 01 Jan 2019 00:00:00 GMT",
>       "title": "Avenger End Game"
>     },
>     {
>       "id": 2,
>       "release_date": "Tue, 01 Jan 2019 00:00:00 GMT",
>       "title": "Avenger"
>     },
>     {
>       "id": 3,
>       "release_date": "Wed, 01 Jan 2020 00:00:00 GMT",
>       "title": "Amazing Spider man"
>     }
>   ],
>   "success": true
> }
> ```

