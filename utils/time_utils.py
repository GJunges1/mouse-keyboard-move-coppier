from types import SimpleNamespace
from threading import Lock


def save_snapshot(
    timeline: list, shared: SimpleNamespace, lock: Lock, sleeptime: float
):
    cache = shared.cache
    with lock:
        if cache:
            found_move = False
        for index, event in reversed(list(enumerate(cache))):
            if event["type"] == "move":
                if not found_move:
                    found_move = True
                else:
                    del cache[index]
        timeline.extend(cache)
        timeline.append({"type": "timemark", "timedelta": sleeptime})
        shared.cache = []
