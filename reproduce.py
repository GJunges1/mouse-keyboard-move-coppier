import pyautogui as pg
import json
from os.path import join as pjoin
from sys import path
import os, sys

lastx = None
lasty = None
with open(pjoin(path[0], "cache.json"), "r", encoding="utf-8") as fp:
    cache = json.load(fp)

for event_type, details in cache:
    if event_type == "m":
        x, y = details
        if lastx == None:
            lastx = x
        if lasty == None:
            lasty = y
        if abs(lasty - y) > 10 or abs(lastx - x) > 10:
            lasty = y
            lastx = x
            pg.moveTo(x, y)
    elif event_type == "c":
        variation, x, y = details
        if variation == "p":
            pg.mouseDown(x, y, duration=0.1)
        elif variation == "r":
            pg.mouseUp(x, y, duration=0.1)
    elif event_type == "s":
        x, y, dy = details
        pg.scroll(100 * dy, x, y)
    elif event_type == "k":
        keys = details
        if keys == "ctrl_l":
            print("entrou")
            keys = "leftcontrol"
        if keys == "shift_l":
            print("entrou")
            keys = "leftshift"
        pg.press(keys)
