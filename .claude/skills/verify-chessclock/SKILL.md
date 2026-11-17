---
name: verify-chessclock
description: Check that the chess clock's two player clocks always add up to the game time used, that the game clock stops at zero, and that the clock is always on a real player. Use when changing the routes in main.py (start, switch, pause, reset, state, set_global_time), _advance, or the polling and buttons in templates/index.html.
---

# Verify the chess clock

**Properties.** `TimeAddsUp`: player 1 time + player 2 time + global time left = the configured game time. `ClockStopsAtZero`: the global time never goes below zero, and the game ends there. `ActiveIsAPlayer`: while a game runs, the clock is on player 1 or player 2.

**Harm if broken.** Players see times that do not add up, a game that never ends, or time charged to nobody.

## Run

```sh
export TLA2TOOLS=/absolute/path/to/tla2tools.jar   # TLC 1.7.4 release
export JAVA=/path/to/java                          # Java 11 or later
bash scripts/verification/check-model.sh .claude/skills/verify-chessclock/model/Clock.tla
bash scripts/verification/check-model.sh .claude/skills/verify-chessclock/model/Clock.tla --mutant
uv run --with flask --with pytest python -m pytest -q tests
```

The model must pass (31 distinct states, 3-second game). The `--mutant` run replays the code before commits dc3d161, 07857be and 7a78940 and must report a violation. With one rule per config it reports `ActiveIsAPlayer` (switch to 3), `TimeAddsUp` (start, tick, start) and `ClockStopsAtZero` (ticks past zero). `tests/test_clock.py` replays each path on the real routes with a fake `time.time`. Read every TLC result with the pstack `/statechart` skill.

## Coverage

Synced with the code at commit `9c16e5f`. Move this forward only after you confirm that the model still describes the code at the new commit.

| Model step | Code (`main.py`) |
| --- | --- |
| `Start` | `start_game` |
| `Switch(p)` | `switch_player` |
| `Pause` | `pause_game` |
| `Tick` | `_advance`, called from `/state`, `/switch` and `/pause` |
| `Reset` | `reset_game` |

## Not covered

The clock is one global `game_state` shared by every visitor and every gunicorn worker: with more than one worker, each holds its own clock. Also not covered: `set_global_time`, fractional seconds, and the page's 100 ms polling, apart from the reload behavior that commit 9c16e5f fixed.
