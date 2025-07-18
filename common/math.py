from dataclasses import dataclass


def _get_xy(other) -> tuple[int, int] | tuple[float, float]:
    if isinstance(other, Vector2):
        return other.x, other.y
    elif isinstance(other, (tuple, list)) and len(other) == 2:
        return other[0], other[1]
    elif isinstance(other, dict) and all(k in other for k in ("x", "y")):
        return other["x"], other["y"]
    elif isinstance(other, (int, float)):
        return other, other
    else:
        raise TypeError(f"Unsupported operand type: {type(other).__name__}")


@dataclass(slots=True)
class Vector2:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        x, y = _get_xy(other)
        return Vector2(int(self.x + x), int(self.y + y))

    def __iadd__(self, other):
        dx, dy = _get_xy(other)
        self.x = int(self.x + dx)
        self.y = int(self.y + dy)
        return self

    def __sub__(self, other):
        x, y = _get_xy(other)
        return Vector2(int(self.x - x), int(self.y - y))

    def __isub__(self, other):
        dx, dy = _get_xy(other)
        self.x = int(self.x - dx)
        self.y = int(self.y - dy)
        return self

    def __mul__(self, other):
        x, y = _get_xy(other)
        return Vector2(int(self.x * x), int(self.y * y))

    def __imul__(self, other):
        dx, dy = _get_xy(other)
        self.x = int(self.x * dx)
        self.y = int(self.y * dy)
        return self

    def __truediv__(self, other):
        x, y = _get_xy(other)
        return Vector2(int(self.x / x), int(self.y / y))

    def __itruediv__(self, other):
        dx, dy = _get_xy(other)
        self.x = int(self.x / dx)
        self.y = int(self.y / dy)
        return self

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __ifloordiv__(self, other):
        return self.__itruediv__(other)

    def __getitem__(self, index) -> int:
        result = None
        if index == 0:
            result = self.x
        elif index == 1:
            result = self.y
        else:
            IndexError("Vector2 only have 2 index 0 (x) or 1 (y).")

        if result is None:
            return 0
        return result


@dataclass(slots=True)
class Direction2D:
    left: int
    down: int
    right: int
    up: int

    def to_dict(self):
        return {key: getattr(self, key) for key in self.__slots__}

    def _get_delta(self, other):
        if isinstance(other, dict):
            for k in other.keys():
                if k in self.__slots__:
                    continue
                err_msg = f"Foreign key detected! '{k}' is not part of Direction2D."
                raise KeyError(err_msg)
            return other

        if isinstance(other, (Direction2D, tuple, list)):
            if isinstance(other, Direction2D):
                return self.to_dict()

            if len(other) == 4:
                return {key: other[i] for i, key in enumerate(self.__slots__)}

        x, y = _get_xy(other)
        x = int(x)
        y = int(y)
        return {"left": x, "right": x, "up": y, "down": y}

    def __iter__(self):
        for key in self.__slots__:
            yield getattr(self, key)

    def __add__(self, other):
        delta = self._get_delta(other)
        new_values = {key: getattr(self, key) + delta[key] for key in self.__slots__}
        return Direction2D(**new_values)

    def __iadd__(self, other):
        delta = self._get_delta(other)
        for key in self.__slots__:
            setattr(self, key, getattr(self, key) + delta[key])
        return self

    def __sub__(self, other):
        delta = self._get_delta(other)
        new_values = {key: getattr(self, key) - delta[key] for key in self.__slots__}
        return Direction2D(**new_values)

    def __isub__(self, other):
        delta = self._get_delta(other)
        for key in self.__slots__:
            setattr(self, key, getattr(self, key) - delta[key])
        return self

    def __mul__(self, other: "Vector2"):
        delta = self._get_delta(other)
        new_values = {key: getattr(self, key) * delta[key] for key in self.__slots__}
        return Direction2D(**new_values)

    def __imul__(self, other):
        delta = self._get_delta(other)
        for key in self.__slots__:
            setattr(self, key, getattr(self, key) * delta[key])
        return self

    def __truediv__(self, other):
        delta = self._get_delta(other)
        new_values = {key: getattr(self, key) // delta[key] for key in self.__slots__}
        return Direction2D(**new_values)

    def __itruediv__(self, other):
        delta = self._get_delta(other)
        for key in self.__slots__:
            setattr(self, key, getattr(self, key) // delta[key])
        return self

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __ifloordiv__(self, other):
        return self.__itruediv__(other)
