# `/matches/`

The `/matches/` endpoint interacts with Tesserae's intertext discovery capabilities.

## POST

Requesting POST at `/matches/` submits a query for discovering intertexts between the texts available in Tesserae's database.  The query parameters should be sent as a JSON data payload.

### Request

The JSON data payload representing query parameters must contain the following keys.

TODO:  On the live server, should we limit the amount of source and target texts allowed to be queried?

|Key|Description|
|---|---|
|`source`|A list of strings representing CTS URNs that identify a unit.  The units will be compared with the units listed in `target` to find intertexts.|
|`target`|A list of strings representing CTS URNs that identify a unit.  The units will be compared with the units listed in `source` to find intertexts.|
|`method`|A JSON object describing the scoring method used to evaluate the intertextual strength of a source text and target text pair.  More information on specifying the scoring method can be found in [Scoring Methods](../details/methods.md).|

### Response

On success, the data payload contains … TODO:  Figure out what this contains

On failure, the data payload contains error information in a JSON object with the following keys:

|Key|Description|
|---|---|
|`"data"`|The JSON object received as request data payload.|
|`"message"`|A string explaining why the request data payload was rejected.|

### Examples

TODO:  add examples
