# `/texts/<cts_urn>/`

The `/texts/<cts_urn>/` endpoint interacts with a specific literary work in Tesserae's database.

Note that `<cts_urn>` is a placeholder to be replaced by a [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding) CTS URN refering to a specific text.  (Modern web browsers tend to percent encode URLs by default, but if you are using a different method to query the API, you will have to percent encode the CTS URN yourself.  A variety of resources online can help you do this; query for "percent encode" in your favorite search engine to find them.)  Throughout the rest of this page, `<cts_urn>` will continue to serve as a placeholder for a percent encoded CTS URN.

## GET

Requesting GET at `/texts/<cts_urn>/` provides information on the literary work specified by `<cts_urn>`.

### Request

Remember, `<cts_urn>` must be properly percent encoded.

### Response

If `<cts_urn>` contains any information past the work identifiers (i.e., passage citations and subreferences), the response will be a `301` redirect, where the `Location` header points to the same URL, except that the information past the work identifiers is truncated.

On success, the response includes a data payload consisting of a JSON object with the following keys:

|Key|Value|
|---|---|
|`"author"`|A string identifying the text's author.|
|`"cts_urn"`|A string which uniquely identifies the text according to the Canonical Text Services conventions.|
|`"is_prose"`|A boolean value denoting whether the text is considered a prose work.|
|`"language"`|A string identifying the composition language of the text.|
|`"title"`|A string identifying the text's name.|
|`"year"`|An integer representing the text's publication year; a negative integer corresponds to the BC era.|

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Value|
|---|---|
|`"cts_urn"`|A string corresponding to the CTS URN decoded from the URL.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Retrieve a Text's Database Entry

Suppose that `urn:cts:latinLit:phi0917.phi001` exists in the database.

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/
```

Response:

```
HTTP/1.1 200 OK
...

{ 
  "author": "Lucan", 
  "cts_urn": "urn:cts:latinLit:phi0917.phi001", 
  "is_prose": false, 
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess",
  "language": "latin", 
  "title": "Bellum Civile", 
  "year": 65 
}
```

#### Attempt to Retrieve a Text's Database Entry with an Overly Specific CTS URN

Suppose that `urn:cts:latinLit:phi0917.phi001` exists in the database.

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001%3A1.1/"
```

Response:

```
HTTP/1.1 301 Moved Permanently
...
Location: /texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/
...
```

#### Attempt to Retrieve the Database Entry for a Text Not in the Database

Assume that no entry in the database has the CTS URN "DEADBEEF".

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/texts/DEADBEEF"
```

Response:

```
HTTP/1.1 404 Not Found
...

{
  "cts_urn": "DEADBEEF",
  "message": "No text with the provided CTS URN (DEADBEEF) was found in the database."
}
```

## PATCH

> NB:  The PATCH method for `/texts/<cts_urn>/` is available only on the administrative server

Requesting PATCH at `/texts/<cts_urn>/` with an appropriate JSON data payload will update the database entry of the text with a CTS URN of `<cts_urn>` according to the JSON data.

### Request

Appropriate JSON data for a PATCH at `/texts/<cts_urn>/` is any JSON object without the key `"cts_urn"`.  The keys in this object specify which attributes of the text entry in Tesserae's database will be updated (or added, if the key does not correspond with any of the text entry's attributes).  The new values of these attributes are specified by the values of the keys corresponding to those attributes.

> NB:  You cannot update a text's CTS URN with a PATCH at `/texts/<cts_urn>/`.  For this case, consider a [DELETE at `/texts/<cts_urn>/`](#delete) followed by a [POST at `/texts/`](texts.md#post).

### Response

If `<cts_urn>` contains any information past the work identifiers (i.e., passage citations and subreferences), the response will be a `308` redirect, where the `Location` header points to the same URL, except that the information past the work identifiers is truncated.

On success, the data payload contains the text entry in Tesserae's database after the update has been made.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Value|
|---|---|
|`"cts_urn"`|A string matching the percent decoded `<cts_urn>`.|
|`"data"`|The JSON object received as request data payload.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Update the Value of a Pre-existing Attribute of a Text's Database Entry

Assume that the following entry exists in the database:

```
{
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "is_prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess",
  "language": "latin",
  "title": "Bellum Civile",
  "year": 65
}
```

Request:

```
curl -i -X PATCH "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/" -d '{ \
  "title": "Pharsalia" \
}'
```

Response:

```
HTTP/1.1 200 OK
...

