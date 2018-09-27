# `/texts/`

The `/texts/` endpoint interacts with Tesserae's database of literary works.

## GET

Requesting GET at `/texts/` provides information on literary works stored in Tesserae's database.

### Request

The following fields may be used in a URL query to filter the response:

|Field|Description|
|---|---|
| `author`|  Only database information for texts with the specified author are returned
| `after`|  Only database information for texts written/published after the specified year are returned; use negative integers for B.C. dates
| `before`|  Only database information for texts written/published before the specified year are returned; use negative integers for B.C. dates
| `cts_urn`|  Only database information for texts with the specified CTS URN are returned
| `prose`|  If set to "true", only database for information for texts considered prose works are returned|
| `language`|  Only database information for texts with the specified language are returned
| `title`|  Only database information for texts with the specified title are returned

### Response

On success, the response includes a JSON data payload consisting of an array of objects, where each object contains the following keys:

|Key|Description|
|---|---|
|`"author"`|A string identifying the text's author.|
|`"cts_urn"`|A string which uniquely identifies the text according to the Canonical Text Services conventions.|
|`"prose"`|A boolean value denoting whether the text is considered a prose work.|
|`"language"`|A string identifying the composition language of the text.|
|`"title"`|A string identifying the text's name.|
|`"year"`|An integer representing the text's publication year; a negative integer corresponds to the BC era.|

### Examples

#### Search by One Field

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/texts/?author=Vergil"
```

Response:

```
HTTP/1.0 200 OK
...

[
  {
    "author": "Vergil",
    ...
  },
  ...
]
```

#### Search by Multiple Fields

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/texts/?after=100&language=latin"
```

Response:

```
HTTP/1.0 200 OK
...

[
  {
    ...
    "language": "latin",
    ...
    "year": 101
  },
  ...
]
```

## POST

> NB:  The POST method for `/texts/` is available only on the administrative server

Requesting POST at `/texts/` with an appropriate JSON data payload will add the text described by the JSON data to Tesserae's database.

### Request

Appropriate JSON data for a POST at `/texts/` must be a JSON object containing the following keys:

|Key|Description|
|---|---|
|`"author"`|A string identifying the text's author.|
|`"cts_urn"`|A string which uniquely identifies the text according to the Canonical Text Services conventions.|
|`"prose"`|A boolean value denoting whether the text is a prose work.|
|`"language"`|A string identifying the composition language of the text.|
|`"path"`| A string identifying the location of the text's contents.|
|`"title"`|A string identifying the text's name.|
|`"year"`|An integer representing the text's publication year; a negative integer corresponds to the BC era.|

### Response

On success, there is no reponse data payload.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Description|
|---|---|
|`"data"`|The JSON object received as request data payload.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Upload a New Text

Request:

```
curl -i -X POST "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "author": "Lucan", \
  "cts_urn": "urn:cts:latinLit:phi0917.phi001", \
  "prose": false, \
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess" \
  "language": "latin", \
  "title": "Bellum Civile", \
  "year": 65 \
}'
```

Response:

```
HTTP/1.0 200 OK
...
```

#### Upload a Text Already in the Database

Assume that an entry in the database with the CTS URN "urn:cts:latinLit:phi0917.phi001" already exists.

Request:

```
curl -i -X POST "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "author": "Lucan", \
  "cts_urn": "urn:cts:latinLit:phi0917.phi001", \
  "prose": false, \
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess" \
  "language": "latin", \
  "title": "Bellum Civile", \
  "year": 65 \
}'
```

Response:

```
HTTP/1.0 400 Bad Request
...

{
  "data": {
    "author": "Lucan",
    "cts_urn": "urn:cts:latinLit:phi0917.phi001",
    "prose": false,
    "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess"
    "language": "latin",
    "title": "Bellum Civile",
    "year": 65
  },
  "message": "The CTS URN provided (urn:cts:latinLit:phi0917.phi001) already exists in the database. If you meant to update the text information, try PUT."
}
```

#### Upload a Text with Insufficient Information

Request:

