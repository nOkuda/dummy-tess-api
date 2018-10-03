# `/parallels/<uuid>/`

The `/parallels/<uuid>/` endpoint serves the results from a Tesserae intertext discovery result.  Note that `<uuid>` is a placeholder for an identifying string.

> NB:  This endpoint is meant to be used for retrieving the results from a Tesserae search and not as a permanent link to a previously completed search.

## GET

Requesting GET at `/parallels/<uuid>/` retrieves the Tesserae search results associated with `<uuid>`.  This association was made at the time that the intertext query was submitted with a POST at [`/parallels/`](parallels.md).

### Request

There are no special points to note about requesting Tesserae search results.

### Response

On success, the data payload contains a JSON object with the following keys:

|Key|Value|
|---|---|
|`"data"`|The JSON object received as request data payload.|
|`"parallels"`|A list of JSON objects describing parallels found.|

A JSON object in the `"parallels"` list of the successful response data payload contains the following keys:

|Key|Value|
|---|---|
|`"source"`|A string representing the CTS URN for the text span used as the source in this parallel.|
|`"target"`|A string representing the CTS URN for the text span used as the target in this parallel.|
|`"match_tokens"`|A list of strings, where each string is a token found in both the source span and the target span.|
|`"score"`|A number representing the score assigned to the pair of text spans.|
|`"source_raw"`|The string making up the text span specified by the value of `"source"`.|
|`"target_raw"`|The string making up the text span specified by the value of `"target"`.|
|`"highlight"`|A list of strings representing CTS URNs that define which parts in the source and target spans were used to determine the score.|

> NB:  A successful response body will be compressed with gzip.

On failure, the response is a 404 error.

### Examples

#### Retrieving Search Results

Assume that the identifier `id1` is associated with a certain search result.

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/parallels/id1"
```

Response:

```
HTTP/1.1 200 OK
...
Content-Encoding: gzip
...

...
```

#### Attempting to Retrieve Search Results that Do Not Exist

Assume that the identifier `i-expired` is not associated with any search results in cache.

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/parallels/i-expired"
```

Response:

```
HTTP/1.1 404 Not Found
...
```
