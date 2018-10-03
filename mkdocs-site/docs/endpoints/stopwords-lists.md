# `/stopwords/lists/`

the `/stopwords/lists` endpoint serves the names of the curated stopwords lists.  Use [`/stopwords/lists/<name>/`](stopwords-lists-name.md) to obtain one of these curated stopwords lists.

## GET

Requesting GET at `/stopwords/lists/` provides a list of strings, where each entry is the name of one of the curated stopwords lists.

### Request

There are no special points to note about requesting the curated stopwords list names.

### Response

On success, the response includes a JSON data payload consisting of a JSON object with the key `"list_names"` associated with an array of strings.  Each string in this array is the name of a curated stopwords list available on the Tesserae database.

### Examples

#### Discover Curated Stopwords List Names

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/stopwords/lists/"
```

Response:

```
HTTP/1.0 200 OK
...

{
  "list_names": [
    "latin-lemma-10",
    ...
  ]
}
```

## POST

> NB:  The POST method for `/stopwords/lists/` is available only on the administrative server

Requesting POST at `/stopwords/lists/` with an appropriate JSON data payload will add a stopwords list and an associated name to Tesserae's database.

### Request

Appropriate JSON data for a POST at `/stopwords/lists/` must be a JSON object containing the following keys:

|Key|Value|
|---|---|
|`"name"`|A string representing the name of the stopwords lists.|
|`"stopwords"`|An array of strings, where each string is a stopword.|

If the value given to `"name"` is already used in Tesserae's database for a stopwords list, the request will fail.  Consider a DELETE followed by a POST if you wish to change the list associated with a given list name.

### Response

On success, the response data payload contains the key `"stopwords"` associated with an array of strings.  Additionally, the `Content-Location` header will specify the URL associated with this newly created stopwords list.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Value|
|---|---|
|`"data"`|The JSON object received as request data payload.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Create a New Stopwords List

Request:

```
curl -i -X POST "https://tesserae.caset.buffalo.edu/stopwords/lists/" -d '{ \
  "name": "new-list", \
  "stopwords": [ \
    "a", \
    "b" \
  ] \
}'
```

Response:

```
HTTP/1.1 201 Created
...
Content-Location: /stopwords/lists/new-list/
...

{ 
  "stopwords": [
    "a",
    "b"
  ]
}
```

#### Attempt to Create a New Stopwords List with a Name Already in the Database

Suppose that `latin-lemma-10` is the name of one of the stopwords lists.

Request:

```
curl -i -X POST "https://tesserae.caset.buffalo.edu/stopwords/lists/" -d '{ \
  "name": "latin-lemma-10", \
  "stopwords": [ \
    "a", \
    "b" \
  ] \
}'
```

Response:

```
HTTP/1.1 400 Bad Request
...

{ 
  "data": {
    "name": "latin-lemma-10",
    "stopwords": [
      "a",
      "b"
    ]
  }
  "message": "The stopwords list name provided (latin-lemma-10) already exists in the database. If you meant to update the stopwords list, try a DELETE followed by a POST."
}
```

## DELETE

> NB:  The DELETE method for `/stopwords/lists/` is available only on the administrative server

Requesting DELETE at `/stopwords/lists/` with an appropriate JSON data payload will delete the stopwords list described by the JSON data from Tesserae's database.

### Request

Appropriate JSON data for a DELETE at `/stopwords/lists/` must contain the `"name"` key, associated with a string that is the name of one of the stopwords lists in Tesserae's database.

### Response

On success, there is no response data payload.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Value|
|---|---|
|`"data"`|The JSON object received as request data payload.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Delete a Stopwords List Already in the Database

Assume that a stopwords list named `already-exists` already exists in the database.


Request:

```
curl -i -X DELETE "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "name": "already-exists" \
}'
```

Response:

```
HTTP/1.1 204 No Content
...
```

#### Attempt to Delete a Stopwords List Not in the Database

Assume that there is not stopwords list named "i-dont-exist" in the database.

Request:

```
curl -i -X DELETE "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "name": "i-dont-exist" \
}'
```

Response:

```
HTTP/1.1 400 Bad Request
...

{
  "data": {
    "name": "i-dont-exist"
  },
  "message": "No stopwords list names match the specified name (i-dont-exist)."
}
```
