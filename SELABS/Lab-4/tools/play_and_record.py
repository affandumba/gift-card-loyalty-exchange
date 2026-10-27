"""Runs the real game.py in a normal window, drives it with an autopilot that posts
genuine arrow-key events, and screen-captures the window with ffmpeg (gdigrab).

usage: python play_and_record.py <game.py> <out.mp4> <caption> [seconds]
"""
import importlib.util
import os
import random
import subprocess
import sys
import threading
import time
from collections import deque

os.environ["SDL_VIDEO_WINDOW_POS"] = "40,40"
import ctypes

ctypes.windll.user32.SetProcessDPIAware()  # window and gdigrab capture then use the same pixels
import pygame  # noqa: E402

path, out, caption = sys.argv[1], sys.argv[2], sys.argv[3].replace(":", " -").replace("'", "")
seconds = float(sys.argv[4]) if len(sys.argv) > 4 else 10
preset = sys.argv[5] if len(sys.argv) > 5 else None

spec = importlib.util.spec_from_file_location("game_under_test", path)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

holder = {}
RealGame = g.Game


class CapturedGame(RealGame):
    def __init__(self):
        super().__init__()
        if preset == "features":
            # demo set-up only: start near the 1000-point bonus life and the fruit trigger
            self.score = 900
            near = sorted((c for c in self.pellets if g.MAZE[c[0]][c[1]] == "."),
                          key=lambda c: g.distance_sq(c, g.PLAYER_START))
            self.pellets = set(near[:34])
        holder["game"] = self


g.Game = CapturedGame
random.seed(int(os.environ.get("SEED", "7")))


def first_step(start, goals):
    goals = set(goals)
    seen, queue = {start}, deque([(start, None)])
    while queue:
        cell, first = queue.popleft()
        if cell in goals and first is not None:
            return first
        for d in g.DIRS:
            nxt = (cell[0] + d[0], cell[1] + d[1])
            if nxt in seen or g.is_wall(nxt) or nxt in g.HOUSE_CELLS:
                continue
            seen.add(nxt)
            queue.append((nxt, first or d))
    return None


def pick(game):
    me = tuple(game.player)
    fruit = getattr(g, "BONUS", {}).get("fruit")
    if fruit and first_step(me, [fruit]):
        return first_step(me, [fruit])
    if game.fright_left > 0.4:
        scared = [x.pos for x in game.ghosts if not x.eaten and x.pos not in g.HOUSE_CELLS]
        if scared and first_step(me, scared):
            return first_step(me, scared)
    power = [c for c in game.pellets if g.MAZE[c[0]][c[1]] == "o"]
    if power and first_step(me, power):
        return first_step(me, power)
    return first_step(me, game.pellets)


KEY_FOR = {v: k for k, v in g.KEY_DIRS.items()}


def driver():
    while "game" not in holder:
        time.sleep(0.05)
    time.sleep(1.0)  # let the window settle
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30",
         "-i", "title=Pac-Man", "-t", str(seconds),
         "-vf", f"scale=iw*2:ih*2:flags=neighbor,pad=iw:ih+36:0:36:black,"
                f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{caption}':"
                f"fontcolor=white:fontsize=22:x=10:y=7",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out])
    t0, last = time.time(), None
    seen, log = None, []
    while time.time() - t0 < seconds + 0.3:
        gm = holder["game"]
        snap = (gm.score, gm.lives, gm.fright_left > 0)
        if snap != seen:
            log.append((round(time.time() - t0, 1),) + snap)
            seen = snap
        step = pick(holder["game"])
        if step and step != last:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=KEY_FOR[step], mod=0, unicode="", scancode=0))
            last = step
        time.sleep(0.03)
    ff.wait()
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    jumps = [b[1] - a[1] for a, b in zip(log, log[1:]) if b[1] - a[1] >= 50]
    print("SUMMARY final", log[-1], "frightened_seen", any(e[3] for e in log),
          "min_lives", min(e[2] for e in log), "big_score_jumps", jumps)


threading.Thread(target=driver, daemon=True).start()
g.main()
print("done", out)
