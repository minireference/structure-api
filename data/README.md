Graph data
==========

The basic format for data entries is as follows:

```yaml
-
  path: math/calculus/derivatives
  aliases:
    - math/differential_calculus
  description: >
      The study of continuous change in a single variable.
      Limits, derivatives, maximization and problem solving.
      Extremely important to physics and many other sciences.
      First part of the minimum calculus course.
  books: any calculus book should do. Exercises with solutions recommended.
  prerequisites:
      - math/functions
      - math/algebra
  usedfors:
      - math/calculus/multivariable
      - math/calculus/vector
  relations:
      - math/calculus/integral
```

Relationships can be described more fully using the alternative format, which
also explains the connection:

```yaml
-
  path: math/calculus/derivatives
  aliases:
    - math/differential_calculus  
  description: >
      The study of continuous change in a single variable.
      Limits, derivatives, maximization and problem solving.
      Extremely important to physics and many other sciences.
      First part of the minimum calculus course.
  books: any calculus book should do. Exercises with solutions recommended.
  prerequisites:
      -
        prerequisite: math/functions
        explain: You need to know about functions before you learn to compute limits and derivatives.
        level: HS
      -
        prerequisite: math/algebra
        explain: Manipulating limits and derivative expressions requires using algebra skills.
        level: HS
  usedfors:
      -
        usedfor: math/calculus/multivariable
        explain: You can use derivatives on multivariable functions like $f(x,y,z)$.
      -
        usedfor: math/calculus/vector
        explain: You can use take derivatives of vector fields.
  relations:
      -
        related: math/calculus/integrals
        explain: Derivatives and integrals are inverse operations. Learning about one will help you understand the other.
        level: UGRAD
```

Future schema
-------------
The following properties are likely to be added:

  - `__class__`: to represent what type of entry, e.g. `SubjectNode`, `TopicNode`,
    or  `ConceptNode`.
  - `contents` and `partof`
  - `scope` (though can be  automatically infer from folder)
  - `aliases` might have 

Scope
-----
When resolving a path like `math/calculus/derivatives` the API can return multiple results:

  - if nodes of different type exists (the derivatives subject and derivatives topic)
  - if node of same type but different scope, e.g. `scope:general` for nodes
    in the common graph, and `scope:miniref` for structure nodes used specifically
    to build Minireference Co. books and websites.
    We assume client applications will resolve the results and display the most
    relevant scope to the user.
  - the uniqueness constrained we impose is:
      
        unique_together('__class__', 'scope', 'path')

I'm thinking of scopes as layers, with name resolution starting at the top most
layer, and proceeding according to a "scope order," analogous to how method name
resolution work in Python subclasses.

The file `scopedir/context.yml` will contain the default settings for all data
files in the directory `scopedir`.


Aliases and UUIDs
-----------------
When importing a data file, node UUIDs can be stored inline, or specified in a
`uuids.yml` file in the folder, or left unspecified and resolved/created later.

### Special symbols
These can be used to link to specify a particular scope, node type, or level for a given path:

  - Class prefix of the form: `c:` or `concept:`, `t:` or `topic:`, and `s:` or `subject:`
  - Scope prefix of the form `miniref::` or `ccssm::`
  - Level suffix  `|PS`, `|HS`, `|UGRAD`, or `|GRAD`
  - Specific node UUID:  `id:{{UUID}}`



Sources
-------
Some of the initial descriptions were inspired by math subject lists taken from: 
http://functionspace.org/articles/10 and https://news.ycombinator.com/item?id=8697772 .
