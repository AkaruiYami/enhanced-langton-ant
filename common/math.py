from dataclasses import dataclass


@dataclass
class Vector2:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        x, y = self._get_xy(other)
        return Vector2(int(self.x + x), int(self.y + y))

    def __iadd__(self, other):
        dx, dy = self._get_xy(other)
        self.x = int(self.x + dx)
        self.y = int(self.y + dy)
        return self

    def __sub__(self, other):
        x, y = self._get_xy(other)
        return Vector2(int(self.x - x), int(self.y - y))

    def __isub__(self, other):
        dx, dy = self._get_xy(other)
        self.x = int(self.x - dx)
        self.y = int(self.y - dy)
        return self

    def __mul__(self, other: "Vector2"):
        x, y = self._get_xy(other)
        return Vector2(int(self.x * x), int(self.y * y))

    def __imul__(self, other):
        dx, dy = self._get_xy(other)
        self.x = int(self.x * dx)
        self.y = int(self.y * dy)
        return self

    def __truediv__(self, other):
        x, y = self._get_xy(other)
        return Vector2(int(self.x / x), int(self.y / y))

    def __itruediv__(self, other):
        dx, dy = self._get_xy(other)
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

    def _get_xy(self, other) -> tuple[int, int] | tuple[float, float]:
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
