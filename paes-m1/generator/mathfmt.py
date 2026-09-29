"""Álgebra mínima de expresiones a + b√n con coeficientes racionales."""
from fractions import Fraction
from functools import reduce
from math import gcd, sqrt
from collections import namedtuple

Raw = namedtuple("Raw", "s v")  # opción ya formateada (texto, valor numérico)


def sqfree(n):
    s, t, f = 1, n, 2
    while f * f <= t:
        while t % (f * f) == 0:
            t //= f * f
            s *= f
        f += 1
    return s, t


def E(*pairs):
    """Expresión normalizada: suma de c·√n (n se reduce a libre de cuadrados)."""
    acc = {}
    for c, n in pairs:
        s, t = sqfree(n)
        acc[t] = acc.get(t, 0) + Fraction(c) * s
    return tuple((acc[n], n) for n in sorted(acc) if acc[n] != 0)


def val(e):
    return sum(float(c) * sqrt(n) for c, n in e)


def fmt(e):
    if not e:
        return "0"
    d = reduce(lambda a, b: a * b // gcd(a, b), [c.denominator for c, _ in e])
    nums = [int(c * d) for c, _ in e]
    g = reduce(gcd, [abs(x) for x in nums] + [d])
    nums = [x // g for x in nums]
    d //= g
    out = []
    for i, (x, (_, n)) in enumerate(zip(nums, e)):
        a = abs(x)
        core = (str(a) if (a != 1 or n == 1) else "") + (f"√{n}" if n > 1 else "")
        if i == 0:
            out.append(("−" if x < 0 else "") + core)
        else:
            out.append((" − " if x < 0 else " + ") + core)
    body = "".join(out)
    if d == 1:
        return body
    return f"{body}/{d}" if len(e) == 1 else f"({body})/{d}"


def rs(c, n):
    """Texto de c·√n sin normalizar (para enunciados y figuras)."""
    if n == 1:
        return str(c)
    return (str(c) if c != 1 else "") + f"√{n}"
