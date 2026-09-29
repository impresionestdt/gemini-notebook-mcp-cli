"""Construcción de preguntas y bancos con la regla de longitud de alternativas."""
import random
from mathfmt import Raw, fmt, val

SKILLS = ["Resolver problemas", "Modelar", "Representar", "Argumentar"]  # las 4 habilidades PAES M2
LEGACY_PRO = "Aplicar procedimientos"  # ya no es una habilidad: sus plantillas pasan a «Resolver problemas»
MAX_GAP = 16  # correcta - distractor más largo <= 16 caracteres


class Reject(Exception):
    """La pregunta generada no cumple las reglas: se descarta y se vuelve a generar."""


def check_lengths(correct, dists):
    return len(correct) - max(len(d) for d in dists) <= MAX_GAP


def distinct(correct_e, cands, k=4):
    """Elige k distractores con texto y valor distintos de la correcta y entre sí."""
    cs, cv = (correct_e.s, correct_e.v) if isinstance(correct_e, Raw) else (fmt(correct_e), val(correct_e))
    seen, vals, out = {cs}, [cv], []
    for c in cands:
        s, v = (c.s, c.v) if isinstance(c, Raw) else (fmt(c), val(c))
        if s in seen or any(abs(v - x) < 1e-9 for x in vals):
            continue
        seen.add(s); vals.append(v); out.append(s)
        if len(out) == k:
            return out
    raise Reject("faltan distractores")


def make(stem, svg, correct, dists, skill, expl):
    if len(dists) != 4 or len(set(dists + [correct])) != 5:
        raise Reject("opciones repetidas")
    if not check_lengths(correct, dists):
        raise Reject("regla de longitud")
    return {"q": stem, "svg": svg, "o": [correct] + dists, "s": skill, "e": expl}


def norm(by_skill):
    """Unifica las plantillas al esquema de 4 habilidades (los procedimientos se evalúan como resolución de problemas)."""
    by = {k: list(v) for k, v in by_skill.items() if k != LEGACY_PRO}
    for f in by_skill.get(LEGACY_PRO, []):
        if f not in by.setdefault(SKILLS[0], []):
            by[SKILLS[0]].append(f)
    return by


def gen_bank(by_skill, lvl, size, seed):
    rng = random.Random(seed)
    by_skill = norm(by_skill)
    base, extra = divmod(size, len(SKILLS))
    quotas = {s: base + (1 if i < extra else 0) for i, s in enumerate(SKILLS)}
    bank, seen = [], set()
    for skill, fs in by_skill.items():
        quota = quotas[skill]
        cnt = att = 0
        while cnt < quota and att < 40000:
            f = fs[att % len(fs)]
            att += 1
            try:
                q = f(rng, lvl)
            except Reject:
                continue
            q["s"] = skill
            key = (q["q"], tuple(sorted(q["o"])), q["svg"])
            if key in seen:
                continue
            seen.add(key); bank.append(q); cnt += 1
        if cnt < quota:
            raise RuntimeError(f"{skill}: solo {cnt}/{quota} preguntas únicas")
    rng.shuffle(bank)
    return bank
