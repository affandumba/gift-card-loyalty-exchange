# Lab 4 - Vibe Coding: Pac-Man Repair

**Name:** Affan Dumba | **SRN:** PES1UG24CS280 | **Section:** E
**Starter repo:** SETAPESU26/34_pacman (cloned, no PR raised to it)
**LLM used:** Claude (Claude Code)

## What is in this folder

| File | What it is |
|---|---|
| `game.py` | final game after all fixes |
| `original_code/game_original.py` | starter code, untouched |
| `Lab4_Before_...mp4` | 10 s of the original build - power pellet does nothing |
| `Lab4_After_...mp4` | 10 s of the fixed build - ghosts turn frightened, each in its own colour |
| `Lab4_After_Features_...mp4` | 14 s showing bonus life, bonus fruit and the win screen (score pre-set to 900 so it fits in a short clip) |
| `Lab4_Chat_History_...pdf` | chat with the LLM |
| `tools/play_and_record.py` | script used to record the clips |

The clips are screen captures of the real `game.py` window. The arrow-key presses are sent by a small autopilot script (it posts normal pygame key events) so the runs are repeatable.

## Task 1 - power pellet bug

`eat()` compared the cell with `"O"` but the maze uses lowercase `"o"`, so the frightened branch never ran. Changing it to `"o"` fixed it: `fright_left` is set to 3 s and every ghost that is not eaten reverses once.

## Task 2 - `ghost_color(name, mode)`

Returns a different tint per ghost in `frightened` mode (Blinky magenta, Pinky violet, Inky green, Clyde yellow). For `normal` and `eaten` it returns `None` so the default colours are kept.

## Task 3 - `on_pellet_eaten(score, pellets_left)`

- 30 pellets left: a cherry appears at row 3, col 10; eating it gives +100.
- 1 pellet left: the HUD text flashes red for about 1.5 s.
- The state lives in a small `BONUS` dict that `Game.reset()` clears, so pressing R does not leave an old cherry behind.

## Task 4 - `bonus_life_threshold()`

Returns `1000`. The README suggests 10000 but the maze only has 130 pellets (about 1300 points), so 10000 would never trigger. At 1000 the extra life is reachable.

## How I checked it

- Called `eat()` on a power pellet cell: `fright_left` became 3.0 and all ghost directions flipped.
- Same autopilot and random seed on both versions: the original never goes frightened, the fixed one does and ghosts can be eaten for +200.
- Feature clip: score reaches 1000 and lives go 3 -> 4, the cherry adds 100, the game ends in the win state.

## Prompts, in short

1. Gave the assistant the handout and repo and asked it to do the lab.
2. It found the `"O"` / `"o"` mismatch and fixed it (worked first attempt).
3. Implemented the three empty hooks one by one, checking each against what the README says about when it is called and what it returns.
4. Asked for before/after videos, then asked for them to be real window recordings instead of simulated frames.

Full chat: see `Lab4_Chat_History_Affan_Dumba_PES1UG24CS280.pdf`.
