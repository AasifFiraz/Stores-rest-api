# 🔐 Stores Rest Api

Rest api developed using flask, All data stored in sqlite database, some endpoints require **jwt authentication** and some are open endpoints. All the endpoints contains CRUD Operations. Visit the Rest Api - [here](https://stores-rest-api-aasif.herokuapp.com/)

 ##  Download The Repository

```bash
git clone https://github.com/AasifFiraz/Stores-rest-api.git
```
##  Download The Source Code
You can quickly download the source code by clicking [here](https://github.com/AasifFiraz/Stores-rest-api/archive/refs/heads/main.zip)

## Installation
 
```bash
pip install requirements.txt
```
This will install the necessary python packages you need to run the Api

## Open Endpoints

Open endpoints require no Authentication.
 
 # Register
**URL** :   `POST /register`

**Data constraints**

```json
{
    "username": "[valid username]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "Johndoe",
    "password": "abcd1234"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
	"message": "user created successfully"
}
```

## Error Response

**Condition** : If 'username' and 'password' combination is wrong.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
	"message": {
		"username/password": "field cannot be blank"
	}
}
``` 
 # Login
 
 **URL** : `POST /login` 

**Data constraints**

```json
{
    "username": "[valid username]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "Johndoe",
    "password": "abcd1234"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
	"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjUyMDgyNjI3LCJqdGkiOiJkZTQ5ZmJlOC00OTQyLTRlZjktYjNhMC0xOTFhNmI0MDRhMWYiLCJ0eXBlIjoiYWNjZ",

	"refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjA4MjYyNywianRpIjoiMGVmZGVjZDItMjI1MS00N2EyLWE4MWYtMGIyMWVhZDUwODJhIiwidHlwZSI6InJlZnJlc2g""
}
```

## Error Response

**Condition** : If 'username' or 'password'  is wrong.

**Code** : `401 UNAUTHORIZED`

**Content** :

```json
{
	"message": "Invalid credentials"
}
```

## Store Endpoints

* `POST /store/<name>` 
	
	**Success Response** - 200

	```json
	{
		"id": 1,
		"name": "Sport Goods",
		"items": []
	}
	```
<br>

* `GET /store/<name>` 
	
	**Success Response** - 200

	```json
	{
		"id": 1,
		"name": "Sport Goods",
		"items": []
	}
	```
<br>

* `DELETE /store/<name>` 
	
	**Success Response** - 200

	```json
	{
		"message": "store 'Sport Goods' deleted"
	}
	```

<br>

* `GET /stores` - Retrieves all the stores 
	
	**Success Response** - 200

	```json
	{
		"items": [
			{
				"id": 2,
				"name": "Fruits",
				"items": []
			}
		]
	}
	```

## User Endpoints

* `GET /user/<user_id>` 
	
	**Success Response** - 200

	```json
	{
		"user_id": 1,
		"username": "Johndoe"
	}
	```

<br>

* `DELETE /user/<user_id>` 
	
	**Success Response** - 200

	```json
	{
		"message": "User deleted"
	}
	```


## Endpoints that require Authentication

Closed endpoints require a Bearer Access Token to be included in the header of the request. A Token can be acquired from the Login view above.

## Item Endpoints 

`<name> = Item Name`

* `POST /item/<name>` 

	**Authorization** : `Bearer <Acesss Token>`
	
	**Data example** 

	```json
	{
	    "price": "19.99",
	    "store_id": 2
	}
	```
<br>

* `GET /item/<name>` 
* 
	**Authorization** : `Bearer <Acesss Token>`	
	
	**Success Response** - 200

	```json
	{
	    "id": 1,
	    "name": "Racket",
	    "price": 19.99,
	    "store_id": 2
	}
	```
<br>

* `PUT /item/<name>` 

	**Authorization** : `Bearer <Acesss Token>`
	
	**Data example** 

	```json
	{
	    "price": "39.99",
	    "store_id": 2
	}
	```
<br>

* `DELETE /item/<name>` 

	**Authorization** : `Bearer <Acesss Token>`
	
	**Data example** 

	```json
	{
		"message": "item 'Racket' deleted"
	}
	```
