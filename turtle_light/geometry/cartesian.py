import math
import numbers

DEFAULT_EPSILON = 1e-6


class Vector:
    # init
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # attrs
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def position(self):
        return self.x, self.y

    @property
    def slope(self):
        if self.x == 0:
            return None
        return self.y / self.x

    # opers
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def s_mul(self, other):
        return Vector(self.x * other, self.y * other)

    def d_mul(self, other):
        return self.x * other.x + self.y * other.y

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return self.s_mul(other)
        if isinstance(other, Vector):
            return self.d_mul(other)

    def __rmul__(self, other):
        return self.s_mul(other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __matmul__(self, other):
        return self.x * other.y - other.x * self.y

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def same(self, other, eps=DEFAULT_EPSILON):
        return -eps <= self.x - other.x <= eps and -eps <= self.y - other.y <= eps

    def __eq__(self, other):
        return self.same(other)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def vertical(self, other, eps=DEFAULT_EPSILON):
        return -eps <= self * other <= eps

    def __mod__(self, other):  # vertical
        return self.vertical(other)

    def parallel(self, other, eps=DEFAULT_EPSILON):
        return -eps <= self @ other <= eps

    def __floordiv__(self, other):  # parallel
        return self.parallel(other)

    def angle(self, other=None):
        if other is None:
            other = Vector(1, 0)
        if self @ other > 0:
            return math.acos(self * other / abs(self) / abs(other))
        elif self @ other < 0:
            return -math.acos(self * other / abs(self) / abs(other))
        else:
            return 0

    def __xor__(self, other):
        return self.angle(other)

    # transform
    def move(self, d):
        return self + d

    def rotate(self, angle):
        return Vector(
            self.x * math.cos(angle) + self.y * math.sin(angle),
            self.y * math.cos(angle) - self.x * math.sin(angle),
        )

    def revolve(self, angle, point=None):
        if point is None:
            point = Vector(0, 0)
        axis = self - point
        return point + axis.rotate(angle)

    def project(self, wall):
        return (self * wall * wall) / (wall.x**2 + wall.y**2)

    def __rshift__(self, other):
        return self.project(other)

    def normal(self):
        return Vector(-self.y, self.x)

    def __invert__(self):
        return self.normal()

    def central_symm(self, point):
        return 2 * point - self

    def axial_symm(self, axis):
        return self.central_symm(self.project(axis))

    # format
    def __repr__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)


ZERO_VECTOR = Vector(0, 0)


class Line:
    # init
    def __init__(self, begin, direct):
        self.__begin = begin
        self.__direct = direct

    # attrs
    @property
    def begin(self):
        return self.__begin

    @property
    def direct(self):
        return self.__direct

    @property
    def end(self):
        return self.begin + self.direct

    # equation
    @property
    def A(self):
        return self.direct.y

    @property
    def B(self):
        return -self.direct.x

    @property
    def C(self):
        return self.direct @ self.begin

    @property
    def equation(self):
        return self.A, self.B, self.C

    # opers
    def vertical(self, other, eps=DEFAULT_EPSILON):
        return self.direct.vertical(other.direct, eps)

    def __mod__(self, other):  # vertical
        return self.vertical(other)

    def parallel(self, other, eps=DEFAULT_EPSILON):
        return self.direct.parallel(other.direct, eps)

    def __floordiv__(self, other):
        return self.parallel(other)

    def same(self, other, eps=DEFAULT_EPSILON):
        return self.parallel(other, eps) and self.direct.parallel(
            other.begin - self.begin, eps
        )

    def __eq__(self, other):
        return self.same(other)

    def intersect(self, other, eps=DEFAULT_EPSILON):
        if self.parallel(other, eps):
            return None
        ix = (other.C * self.B - self.C * other.B) / (
            self.A * other.B - other.A * self.B
        )
        iy = (self.C * other.A - other.C * self.A) / (
            self.A * other.B - other.A * self.B
        )
        return Vector(ix, iy)

    def __or__(self, other):
        return self.intersect(other)

    def p_collide(self, other, eps=DEFAULT_EPSILON):
        eqrt = self.A * other.x + self.B * other.y + self.C
        return -eps <= eqrt <= eps

    def l_collide(self, other, eps=DEFAULT_EPSILON):
        ip = self.intersect(other, eps)
        if ip is None:
            return False
        return self.p_collide(ip, eps) and other.p_collide(ip, eps)

    def __contains__(self, other):
        if isinstance(other, Vector):
            return self.p_collide(other)
        if isinstance(other, Line):
            return self.l_collide(other)

    def __and__(self, other):
        if other not in self:
            return None
        return self | other

    def angle(self, other):
        return self.direct ^ other.direct

    def __xor__(self, other):
        return self.angle(other)

    # transform
    def move(self, d):
        return Line(self.begin + d, self.direct)

    def rotate(self, angle):
        return Line(self.begin.rotate(angle), self.direct.rotate(angle))

    def revolve(self, angle, point=None):
        return Line(self.begin.revolve(angle, point), self.direct.rotate(angle))

    def normal(self, point=None):
        if point is None:
            point = Vector(0, 0)
        return Line(point, ~self.direct)

    def central_symm(self, point):
        return Line(self.begin.axial_symm(point), self.direct)

    def axial_symm(self, axis):
        return Line(self | axis, self.direct.axial_symm(axis.direct))

    # format
    def __repr__(self):
        return "{A}x+{B}y+{C}=0".format(A=self.A, B=self.B, C=self.C)


class Ray(Line):
    def p_collide(self, other, eps=DEFAULT_EPSILON):
        if super().p_collide(other, eps):
            p_dir = other - self.begin
            return p_dir.x * self.direct.x >= -eps and p_dir.y * self.direct.y >= -eps
        return False


class Curve(Line):
    def p_collide(self, other, eps=DEFAULT_EPSILON):
        if super().p_collide(other, eps):
            p_dir = other - self.begin
            return abs(p_dir) - abs(self.direct) <= eps
        return False


class Dot(Vector):
    pass


class TDLine(Line):
    def __init__(self, begin, end):
        super().__init__(begin, end - begin)


class EQLine(Line):
    def __init__(self, a, b, c):
        if b == 0:
            super().__init__(-c / a, 0)
        else:
            super().__init__(Vector(0, -c / b), Vector(-b, a))


class TDRay(Ray):
    def __init__(self, begin, end):
        super().__init__(begin, end - begin)


class TDCurve(Curve):
    def __init__(self, begin, end):
        super().__init__(begin, end - begin)
