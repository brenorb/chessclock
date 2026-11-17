# Chess clock verification

| Skill | What it checks | Tool |
| --- | --- | --- |
| [verify-chessclock](../../.claude/skills/verify-chessclock/SKILL.md) | Player clocks add up to the game time used, the game ends at zero, and the clock is always on a real player | TLA+ / TLC, 31 states, plus `tests/test_clock.py` |

The model found three server bugs, now fixed, and the flow model below exposed a fourth in the page:

1. `/switch/3` charged time to nobody (dc3d161).
2. `/start` during a game cleared the players but kept the global time used (07857be).
3. The global time ran below zero and the game never ended (7a78940).
4. Reloading the page during a game showed an empty clock and offered to start again (9c16e5f).

## Play a timed game

Generated with pstack `/statechart` from [PlayGame.tla](flows/play-a-game/PlayGame.tla) ([TLC report](flows/play-a-game/report.md)). The chart hides seconds passing and page reloads, which leave the screen unchanged.

```mermaid
---
title: "Play a timed game"
---
stateDiagram-v2
  state "Legend" as legend {
    lg0: done
    lg1: idle
    lg2: playing
  }
  class lg0 orange
  class lg1 tan
  class lg2 blue
  s0: Set the game time
  s1: Player 1's clock running
  s2: Paused
  s3: Player 2's clock running
  s4: Time's up
  [*] --> s0
  s0 --> s1: you press start
  s1 --> s0: you reset
  s1 --> s2: you pause
  s1 --> s3: the player taps their clock
  s1 --> s4: the game time runs out
  s2 --> s0: you reset
  s2 --> s1: you resume
  s3 --> s0: you reset
  s3 --> s1: the player taps their clock
  s3 --> s2: you pause
  s4 --> s0: you reset
  s3 --> s4: the game time runs out
  s2 --> s3: you resume
  class s0 tan
  class s1 blue
  class s2 blue
  class s3 blue
  class s4 orange
```
