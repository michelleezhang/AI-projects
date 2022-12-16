(define (domain sokorobotto)
  (:requirements :typing :negative-preconditions)
  (:types 
    shipment order location robot pallette saleitem - object 
    robot pallette - movingobject
  )
  (:predicates
    (includes ?x - shipment ?y - saleitem)
    (ships ?x - shipment ?y - order)
    (orders ?x - order ?y - saleitem)
    (unstarted ?x - shipment)
    (packing-location ?x - location)
    (available ?x - location)
    (contains ?x - pallette ?y - saleitem)
    (free ?x - robot)
    (connected ?x ?y - location)
    (at ?x - movingobject ?y - location)
    (no-robot ?x - location)
    (no-pallette ?x - location)
    (holding ?x - robot ?y - pallette)
    (shipment-location ?x - location)
    (picked-up ?x - pallette)
  )

  ; this action changes the location of the robot only from loc1 to loc2
  (:action move
      :parameters (?robot - robot
                   ?loc1 - location
                   ?loc2 - location )
      :precondition (and (connected ?loc1 ?loc2)  ; is loc2 reachable from loc1?
                         (at ?robot ?loc1)        ; is the robot at loc1?
                         (free ?robot)            ; is the robot free?
                         (no-robot ?loc2))        ; is there no robot at loc2 ?
      :effect (and (at ?robot ?loc2)
                   (no-robot ?loc1)
                   (not (at ?robot ?loc1))
                   (not (no-robot ?loc2)))
  )

  ; this action changes the location of a robot holding a pallette (changes location of robot and pallette)
  (:action movep
      :parameters (?robot - robot
                   ?pallette - pallette
                   ?loc1 - location
                   ?loc2 - location)
      :precondition (and (connected ?loc1 ?loc2)
                         (at ?robot ?loc1)
                         (holding ?robot ?pallette)
                         (at ?pallette ?loc1)
                         (no-robot ?loc2)
                         (no-pallette ?loc2))
      :effect (and (at ?robot ?loc2)
                   (at ?pallette ?loc2)
                   (no-robot ?loc1)
                   (no-pallette ?loc1)
                   (not (at ?robot ?loc1))
                   (not (at ?pallette ?loc1))
                   (not (no-pallette ?loc2))
                   (not (no-robot ?loc2)))
  )

  ; this action "packs" -- we put the item from the palette at loc onto the shipment 
  (:action pack
      :parameters (?item - saleitem
                   ?pallette - pallette
                   ?order - order
                   ?shipment - shipment
                   ?loc - location)
      :precondition (and (at ?pallette ?loc)
                         (contains ?pallette ?item)
                         (orders ?order ?item)
                         (ships ?shipment ?order)
                         (not (unstarted ?shipment))
                         (shipment-location ?loc)
                         (packing-location ?loc))
      :effect (and (includes ?shipment ?item)
                   (not (contains ?pallette ?item)))
  )

  ; this action starts the robot packing 
  (:action start
      :parameters (?shipment - shipment
                   ?loc - location)
      :precondition (and (unstarted ?shipment) 
                         (packing-location ?loc)
                         (available ?loc))
      :effect (and (not(unstarted ?shipment))
                   (shipment-location ?loc)
                   (not(available ?loc)))
  )

  ; this action stops the robot packing
  (:action stop
      :parameters (?shipment - shipment
                   ?loc - location)
      :precondition (and (packing-location ?loc)
                         (shipment-location ?loc))
      :effect (and (not (shipment-location ?loc))
                   (available ?loc))
  )

  ; this action makes the robot pick up a pallette
  (:action pickup
      :parameters (?robot - robot
                   ?pallette - pallette
                   ?loc - location)
      :precondition (and (at ?robot ?loc)
                         (at ?pallette ?loc)
                         (free ?robot))
      :effect (and (holding ?robot ?pallette)
                   (picked-up ?pallette)
                   (not(free ?robot)))
  )

  ; this action makes the robot put down a pallette 
  (:action putdown
      :parameters (?robot - robot
                   ?pallette - pallette
                   ?loc - location)
      :precondition (and (at ?robot ?loc)
                         (holding ?robot ?pallette)
                         (picked-up ?pallette))
      :effect (and (not(holding ?robot ?pallette))
                   (not(picked-up ?pallette))
                   (free ?robot))
  )
)