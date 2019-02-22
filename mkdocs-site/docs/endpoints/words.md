# `/words/`

The `/words/` endpoint interacts with Tesserae's database of words, as found in the literary works Tesserae has processed.

## GET

Requesting GET at `/words/` provides information on words stored in Tesserae's database.

### Request

The following fields may be used in a URL query to filter the response:

|Field Name|Field Value|
|---|---|
| `form` | Only database information for words with the specified form is returned. |
| `lemma` | Only database information for words with the specified lemma is returned. |

> NB:  Remember to percent encode field values when necessary.

### Response

On success, the response includes a JSON data payload consisting of a JSON object with the key `"words"`, associated with an array of JSON objects.  The JSON objects in the array, in turn, contain the following keys:

|Key|Value|
|---|---|
|`"form"`|A string matching the word's form.|
|`"lemmata"`|A list of strings, where each string is a possible lemma for this word.|
|`"language"`|A string indicating what language this word belongs to.|

### Examples

#### Search by One Field

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/words/?form=leges"
```

Response:

```
HTTP/1.1 200 OK
...

{
  "words": [
    {
      "form": "leges",
      "lemmata": ["lego", "lex"],
      "language": "latin"
    }
  ]
}
```

#### Search for Word Not Present in Database

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/words/?lemma=xlwbnd"
```

Response:

```
HTTP/1.1 200 OK
...

{
  "words": []
}
```
