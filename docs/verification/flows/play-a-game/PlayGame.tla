------------------------------ MODULE PlayGame ------------------------------
\* Two players sharing one chess clock page, with a 2-second game.
EXTENDS Naturals

VARIABLES screen, left, turn

vars == <<screen, left, turn>>

Init == screen = "setup" /\ left = 2 /\ turn = 1

YouStart == screen = "setup" /\ screen' = "running" /\ turn' = 1 /\ UNCHANGED left
SecondPasses == screen = "running" /\ left > 0 /\ left' = left - 1
                /\ screen' = (IF left = 1 THEN "over" ELSE "running") /\ UNCHANGED turn
PlayerMoves == screen = "running" /\ turn' = 3 - turn /\ UNCHANGED <<screen, left>>
YouPause == screen = "running" /\ screen' = "paused" /\ UNCHANGED <<left, turn>>
YouResume == screen = "paused" /\ screen' = "running" /\ UNCHANGED <<left, turn>>
YouReload == screen \in {"running", "paused"} /\ UNCHANGED vars
YouReset == screen # "setup" /\ screen' = "setup" /\ left' = 2 /\ turn' = 1

Next == YouStart \/ SecondPasses \/ PlayerMoves \/ YouPause \/ YouResume \/ YouReload \/ YouReset

Spec == Init /\ [][Next]_vars

\* The game ends exactly when its time runs out.
EndsAtZero == (screen = "over") <=> (left = 0)
=============================================================================
