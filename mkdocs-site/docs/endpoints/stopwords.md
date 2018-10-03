# `/stopwords/`

The `/stopwords/` endpoint serves stopwords lists.  These lists can be useful when parameterizing the scoring algorithm at the `/parallels/` endpoint.

Stopwords lists are typically computed using frequency information.  The reasoning is that the most frequent features are typically the least informative (consider, for example, the articles in English).

## GET

Requesting GET at `/stopwords/` provides a stopwords list.  How this stopwords list was created is dependent on the URL query fields used.

By default, a GET at `/stopwords/` returns an empty list.

### Request

The following fields may be used in a URL query to specify the parameters by which the stopwords list is created:

|Field Name|Field Value|
|---|---|
|`feature`|A string specifying the linguistic feature by which frequencies are calculated; `lemma` is the default.|
|`list_size`|An integer specifying the number of stopwords to include in the stopwords list. `10` is the default.|
|`works`|A percent-encoded string of the form `<CTS URN 1>,<CTS URN 2>,...`, specifying which works are used to determine feature frequencies.  Alternatively, a string matching one of the languages in the Tesserae database will compute feature frequencies from the corpus of works in that language.|

### Response

On success, the response data payload will contain a JSON object with the key `"stopwords"`, associated with a list of strings.

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Value|
|---|---|
|`"data"`|A JSON object whose keys are the received URL query fields, associated with percent-decoded values.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

#### Get the 10 Highest Frequency Lemmata in Latin

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/stopwords/?works=latin"
```

Response:

```
HTTP/1.1 200 OK
...

{ 
  "stopwords": [
    ...
  ]
}
```

#### Get the 20 Highest Frequency Lemmata in Latin

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/stopwords/?works=latin&list_size=20"
```

Response:

```
HTTP/1.1 200 OK
...

{ 
  "stopwords": [
    ...
  ]
}
```

#### Get the 15 Highest Frequency Lemmata in Two Specific Texts

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/stopwords/?works=urn%3Acts%3AlatinLit%3Aphi0917.phi001%2Curn%3Acts%3AlatinLit%3Aphi0690.phi003.opp-lat1&list_size=15"
```

Response:

```
HTTP/1.1 200 OK
...

{ 
  "stopwords": [
    ...
  ]
}
```

#### Attempt to Get a Stopwords List with a Text Not in the Database

Suppose the CTS URN `DEADBEEF` does not exist in the database.

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/stopwords/?works=DEADBEEF&list_size=15"
```

Response:

```
HTTP/1.1 400 Bad Request
...

{
  "data": {
    "works": ["DEADBEEF"],
    "list_size": 15
  },
  "message": "The CTS URN provided (DEADBEEF) does not exist in this database."
}
```
