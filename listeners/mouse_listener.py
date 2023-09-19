from functools import partial
from threading import Lock
from pynput import mouse


def on_move(shared, lock: Lock, x, y):
    cache = shared.cache
    print(f"Pointer moved to {(x,y)}")
    with lock:
        cache.append({"type": "move", "details": (x, y)})


def on_click(shared, lock: Lock, x, y, button, pressed):
    cache = shared.cache
    if button == mouse.Button.left:
        if pressed:
            print("{0} at {1}".format("Pressed", (x, y)))
            with lock:
                cache.append({"type": "click press", "details": (x, y)})
        else:
            with lock:
                cache.append({"type": "click release", "details": (x, y)})


def on_scroll(shared, lock: Lock, x, y, dx, dy):
    cache = shared.cache
    print("Scrolled {0} at {1}".format("down" if dy < 0 else "up", (x, y)))
    with lock:
        cache.append({"type": "scroll", "details": (x, y, dy)})


class MouseListener:

    def __init__(self, shared, lock):
        self.listener = mouse.Listener(
            on_move=partial(on_move, shared, lock),
            on_click=partial(on_click, shared, lock),
            on_scroll=partial(on_scroll, shared, lock),
        )

    def start(self):
        self.listener.start()
