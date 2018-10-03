# `/stopwords/lists/<name>/`

The `/stopwords/lists/<name>/` endpoint serves a specific curated stopwords list.  Note that `<name>` is a placeholder for the name of a curated stopwords list.

## GET

Requesting GET at `/stopwords/lists/<name>/` provides the curated stopwords list specified by `<name>`.

### Request

Again, `<name>` is a placeholder for the name of the desired curated stopwords list.  Names recognized by the server can be discovered at [`/stopwords/lists/`](stopwords-lists.md).

### Response

On success, the response includes a JSON data payload consisting of a JSON object with the key `"stopwords"` associated with an array of strings.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Value|
|---|---|
|`"name"`|A string matching the requested stopwords list name.|
|`"message"`|A string explaining why the request was rejected.|

### Examples

#### Query for Curated Stopwords List Already in Database

Suppose that `latin-lemma-10` is the name of one of the stopwords lists in the database.

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/stopwords/lists/latin-lemma-10/"
```

Response:

```
HTTP/1.1 200 OK
...

{
  "stopwords": [
    ...
    "et",
    ...
  ]
}
```

#### Query for Curated Stopwords List Not in Database

Suppose that `i-dont-exist` does not match any stopwords list names.

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/stopwords/lists/i-dont-exist/"
```

Response:

```
HTTP/1.1 400 Bad Request
...

{
  "name": "i-dont-exist",
  "message": "No stopwords list names match the specified name (i-dont-exist)."
}
```
