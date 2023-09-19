from time import sleep
import pyautogui as pg
import json
from os.path import join as pjoin
from sys import path
from timeit import default_timer as timer

with open(pjoin(path[0], "cache.json"), "r", encoding="utf-8") as fp:
    cache = json.load(fp)

start = timer()
elapsed = 0
pg.FAILSAFE = False
for event in cache:
    if event["type"] == "timemark":
        elapsed = timer() - start
        time = event["timedelta"]

        if time > elapsed:
            sleep(time - elapsed)

        start = timer()
    else:
        if event["type"] == "move":
            x, y = event["details"]
            pg.moveTo(x, y)
        elif event["type"] == "click press":
            x, y = event["details"]
            pg.mouseDown(x, y)
        elif event["type"] == "click release":
            pg.mouseUp(x, y)
        elif event["type"] == "scroll":
            x, y, dy = event["details"]
            pg.scroll(dy * 100, x, y)
        elif event["type"] == "keyboard":
            key = event["details"]
            pg.press(key)
