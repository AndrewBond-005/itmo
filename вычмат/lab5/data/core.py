from utils.const import DEFAULT_ROWS

_state = {"x": [], "y": []}
_callbacks = []

def subscribe(callback):
    if callback not in _callbacks:
        _callbacks.append(callback)

def notify():
    for callback in _callbacks:
        callback()

def get_x():
    return _state["x"].copy()

def get_y():
    return _state["y"].copy()

def add_point(x=None, y=None):
    _state["x"].append(x)
    _state["y"].append(y)
    notify()

def delete_point(index):
    if 0 <= index < len(_state["x"]):
        del _state["x"][index]
        del _state["y"][index]
        notify()

def update_x(index, x):
    if 0 <= index < len(_state["x"]):
        _state["x"][index] = x
        notify()

def update_y(index, y):
    if 0 <= index < len(_state["y"]):
        _state["y"][index] = y
        notify()

def clear_all():
    _state["x"].clear()
    _state["y"].clear()
    notify()