{
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "is_prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess",
  "language": "latin",
  "title": "Pharsalia",
  "year": 65
}
```

#### Add New Information to a Text's Database Entry

Assume that the following entry exists in the database:

```
{
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "is_prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess",
  "language": "latin",
  "title": "Bellum Civile",
  "year": 65
}
```

Request:

```
curl -i -X PATCH "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/" -d '{ \
  "alternate_title": "Pharsalia" \
}'
```

Response:

```
HTTP/1.1 200 OK
...

{
  "alternate_title": "Pharsalia"
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "is_prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess",
  "language": "latin",
  "title": "Bellum Civile",
  "year": 65
}
```

#### Attempt to Update a Text's Database Entry with an Overly Specific CTS URN

Suppose that `urn:cts:latinLit:phi0917.phi001` exists in the database.

Request:

```
curl -i -X PATCH "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001%3A1.1%3A1.1/" -d '{ \
  "new_key": "new_value" \
}'
```

Response:

```
HTTP/1.1 308 Moved Permanently
...
Location: /texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/
...
```

#### Attempt to Update the Database Entry for a Text Not in the Database

Assume that no entry in the database has the CTS URN "DEADBEEF".

Request:

```
curl -i -X PATCH "https://tesserae.caset.buffalo.edu/texts/DEADBEEF/" -d '{ \
  "fail": "this example will" \
}'
```

Response:

```
HTTP/1.1 404 Not Found
...

{
  "cts_urn": "DEADBEEF",
  "data": {
    "fail": "this example will"
  },
  "message": "No text with the provided CTS URN (DEADBEEF) was found in the database."
}
```

## DELETE

> NB:  The DELETE method for `/texts/<cts_urn>/` is available only on the administrative server

Requesting DELETE at `/texts/<cts_urn>/` with an appropriate JSON data payload will delete the text described by the JSON data from Tesserae's database.

### Request

There is no request data payload.

### Response

If `<cts_urn>` contains any information past the work identifiers (i.e., passage citations and subreferences), the response will be a `308` redirect, where the `Location` header points to the same URL, except that the information past the work idenitifiers is truncated.

On success, there is no response data payload.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Value|
|---|---|
|`"cts_urn"`|A string matching the percent decoded `<cts_urn>`.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Delete a Text

Assume that the following entry exists in the database:

```
{
  "author": "Lucan",
  "cts_urn": "urn:cts:latinLit:phi0917.phi001",
  "is_prose": false,
  "path": "https://raw.githubusercontent.com/tesserae/tesserae/master/texts/la/lucan.bellum_civile.tess",
  "language": "latin",
  "title": "Bellum Civile",
  "year": 65
}
```

Request:

```
curl -i -X DELETE "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/"'
```

Response:

```
HTTP/1.1 204 No Content
...
```

#### Attempt to Delete a Text's Database Entry with an Overly Specific CTS URN

Suppose that `urn:cts:latinLit:phi0917.phi001` exists in the database.

Request:

```
curl -i -X DELETE "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001%3A1.1%3A1.1/"
```

Response:

```
HTTP/1.1 308 Moved Permanently
...
Location: /texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/
...
```


#### Attempt to Delete a Database Entry for a Text Not in the Database

Assume that no entry in the database has the CTS URN "DEADBEEF".

Request:

```
curl -i -X DELETE "https://tesserae.caset.buffalo.edu/texts/DEADBEEF/"
```

Response:

```
HTTP/1.1 404 Not Found
...

{
  "cts_urn": "DEADBEEF"
  "message": "No text with the provided CTS URN (DEADBEEF) was found in the database."
}
```
