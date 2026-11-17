------------------------------- MODULE Clock -------------------------------
\* The chess clock server (main.py) in whole seconds. Each action is one
\* route; Tick is a second of wall time folded in by /state, /switch or
\* /pause while the clock runs.
\* Broken = TRUE is the code before the fix: /switch took any player number,
\* /start reset the players but not the global time, and the global time
\* ran on below zero.
EXTENDS Naturals, Integers

CONSTANTS Broken, Total

VARIABLES started, paused, finished, active, p1, p2, global

vars == <<started, paused, finished, active, p1, p2, global>>

Init ==
  /\ started = FALSE /\ paused = FALSE /\ finished = FALSE
  /\ active = 0 /\ p1 = 0 /\ p2 = 0 /\ global = Total

Start ==
  /\ Broken \/ ~started
  /\ started' = TRUE /\ paused' = FALSE /\ active' = 1 /\ p1' = 0 /\ p2' = 0
  /\ UNCHANGED <<finished, global>>

Switch(p) ==
  /\ started /\ ~paused /\ ~finished
  /\ Broken \/ p \in {1, 2}
  /\ active' = p
  /\ UNCHANGED <<started, paused, finished, p1, p2, global>>

Pause ==
  /\ started /\ ~finished
  /\ paused' = ~paused
  /\ UNCHANGED <<started, finished, active, p1, p2, global>>

Tick ==
  /\ started /\ ~paused /\ ~finished
  /\ Broken \/ global > 0
  /\ global >= -1
  /\ global' = global - 1
  /\ p1' = IF active = 1 THEN p1 + 1 ELSE p1
  /\ p2' = IF active = 2 THEN p2 + 1 ELSE p2
  /\ finished' = (~Broken /\ global - 1 = 0)
  /\ UNCHANGED <<started, paused, active>>

Reset ==
  /\ started' = FALSE /\ paused' = FALSE /\ finished' = FALSE
  /\ active' = 0 /\ p1' = 0 /\ p2' = 0 /\ global' = Total

Next == Start \/ Pause \/ Tick \/ Reset \/ \E p \in {1, 2, 3} : Switch(p)

Spec == Init /\ [][Next]_vars

\* The two players' clocks add up to the game time used.
TimeAddsUp == p1 + p2 + global = Total

\* The game clock never runs below zero.
ClockStopsAtZero == global >= 0

\* While a game runs, the clock is on one of the two players.
ActiveIsAPlayer == started => active \in {1, 2}
=============================================================================
