import json
import os
import sys
from listeners.keyboard_listener import KeyboardListener
from threading import Lock
from listeners.mouse_listener import MouseListener


cache = []
lock = Lock


# # ...or, in a non-blocking fashion:
mouse_listener = MouseListener(cache, lock)
mouse_listener.start()

# Collect events until released
keyboard_listener = KeyboardListener(cache, mouse_listener.listener, lock)
keyboard_listener.start()

# ...or, in a non-blocking fashion:
# keyboard_listener = keyboard.Listener(
#     on_press=partial(on_press, cache, mouse_listener),
#     on_release=partial(on_release, cache, mouse_listener),
# )
# keyboard_listener.start()

with open(os.path.join(sys.path[0], "cache.json"), "w", encoding="utf-8") as fp:
    json.dump(cache, fp, indent=2, ensure_ascii=False)
print("file written to cache.json")
