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


def get_point(index):
    """Возвращает точку по индексу (x, y) или (None, None) если индекс некорректен"""
    if 0 <= index < len(_state["x"]):
        return _state["x"][index], _state["y"][index]
    return None, None


def get_points():
    """Возвращает список всех валидных точек (x, y) где оба значения не None"""
    points = []
    for x, y in zip(_state["x"], _state["y"]):
        if x is not None and y is not None:
            points.append((x, y))
    return points


def find_nearest(x_click, y_click):
    """Находит индекс ближайшего узла по евклидову расстоянию"""
    min_dist_sq = float('inf')
    min_idx = -1

    for i in range(len(_state["x"])):
        if _state["x"][i] is None or _state["y"][i] is None:
            continue

        dx = _state["x"][i] - x_click
        dy = _state["y"][i] - y_click
        dist_sq = dx * dx + dy * dy

        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            min_idx = i

    if min_idx != -1:
        return min_idx, min_dist_sq ** 0.5
    return -1, float('inf')


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