```
curl -i -X POST "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "author": "Lucan", \
  "prose": false, \
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess" \
  "language": "latin", \
  "title": "Bellum Civile", \
  "year": 65 \
}'
```

Response:

```
HTTP/1.0 400 Bad Request
...

{
  "data": {
    "author": "Lucan",
    "prose": false,
    "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess"
    "language": "latin",
    "title": "Bellum Civile",
    "year": 65
  },
  "message": "The request data payload is missing the following required key(s): cts_urn."
}
```

## PATCH

> NB:  The PATCH method for `/texts/` is available only on the administrative server

Requesting PATCH at `/texts/` with an appropriate JSON data payload will update the text described by the JSON data in Tesserae's database.

### Request

Appropriate JSON data for a PATCH at `/texts/` must contain the `cts_urn` key, associated with a value corresponding to the CTS URN of a text entry in Tesserae's database.  Any other keys with their values in the request data payload will update values corresponding to those keys for the text entry in Tesserae's database.

> NB:  You cannot update a text's CTS URN with a PATCH at `/texts/`.  For this case, consider a DELETE followed by a POST.

### Response

On success, the data payload contains the text entry in Tesserae's database after the update has been made.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Description|
|---|---|
|`"data"`|The JSON object received as request data payload.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Update a Text

Assume that the following entry exists in the database:

```
{
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess"
  "language": "latin",
  "title": "Bellum Civile",
  "year": 65
}
```

Request:

```
curl -i -X PATCH "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "cts_urn": "urn:cts:latinLit:phi0917.phi001", \
  "title": "Pharsalia" \
}'
```

Response:

```
HTTP/1.0 200 OK
...

{
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess"
  "language": "latin",
  "title": "Pharsalia",
  "year": 65
}
```

#### Add New Information to a Text

Assume that the following entry exists in the database:

```
{
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess"
  "language": "latin",
  "title": "Bellum Civile",
  "year": 65
}
```

Request:

```
curl -i -X PATCH "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "cts_urn": "urn:cts:latinLit:phi0917.phi001", \
  "alternate_title": "Pharsalia" \
}'
```

Response:

```
HTTP/1.0 200 OK
...

{
  "alternate_title": "Pharsalia"
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess"
  "language": "latin",
  "title": "Bellum Civile",
  "year": 65
}
```

#### Update a Text Not in the Database

Assume that no entry in the database has the CTS URN "DEADBEEF".

Request:

```
curl -i -X PATCH "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "cts_urn": "DEADBEEF", \
  "fail": "this example will" \
}'
```

Response:

```
HTTP/1.0 400 Bad Request
...

{
  "data": {
    "cts_urn": "DEADBEEF",
    "fail": "this example will"
  },
  "message": "No text with the provided CTS URN (DEADBEEF) was found in the database."
}
```

## DELETE

> NB:  The DELETE method for `/texts/` is available only on the administrative server

Requesting DELETE at `/texts/` with an appropriate JSON data payload will delete the text described by the JSON data from Tesserae's database.

### Request

Appropriate JSON data for a DELETE at `/texts/` must contain the `cts_urn` key, associated with a value corresponding to the CTS URN of a text entry in Tesserae's database.

### Response

On success, there is no response data payload.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Description|
|---|---|
|`"data"`|The JSON object received as request data payload.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Delete a Text

Assume that the following entry exists in the database:

```
{
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess"
  "language": "latin",
  "title": "Bellum Civile",
  "year": 65
}
```

Request:

```
curl -i -X DELETE "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "cts_urn": "urn:cts:latinLit:phi0917.phi001" \
}'
```

Response:

```
HTTP/1.0 204 No Content
...
```

#### Delete a Text Not in the Database

Assume that no entry in the database has the CTS URN "DEADBEEF".

Request:

```
curl -i -X DELETE "https://tesserae.caset.buffalo.edu/texts/" -d '{ \
  "cts_urn": "DEADBEEF" \
}'
```

Response:

```
HTTP/1.0 400 Bad Request
...

{
  "data": {
    "cts_urn": "DEADBEEF"
  },
  "message": "No text with the provided CTS URN (DEADBEEF) was found in the database."
}
```
