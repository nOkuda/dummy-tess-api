# Canonical Text Services Uniform Resource Names (CTS URNs)

This page describes some of the basic concepts of CTS URNs used in Tesserae.

## Referencing Convention

The CTS URN standard is a convention for helping two people reference the same thing in a digital text.  For example, suppose you wish to discuss line 10 of book 1 of the digital copy of Homer's _Iliad_ available on the Perseus website.  By providing the appropriate CTS URN, others can follow your discussion by referencing the same digital copy which you referenced when you were forming your points.

There are some technical details about what exactly goes into making a CTS URN, but for purposes of using them, it is sufficient to know the following:

* The various parts of the CTS URN will be separated by a colon (`:`).
* The first four parts of the CTS URN identify the work.
    * e.g., any CTS URN that begins with `urn:cts:greekLit:tlg0012.tlg001` refers to Homer's _Iliad_
* The fifth part, if given, allows for referencing a canonical unit within the work.
    * e.g., the CTS URN `urn:cts:greekLit:tlg0012.tlg001:1` refers to book 1 of Homer's _Iliad_

## Further Resources

* The Homer Multitext Project
    * CTS URN overview, a more thorough primer (with some errors):
        * [https://www.homermultitext.org/hmt-doc/cite/cts-urn-overview.html](https://www.homermultitext.org/hmt-doc/cite/cts-urn-overview.html)
* The CTS URN specification, in unadulterated formality:
    * [http://cite-architecture.github.io/ctsurn_spec/](http://cite-architecture.github.io/ctsurn_spec/)
* Perseus Digital Library + CTS URNs:
    * [http://cts.perseids.org/](http://cts.perseids.org/)
