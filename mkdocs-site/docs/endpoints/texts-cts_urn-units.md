# `/texts/<cts_urn>/units/`

The `/texts/<cts_urn>/units/` endpoint provides CTS URNs for units and subreferences within a specific text.  This endpoint may be useful, for example, when determining what CTS URNs to list in `"source"` for a search query submission at `/parallels/`.

Note that `<cts_urn>` is a placeholder to be replaced by a [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding) CTS URN refering to a specific text.  (Modern web browsers tend to percent encode URLs by default, but if you are using a different method to query the API, you will have to percent encode the CTS URN yourself.  A variety of resources online can help you do this; query for "percent encode" in your favorite search engine to find them.)  Throughout the rest of this page, `<cts_urn>` will continue to serve as a placeholder for a percent encoded CTS URN.

## GET

Requesting GET at `/texts/<cts_urn>/units/` provides lists of CTS URNs identifying partitions of the work specified by `<cts_urn>`.

Note that by default, a GET request at `/texts/<cts_urn>/units/` will return an empty JSON object in the response data payload.  The desired lists must be specified by URL query fields.

### Request

To obtain lists of CTS URNs, the desired lists must be specified by URL query fields.  If one of the following fields is specified in the URL, a corresponding list of CTS URNs will be returned:

|Field Name|Field Value|
|---|---|
|`lines`|The list of returned CTS URNs partition the text by lines (if the text is poetry) or by paragraphs (if the text is prose).|
|`phrases`|The list of returned CTS URNs partition the text by phrases; a phrase is separated from a neighboring phrase by punctuation.|

### Response

On success, the response includes a JSON data payload consisting of a JSON object which may contain any of the following keys:

|Key|Value|
|---|---|
|`"lines"`|An array of strings representing CTS URNs that partition the text into lines (if the text is poetry) or paragraphs (if the work is prose).|
|`"phrases"`|An array of strings representing CTS URNs that partition the text into phrases.|

The specified key appears in the response data payload only when there was a corresponding URL query field in the request.

### Examples

#### Query without Any Filters

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/units/"
```

Response:

```
HTTP/1.0 200 OK
...

{}
```

#### Query for CTS URNs Specifying the Lines of the Text

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/units/?lines=true"
```

Response:

```
HTTP/1.0 200 OK
...

{
  "lines": [
    "urn:cts:latinLit:phi0917.phi001:1.1",
    "urn:cts:latinLit:phi0917.phi001:1.2",
    ...
  ]
}
```

#### Query for Both Line and Phrase CTS URNs

Request:

```
curl -i -X GET "https://tesserae.caset.buffalo.edu/texts/urn%3Acts%3AlatinLit%3Aphi0917.phi001/units/?lines=true&phrases=true"
```

Response:

```
HTTP/1.0 200 OK
...

{
  "lines": [
    "urn:cts:latinLit:phi0917.phi001:1.1",
    "urn:cts:latinLit:phi0917.phi001:1.2",
    ...
  ],
  "phrases": [
    "urn:cts:latinLit:phi0917.phi001:1.1-1.8",
    "urn:cts:latinLit:phi0917.phi001:1.9",
    ...
  ]
}
```
