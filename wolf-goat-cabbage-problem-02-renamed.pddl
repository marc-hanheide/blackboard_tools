;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; problem definition for wolf, goat, cabbage problem
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define 
    (problem boat2)
    (:domain boat)
    (:objects n s)
    (:INIT 
        (config s s s s)

        (valid n s n s)
        (valid s n s n)

        (valid n n n n)
        (valid n n s n)
        (valid n s n n)
        (valid s n n n)

        (valid s s s s)
        (valid s s n s)
        (valid s n s s)
        (valid n s s s)
     
     
    )
  
    (:goal (AND 
            (config n n n n)
        )
    )
)



