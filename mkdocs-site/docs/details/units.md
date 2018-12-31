# Units

This page details the concept of textual units and describes JSON objects permitted in the `"source"` and `"target"` keys of the JSON data payload required by the `/parallels/` endpoint.

## Summary by Example

To get all of the _Aeneid_ by lines:
```
{
  "cts_urn": "urn:cts:latinLit:phi0690.phi003",
  "units": "line"
}
```

To get book 1 of the _Aeneid_ by phrases:
```
{
  "cts_urn": "urn:cts:latinLit:phi0690.phi003:1",
  "units": "phrase"
}
```

## Introduction

Because Tesserae's algorithm works by comparing spans of text, it is necessary to break up a full text into spans of text.  The Tesserae algorithm then compares each span of text labeled as part of the source text with each span of text labeled as part of the target text.  We call these spans of text "units".

## JSON Object

The JSON object specifying which units to extract from what work has the following keys:

|Key|Value|
|---|---|
|`"cts_urn"`|A string representing the CTS URN of the work of interest.|
|`"units"`|A string representing the unit of interest.  Accepted values are described below in [Permitted Units](#permitted_units)|

## Permitted CTS URNs

Acceptable CTS URNs for `"cts_urn"` are either the entire work or by the first level of canonical referencing (e.g., by book of an epic).

## Permitted Units

### Lines

One way to divide the text is by line.  In the case of poetry, lines are inherent to the structure of the text.  In the case of prose, lines are arbitrarily enforced by the referencing conventions used by scholars of the prose work.

To specify division of a text by line, set the `"units"` key to the `"line"` value.

### Phrases

Another way to divide the text is by phrase.  Phrases in a text are delimited by ending punctuation provided by the editors of the edition of the text.

To specify division of a text by phrase, set the `"units"` key to the `"phrase"` value.

