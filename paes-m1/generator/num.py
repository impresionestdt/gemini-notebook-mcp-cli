"""Formato de números para M1: decimales con coma, periódicos y mixtos."""
from fractions import Fraction as F


def dstr(x, nd=None):
    """Decimal finito con coma. nd fuerza cantidad de decimales."""
    x = F(x)
    neg = x < 0
    x = abs(x)
    if nd is None:
        nd = 0
        while (x * 10 ** nd).denominator != 1:
            nd += 1
            if nd > 8:
                raise ValueError("no terminante")
    n = x * 10 ** nd
    n = int(n + F(1, 2)) if nd is not None and (x * 10 ** nd).denominator != 1 else int(n)
    s = str(n).rjust(nd + 1, "0")
    out = s[:-nd] + "," + s[-nd:] if nd else s
    return ("−" if neg else "") + out


def terminates(x):
    d = F(x).denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def pstr(x, reps=3):
    """Expansión decimal con período visible: 1/6 → 0,1666…"""
    x = F(x)
    neg = x < 0
    x = abs(x)
    ent = int(x)
    rem = x - ent
    if rem == 0:
        return ("−" if neg else "") + str(ent)
    digs, seen, r = [], {}, rem
    while r and r not in seen:
        seen[r] = len(digs)
        r *= 10
        d = int(r)
        digs.append(str(d))
        r -= d
    if not r:
        return ("−" if neg else "") + str(ent) + "," + "".join(digs)
    pre = "".join(digs[:seen[r]])
    per = "".join(digs[seen[r]:])
    return ("−" if neg else "") + str(ent) + "," + pre + per * reps + "…"
