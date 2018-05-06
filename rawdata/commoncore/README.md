Common Core State Standards for Mathematics
===========================================
This directory contains the data of the common core state standards for math,
in YAML format suitable for importing into the structure-api.

The common core follows a fairly deep hierarchy:

    Set
      Grade               e.g. 6        = 6th grade
        Domain            e.g. 6.EE     = Expressions and Equations 
          Cluster         e.g. 6.EE.A   = Apply and extend previous under...
            Standard      e.g. 6.EE.2   = Write, read, and evaluate expr...
              Component   e.g. 6.EE.2.c = Evaluate expressions at specific...

Roughly speaking CCSSM domains correspond to `Subject` nodes, while clusters,
standards, and their components can all be classified as topics.


Desired results
---------------
For the purpose of demonstrate the capabilities of the `structure-api`, we want
to show a graph of the prerequisites between common core `Standards`.
At a later stage we could provide a mapping between standards and `miniref:Topic`s
(as in a topic can `cover` one or more standards) and also possibly a mapping
between which `miniref:Concept`s are used in each standard.

A sample output of a Standard includes the following fields:

```yaml
-
  path: 6.EE.B.5
  __class__: Standard
  aliases:
    - 6.EE.5
  description: >
    Understand solving an equation or inequality as a process of answering a question:
    which values from a specified set, if any, make the equation or inequality true?
    Use substitution to determine whether a given number in a specified set makes
    an equation or inequality true.
  contents:
  ispartof:
    - 6.EE.B
  prerequisites:
    - 6.EE.A.2
  usedfors:
    - 8.EE.A.2
    - 8.EE.C.8
  related:
    - 6.EE.B.7
    - 6.EE.B.8
  ccss_guid: 130F1CC227FF4C219095EC708C237FCD
  ccss_url: http://corestandards.org/Math/Content/6/EE/B/5
  asn_url: http://purl.org/ASN/resources/S11434DD

```


Data pipeline
-------------
The pre-processing required to produce the datasets include numerous steps:

  - Obtain a short `path` for each domain:
    - infer a path for `Domain`s from its cluster child elements
    - infer a path for `Cluster`s from statementNotation
  - `guid`: ensure existence of the globally unique identified (GUID) provided by the common core
  - ensure ccss_url returns a 200 [TODO]
  - meld with cleaned edge data:
    - remove `||` comments
    - expand `,`-  and `;`- separated lists
    - confirm existence of `Standard`s for all edge endpoints
    - remove duplicate edges and self-edges (we remove all edge and node comments from xls file)

See the jupyter notebook `data_import_pipeline.ipynb` for details.


Manual annotations
------------------
  - Annotate each cluster with `focusLevel`, which is one of `major`, `additional`, or `supporting` [TODO]



Sources
-------
The official state standards can be obtained from [ASN](http://asn.jesandco.org/resources/ASNJurisdiction/CCSS).
Data is: Copyright 2010. National Governors Association Center for Best Practices and Council of Chief State School Officers,
licensed under [CC BY](http://creativecommons.org/licenses/by/3.0/us/).

The prerequisite structure was extracted from the [edge data](http://tinyurl.com/ccssmgraphdata)
of the common core dependency graph produced by Jason Zimba.
