# `/parallels/`

The `/parallels/` endpoint interacts with Tesserae's intertext discovery capabilities.

## POST

Requesting POST at `/parallels/` submits a query for discovering intertexts between the texts available in Tesserae's database.  The query parameters should be sent as a JSON data payload.

### Request

The JSON data payload representing query parameters must contain the following keys.

TODO:  On the live server, should we limit the amount of source and target texts allowed to be queried?

|Key|Value|
|---|---|
|`"source"`|A list of strings representing CTS URNs, each identifying a text span.  The spans will be compared with the spans listed in `"target"` to find intertexts.|
|`"target"`|A list of strings representing CTS URNs, each identifying a text span.  The spans will be compared with the spans listed in `"source"` to find intertexts.|
|`"method"`|A JSON object describing the scoring method used to evaluate the intertextual strength of a source text and target text pair.  More information on specifying the scoring method can be found in [Scoring Methods](../details/methods.md).|

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
|`"highlight"`|A of list strings representing CTS URNs that define which parts in the source and target spans were used to determine the score.|


On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Value|
|---|---|
|`"data"`|The JSON object received as request data payload.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

