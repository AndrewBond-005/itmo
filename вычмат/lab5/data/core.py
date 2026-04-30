_state = {"x": [], "y": []}
_callbacks = []
_auto_update = True
_silent = False  # флаг тихого режима

# Вычисленные точки
_compute_x = None
_computed_values = {}  # {"lagrange": y, "newton_div": y, "newton_fin": y}


def subscribe(callback):
    if callback not in _callbacks:
        _callbacks.append(callback)


def notify():
    if not _silent:  # не уведомляем в тихом режиме
        for callback in _callbacks:
            callback()


def begin_silent():
    """Начинаем массовые изменения (без уведомлений)"""
    global _silent
    _silent = True


def end_silent():
    """Заканчиваем массовые изменения и обновляем один раз"""
    global _silent
    _silent = False
    notify()


def get_auto_update():
    return _auto_update


def set_auto_update(value):
    global _auto_update
    _auto_update = value
    notify()


def get_x():
    return _state["x"].copy()


def get_y():
    return _state["y"].copy()


def get_point(index):
    if 0 <= index < len(_state["x"]):
        return _state["x"][index], _state["y"][index]
    return None, None


def get_points():
    points = []
    for x, y in zip(_state["x"], _state["y"]):
        if x is not None and y is not None:
            points.append((x, y))
    return points


def find_nearest(x_click, y_click):
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
    clear_computed_points()
    if not _silent:
        notify()


def delete_point(index):
    if 0 <= index < len(_state["x"]):
        del _state["x"][index]
        del _state["y"][index]
        clear_computed_points()
        notify()


def update_x(index, x):
    if 0 <= index < len(_state["x"]):
        _state["x"][index] = x
        clear_computed_points()
        notify()


def update_y(index, y):
    if 0 <= index < len(_state["y"]):
        _state["y"][index] = y
        clear_computed_points()
        notify()


def clear_all():
    _state["x"].clear()
    _state["y"].clear()
    clear_computed_points()
    if not _silent:
        notify()


def set_points(points):
    """Быстрая замена всех точек - одно уведомление"""
    global _state
    begin_silent()
    _state["x"] = [p[0] for p in points]
    _state["y"] = [p[1] for p in points]
    clear_computed_points()
    end_silent()


# Новые функции для вычисленных точек
def set_computed_points(x, values):
    global _compute_x, _computed_values
    _compute_x = x
    _computed_values = values.copy()
    notify()


def get_compute_x():
    return _compute_x


def get_computed_values():
    return _computed_values.copy()


def clear_computed_points():
    global _compute_x, _computed_values
    _compute_x = None
    _computed_values = {}