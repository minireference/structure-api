## Mon 10 Apr 2017 16:58:23 EDT

This might might be useful for dumping the DB as SQL for later comparison

    pg_dump  --data-only --table ?? --table ??? struct



## Mon 10 Apr 2017 13:05:50 EDT

I'm picking up the pieces I left behind this summer. The project is pretty much
all over the place... but I'll now focus on the django implementation and get it
to work.
Also the whole django configurations is sooo complicated fro nothing. I should
cleanup the project at some point, but not today.

The main issue I'm finding a problem with today is the concept of "missing references"
if the import operation is "complete" containing all endpints between Nodes, then
the import can proceed as a two phase process:
  - create Nodes
  - create Links

But what do we do if some references are missing? Do we create a "stub" Node with
just it's path? This will require an "update" operation in the future when we 
import the Node contents for real.

We could skip importing links with missing endpoints altogether, and only import
them in the future, again requiring an update operation.

Let's think for a moment what the usage of the import commands would be like.


## Command usage

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
