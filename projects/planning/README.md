# Planning

## Warehouse Robots!

We're dealing with a number of fancy  pallet-moving robots that can help out in their warehouses.
This is a program to get these robots to move stock around the  warehouse.

The robots are capable of picking up pallets and moving them around 
the warehouse. They can get the pallets to the unloading area, but they need humans
to take the specific items off of them. 

\*The "R" stands for "Robotto."

## Problems

We have ___seven___ problem definitions. 
The first five are problems that the domain can solve, the
sixth and seventh are problems that it should __fail to create a plan for__. 

### The Domain File

The domain file contains the domain name and the relevant PDDL requirements:

```
(define (domain sokorobotto)
  (:requirements :typing)
  (:types  )
  (:predicates  )
)
```

1. The `:types` of all of the objects in your domain.
2. The names of all `:predicates`.
3. The bodies of all necessary actions, including parameters, pre-conditions,
and effects.


### Testing 

Test domain definitions using
```
python test.py <domain file> <problem file> [-v]
```
* The script will run for a bit (for more complicated problems, upwards
of ten seconds) and then give you the results ("ok" for a successful plan
or an error message otherwise).
* The full results also get stored in `<problem file name>_results.json`.
* The `-v` flag can be used print more detailed information: the successful
plan if one is found, or (minor) additional error information if not.

## On PDDL

7. When defining __predicates__ in PDDL, every predicate can be defined using the same variables, say, ?x and ?y, but when the predicates are used to define actions, the variable names cannot be reused. In other words, if ?x is used inside one predicate to denote something of type "fruit," then wherever it's used, it denotes "fruit." If a predicate is designed not to take a fruit as an argument and takes a vegeatable instead, then ?x cannot be used as an argument of that predicate.
8. The same predicate can apply to, say, boxes and tables, as long as both are defined as, say, "object." If the same kind of predicate needs to be defined to act on things of type "box" and things of type "table," then two different predicates will be needed; the same predicate cannot accept arguments of both types. However, one can imagine a predicate that handles both boxes and tables by accepting two arguments, one of type "box," one of type "table."
9. Remember to always think of an action in terms of __preconditions__ and __effects__: respectively the requirements that qualify the action to be taken and the results of the action. Be as detailed as possible to avoid undesired effects, which may be undesired not only in and of themselves, but also because they may prohibit certain preconditions from being met for a subsequent desired action.
