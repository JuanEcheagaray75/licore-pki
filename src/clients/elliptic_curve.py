from itertools import product
from typing import Tuple

curve_point = Tuple[int, int]

INF: curve_point = None

class EllipticCurve:

    def __init__(self, a, b, p):

        self.a = a
        self.b = b
        self.p = p
        self.points = []

    def generate_points(self) -> None:

        self.field_elements = [i for i in range(self.p)]
        self.points.append(INF)
        pos_pairs = product(self.field_elements, self.field_elements)
        self.points.extend([(x, y)
                            for (x, y) in pos_pairs
                            if self.test_element(x, y)])

    def add(self, p1: curve_point, p2: curve_point) -> curve_point:

        if p1 is INF:
            return p2
        elif p2 is INF:
            return p1

        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]

        if not self.eq(x1, x2):
            m = (y2 - y1)*pow(x2 - x1,-1, self.p)
            x3 = (m**2 - x1 - x2) % self.p
            y3 = (m*(x1 - x3) - y1) % self.p

            return (x3, y3)

        elif (self.eq(x1, x2)) and (not self.eq(y1, y2)):
            return INF

        elif (p1 == p2) and not self.eq(y1, 0):
            m = (3*x1**2 + self.a)*pow(2*y1,-1,self.p) % self.p
            x3 = (m**2 - 2*x1) % self.p
            y3 = (m*(x1 - x3) - y1) % self.p

            return (x3, y3)

        elif (p1 == p2) and y1 == 0:
            return INF
        else:
            raise ValueError("Uncovered")

    def inv(self, p1: curve_point) -> curve_point:
        x1 = p1[0]
        y1 = p1[1]

        return (x1, -y1 % self.p)

    # MAGIC
    def mul(self, n: int, p1: curve_point) -> curve_point:
        result = INF
        to_add = p1
        for b in self.bits(n):
            if b:
                result = self.add(result, to_add)
            to_add = self.add(to_add, to_add)

        return result

    def eq(self, x: int, y: int) -> bool:
        return (x - y) % self.p == 0

    def order(self) -> int:
        return len(self.points)

    def test_element(self, x: int, y: int) -> bool:
        return (x**3 + self.a*x + self.b - y**2) % self.p == 0

    def det(self) -> int:
        return (-4*self.a**3 - 27*self.b**2) % self.p

    # MAGIC
    def bits(self, n):
        while n:
            yield n & 1
            n >>= 1
