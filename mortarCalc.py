#!/bin/env python

import sys
import math


class Point():
    _subdivisions = 3
    _kp_size = 9

    def __init__(self, p: str):
        parts = p.split('-')
        if len(parts) != 3:
            raise ValueError("Malformed coordinates. Should be: A1-2-3")

        # Parse the first part of the coordinate
        self.x: float = ord(parts[0][0]) - 65
        self.y: float = int(parts[0][1])

        cur_res = 10
        for p in parts[1:]:
            # Parse the second part of the coordinate
            second = 0
            try:
                second = int(parts[1])
            except ValueError as v:
                raise v
            finally:
                x, y = self._calc_subgrid(second, cur_res)
                self.x += x
                self.y += y
                cur_res *= 10

    def _calc_subgrid(self, v: int, res: int):
        row = math.ceil(self._invert_value(v) / self._subdivisions) - 1
        v -= 1
        col = v - (int(v / self._subdivisions) * self._subdivisions)

        y = row * (self._subdivisions / res)
        x = col * (self._subdivisions / res)

        return x, y

    def _invert_value(self, v: int):
        if 1 <= v <= self._kp_size:
            return self._kp_size + 1 - v
        else:
            raise ValueError("Number is out of bounds (1 to limit)")

    def __str__(self):
        return "%.2f, %.2f" % (self.x, self.y)


def calculate_mortar_data(p1: Point, p2: Point, scale: int):
    distance = math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2)) * scale
    angle = math.degrees(math.atan2(p2.y - p1.y, p2.x - p1.x)) + 90
    return distance, angle


if __name__ == "__main__":
    print("=== Mortar Calculator ===")

    # Point 1, Point 2, GridSize
    #                   ^^^^^^^^ usually 33
    if len(sys.argv) != 4:
        print("2 Arguments are required")
        sys.exit(1)

    try:
        p1 = Point(sys.argv[1])
    except ValueError as v:
        print(v)
        sys.exit(1)

    try:
        p2 = Point(sys.argv[2])
    except ValueError as v:
        print(v)
        sys.exit(1)

    print(p1)
    print(p2)
    print(calculate_mortar_data(p1, p2, int(sys.argv[3])))
