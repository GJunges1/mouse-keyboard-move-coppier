from functools import partial
from threading import Lock
from pynput import keyboard

UPPERCASES = set("ABCDEFGHIJKLMNOPQRSTUVWXYZÇ")


def on_press(shared, lock: Lock, key):
    cache = shared.cache
    try:
        print("alphanumeric key {0} pressed".format(key.char))
        with lock:
            cache.append({"type": "key press", "details": key.char})
    except AttributeError:
        if key != keyboard.Key.esc:
            with lock:
                cache.append({"type": "key press", "details": key.name})
            print("special key {0} pressed".format(key))


def on_release(flags, mouse_listener, key):
    print("{0} released".format(key))
    if key == keyboard.Key.esc:
        mouse_listener.stop()
        flags.should_stop = True
        print("end of capture")
        # Stop listener
        return False


class KeyboardListener:

    def __init__(self, shared, flags, mouse_listener, lock):
        self.mouse_listener = mouse_listener
        self.shared = shared
        self.flags = flags
        self.lock = lock

    def start(self):
        listener = keyboard.Listener(
            on_press=partial(on_press, self.shared, self.lock),
            on_release=partial(on_release, self.flags, self.mouse_listener),
        )
        listener.start()
