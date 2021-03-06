## Sun 19 May 2018 14:11:13 EDT

Checked YAML loading works for miniref and ccssm data. Woo hoo... I thought I had
left the project in a much worse state, but everything seems to work: two pass
loading procedure that creates all nodes first before creating edges.

TODO = implement some sort of "missing nodes" print statement to indicate which
edges were not created because of missing referents.

Here is a sample node json as of this commit:

    {
        "id": "433e468e-412c-4329-b89c-14224ed06831",
        "path": "math/calculus",
        "scope": "miniref",
        "version": "0.1",
        "created_at": "2018-05-20T07:38:22+0000",
        "modified_at": "2018-05-20T07:38:22+0000",
        "comment": null,
        "prerequisites": [
            {
                "prerequisite": {
                    "id": "867e14e3-979d-43ea-b307-cc2a5faee145",
                    "path": "math/functions",
                    "scope": "miniref"
                },
                "explain_prerequisite": null,
                "level": "All"
            }
        ],
        "usedfors": [
            {
                "usedfor": {
                    "id": "9032aed4-20fb-48a4-8353-855d3d7f6386",
                    "path": "math/differential_equations",
                    "scope": "miniref"
                },
                "explain_usedfor": null,
                "level": "All"
            },
            {
                "usedfor": {
                    "id": "148999ae-ca1d-4a43-827d-e7b670763f25",
                    "path": "physics/classical_mechanics",
                    "scope": "miniref"
                },
                "explain_usedfor": null,
                "level": "All"
            },
            {
                "usedfor": {
                    "id": "d8d5f63d-00e3-49e4-aec6-1fd7b9c34d18",
                    "path": "physics/quantum_mechanics",
                    "scope": "miniref"
                },
                "explain_usedfor": null,
                "level": "All"
            }
        ],
        "related": [
            {
                "related": {
                    "id": "c3291ac0-54ca-4a0f-937b-d29ec5563a76",
                    "path": "math/calculus/integrals",
                    "scope": "miniref"
                },
                "explain_related": "Derivatives and integrals are inverse operations. Learning about one will help you understand the other.",
                "level": "UGRAD"
            }
        ],
        "contents": [
            {
                "child": {
                    "id": "8b61ca50-8eaa-4474-bb3f-d31980fbaa21",
                    "path": "math/calculus/derivatives",
                    "scope": "miniref"
                },
                "explain_contains": null,
                "level": "All"
            },
            {
                "child": {
                    "id": "c3291ac0-54ca-4a0f-937b-d29ec5563a76",
                    "path": "math/calculus/integrals",
                    "scope": "miniref"
                },
                "explain_contains": null,
                "level": "All"
            }
        ],
        "ispartof": []
    },



## Tue 18 Apr 2017 18:04:32 EDT

Okay so after a lot of work, we finally have a working version of YAML loading
from a directory. First we start from a clean slate:

    ./manage.py deletenodesandrelns
    All Nodes and Relations deleted

Next we load all data from `miniref/`:

    ./manage.py loadfromyamldata ../data/miniref/
    Loaded YAML data from dir ../data/miniref/

Next we refactor (today) and add some more classes (tomorrow).




## Mon 10 Apr 2017 16:58:23 EDT

This might be useful for dumping the DB as SQL for later comparison

    pg_dump  --data-only --table ?? --table ??? struct



## Mon 10 Apr 2017 13:05:50 EDT

I'm picking up the pieces I left behind this summer. The project is pretty much
all over the place... but I'll now focus on the django implementation and get it
to work.
Also the whole django configurations is so complicated fro nothing. I should
cleanup the project at some point, but not today.

The main issue I'm finding a problem with today is the concept of "missing references"
if the import operation is "complete" containing all endpoints between Nodes, then
the import can proceed as a two phase process:
  - create Nodes
  - create Links

But what do we do if some references are missing? Do we create a "stub" Node with
just it's path? This will require an "update" operation in the future when we 
import the Node contents for real.

We could skip importing links with missing endpoints altogether, and only import
them in the future, again requiring an update operation.

Let's think for a moment what the usage of the import commands would be like.


### Command usage

For initial import of data:

    ./manage.py importfromyamldata ../data/miniref/

Then, let's say you update some of the yaml files:

    ./manage.py updatefromyamldata ../data/miniref/

In this model the yaml files are the main source of truth and whatever is in the
DB gets overwritten. I'm not sure this is the best model, as it would be much 
nicer to have the option to "sync" between what's in the DB and what's in the FS.

One possibility that could work well is to use git-mediated sync:

  - To perform the import or update from file system to DB, we make a git commit
    and then store the commit id along with the data. Whatever was in the database
    gets completely overwritten (presumably you ran an export step before the import).
  - Next, the STRUCTURE-API runs for a few weeks, people make updates to the data
    through the admin interface or by making API calls.
  - To perform an export from the DB to the filesystem, we perform the following steps:
      - Checkout --hard the git revision that corresponds to the last import
      - Create a new branch, e.g., `export-8919381`
      - The above two steps can be performed using the command:  
        `git checkout -b export-8919381 <commit_of_last_import>`
      - Perform the export overwriting completely the filesystem contents
      - Try to rebase the branch `export-8919381` onto the latest version of `master`

I just ran this idea by Naomi and she pointed out two problems with it:
  - Since git doesn't know anything about the database constraints, it's possible
    to have git two accept two git changes (e.g. two pull requests) that create
    the same `path` ids. 
      - A possible solution to this is to use a `pre-merge` hook that checks the
        DB constraints are satisfied, currently `unique_together('scope', 'path')`
  - The other question is, "why are github pull requests good for collaboration?".
    Does it make sense to receive small or large pull requests? If someone adds
    1000+ lines of biology prerequisites, how will I check the data?
      - I don't really have a good response for this, but it seems like git gives
        use a lot of power + `git rebase` is quite powerful and could be useful
        in the long term.
  - A third potential problem I just thought about is the need to enforce consistent
    ordering of data exported to yaml files. In order for diffs to make sense, we
    need to always export nodes in the same order, and keys also.


Okay, seem like it could work, but lunch is priority right now.
