from functools import partial
import json
import os
import sys
import time
from timeit import timeit
from types import SimpleNamespace
from listeners.keyboard_listener import KeyboardListener
from threading import Lock
from listeners.mouse_listener import MouseListener

from utils.time_utils import save_snapshot


shared = SimpleNamespace(cache=[])
flags = SimpleNamespace(should_stop=False)
lock = Lock()


# # ...or, in a non-blocking fashion:
mouse_listener = MouseListener(shared, lock)
mouse_listener.start()

# Collect events until released
keyboard_listener = KeyboardListener(shared, flags, mouse_listener.listener, lock)
keyboard_listener.start()

# ...or, in a non-blocking fashion:
# keyboard_listener = keyboard.Listener(
#     on_press=partial(on_press, cache, mouse_listener),
#     on_release=partial(on_release, cache, mouse_listener),
# )
# keyboard_listener.start()

timeline = []
SLEEPTIME = 1 / 16  # of a second
while not flags.should_stop:
    time.sleep(SLEEPTIME)
    save_snapshot(timeline, shared, lock, SLEEPTIME)

with open(os.path.join(sys.path[0], "cache.json"), "w", encoding="utf-8") as fp:
    json.dump(timeline, fp, indent=2, ensure_ascii=False)
print("file written to cache.json")
