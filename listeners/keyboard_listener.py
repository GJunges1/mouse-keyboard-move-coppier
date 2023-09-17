from functools import partial
from threading import Lock
from pynput import keyboard

UPPERCASES = set("ABCDEFGHIJKLMNOPQRSTUVWXYZÇ")


def on_press(cache, mouse_listener, lock: Lock, key):
    del mouse_listener, lock
    try:
        print("alphanumeric key {0} pressed".format(key.char))
        cache.append(("k", key.char))
    except AttributeError:
        if key != keyboard.Key.esc:
            cache.append(("k", key.name))
            print("special key {0} pressed".format(key))


def on_release(cache, mouse_listener, lock: Lock, key):
    del lock, cache
    print("{0} released".format(key))
    if key == keyboard.Key.esc:
        mouse_listener.stop()
        # Stop listener
        return False


class KeyboardListener:

    def __init__(self, cache, mouse_listener, lock):
        self.mouse_listener = mouse_listener
        self.cache = cache
        self.lock = lock

    def start(self):
        cache = self.cache
        mouse_listener = self.mouse_listener

        with keyboard.Listener(
            on_press=partial(on_press, cache, mouse_listener, self.lock),
            on_release=partial(on_release, cache, mouse_listener, self.lock),
        ) as listener:
            listener.join()
