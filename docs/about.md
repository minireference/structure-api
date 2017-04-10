Subjects, topics, and concepts
==============================

Intro
-----
Every content-based website and mobile app needs a way to display, link to, and
organize categories of content that are accessible. A first click on a category
usually takes the user to a "list view" for the category, from where the user
can click through to the "detail page" of the content item.
The structure of the website is usually represented as a hierarchy of subfolders.
This works well enough, but I think we can do better.

Imagine a graph $G=(V,E)$ where the vertices $V$ represent all subjects, topics,
and concepts and the edges $E$ describe various links between them. In particular
I have settled on the following three type of links:

  - `ispartof`/`contains`: denote folder-like containment structure (but the same
     node can appear in multiple folders, analogous to using hard links in UNIX.)
  - `prerequsite`/`usedfor`: describe dependency relations that can be followed
     in both direction: to find subjects/topics/concepts I should read before
     reading current node, and to see what I can use the current node for in the
     future.
  - `related`: generic relation between concepts
  
**Note--this project is in very early stage of development and the author would
really appreciate feedback about the proposed design. If you have any ideas about
other types of nodes or relationships that I should think about, please send me an email.
I'm first dot last at gmail.**

Example of different types of nodes and relations:
  - `topic:math/quadratic_equation` which contains the definitions of `concept:math/quadratic_equation` and `concept:math/quadratic_formula`
  - `topic:physics/kinematics/UAM`, which is part of `topic:physics/mechanics/kinematics`,
    which is part of `subject:physics/mechanics`.
  - We can usefully describe a dependency relation `topic:math/quadratic_equation --usedfor--> topic:physics/kinematics/UAM`
    to indicate to the student some problems involving the position equation $x(t)=x_i + v_it + \frac{1}{2}at^2$ that describes
    uniform accelerated motion (UAM) requires knowing how to solve equations of the form $ax^2+bx+c=0$.
  - By specifying dependencies at the at the most specific level of description, all other levels of description can be inferred.
    For example, aggregating all dependencies for a subject will show us,
    `subject:physics/mechanics --prerequsites--> [ concept:math/quadratic_equation, topic:math/quadratic_equation, ... ]`,
    which represents a list of specific things you need to know before learning kinematics.
    If we want to see a dependency relation between subjects, we would return
    `subject:physics/mechanics --prerequsite--> subject:high_school_math`.
 


Applications
------------
We want to use a "design in the context of use" approach for building the API,
so it's important to imagine the use cases for the graph API. How will you query
the thing, and what will you use it for?

### Browsing

Consider a landing webpage that looks something like this:


    =================   MY WEBSITE HOMEPAGE ================
    
        Catchy catch phrase that is also easy to
        pronounce, sounds well and also illustrates
        how the site name can used as a verb.


        Physics            Mathematics         Subject3
         Mechanics           Calculus           Subject6
          - derivatives       - limits           - topic61
          - gravity           - derivatives      - topic62
          - kinematics        - integrals        - topic63
         Electricity         Linear_algebra     Subject9
         Magnetism           Probability
         

    =========================================================


Once a user clicks on `topic:kinematics` they see the "detail view," which surfaces
everything we have about that node from the graph:

    ----------------------------------------------------------------------------
    Prerequisites:                                                           (1)
    algebra, functions, quadratic_equation
    ----------------------------------------------------------------------------
                                              /physics/mechanics/kinematics  (2)
    
    Kinematics
    
    Kinematics (from the Greek word 'kinema' for motion) is the study of trajectories
    of moving objects. The motion of an objects is described by three functions:
     - position x(t)
     - velocity v(t)
     - acceleration a(t)
    You can use the equations to predict the motion of object and to ...

    [ Definitions   ]  [ UVM     ] [ UAM     ] [ Explanations ] [ Exercises ] \
    [               ]  [         ] [         ] [              ] [           ]  \
    [               ]  [         ] [         ] [              ] [           ]  / 
    [               ]  [         ] [         ] [              ] [           ] /
    
    ----------------------------------------------------------------------------
    Applications:                                                            (3)
    projectile_motion 
    ----------------------------------------------------------------------------

The UI items labeled (1), (2), and (3) are obtained from the STRUCTURE API, while
the main content of the page (the article on kinematics) comes from a content server.

Of course we can forego the content and just browse the graph as a graph, cf.
https://www.khanacademy.org/exercisedashboard ,
https://conceptcoaster.com/course/python-tutorial/ ,
and https://www.metacademy.org/graphs/concepts/bayesian_naive_bayes#focus=2o1gkpjm&mode=explore 



### Content recommendation

The issue with deep taxonomies and categorization is that they can be overwhelming.
Imagine browsing the list of 50 subjects, thousands of topics and thousands of concepts.
Yeah, that will be a long list!

What if we we had smart list that "recommends" the next topics for you to consider.
Define the `LearnerProfile` to be a model of what the student currently knows.
This student's profile would take into account:

  - student claims: every student can see and edit their profile and indicate which
    topics they `know`, `know about`, or `don't know` (maybe also `don't even know`).
  - student's browsing history
  - student's results on quizzes, exercises, and problems solved

A recommendation service can then recommend logical "next steps" for the student.
I'm not thinking machine learning here---just a smart walk of the graph in code.

I'm imagining a list view in a mobile app that continuously auto-populates with
subjects, topics, and concepts for the student to read next. This "smart list view"
represents the topics on the student's "learning horizon." Roughly speaking we
want to show the set of topics the students have the prerequisites for minus the
set of topics they already know.

The STRUCTURE API and the UUIDs assigned to different nodes will serve as the
data representation for this recommendation service:

```
>>>
GET  /recommend/?profile=[ '{{UUID}}':"knows", '{{UUID2}}':"knows", ... ]

<<<
{ next: [
    { "id": "{UUID3}"
      "reason": "You can use the quadratic equation to solve kinematics problems"
    },
    {...}, ... ] }
```          






