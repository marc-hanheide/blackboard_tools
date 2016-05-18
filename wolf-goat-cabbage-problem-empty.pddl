;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; problem definition for wolf, goat, cabbage problem
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define 
    (problem boat1)
    (:domain boat)
    ; only needs two objects, namely representing
    ; either banke side of the river, [w]est and [e]ast
    (:objects  w e)
    (:INIT 
        ; wolf, goat, cabbage, boat are all on 
        ; the west side to start with
        (config w w w w)

        (valid w w w e)
        (valid w w w w)

    )
  
    (:goal (AND 
            ; they all have to move to the east side
            (config w w w e)
        )
    )
)



