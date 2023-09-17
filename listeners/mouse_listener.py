from functools import partial
from threading import Lock
from pynput import mouse


def on_move(cache, lock: Lock, x, y):
    print(f"Pointer moved to {(x,y)}")
    cache.append(("m", (x, y)))


def on_click(cache, lock: Lock, x, y, button, pressed):
    if button == mouse.Button.left:
        if pressed:
            print("{0} at {1}".format("Pressed", (x, y)))
            cache.append(("c", ("p", x, y)))
        else:
            cache.append(("c", ("r", x, y)))


def on_scroll(cache, lock: Lock, x, y, dx, dy):
    print("Scrolled {0} at {1}".format("down" if dy < 0 else "up", (x, y)))
    cache.append(("s", (x, y, dy)))


class MouseListener:

    def __init__(self, cache, lock):
        self.listener = mouse.Listener(
            on_move=partial(on_move, cache, lock),
            on_click=partial(on_click, cache, lock),
            on_scroll=partial(on_scroll, cache, lock),
        )

    def start(self):
        self.listener.start()
