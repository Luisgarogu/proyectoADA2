# Algoritmo voraz
def modciV(red_social):
    SAG, R_max = red_social
    n = len(SAG)
    E = [0] * n  # Estrategia vacía
    R = R_max

    while True:
        mejor_i = -1
        mejor_utilidad = 0
        for i in range(n):
            ni, o1, o2, r = SAG[i]
            if E[i] < ni:
                delta = abs(o1 - o2)
                if delta == 0:
                    continue
                esfuerzo = ceil(delta * r)
                utilidad = (delta ** 2) / esfuerzo
                if esfuerzo <= R and utilidad > mejor_utilidad:
                    mejor_utilidad = utilidad
                    mejor_i = i

        if mejor_i == -1:
            break

        ni, o1, o2, r = SAG[mejor_i]
        delta = abs(o1 - o2)
        esfuerzo = ceil(delta * r)
        E[mejor_i] += 1
        R -= esfuerzo

    esfuerzo_total = sum(
        ceil(abs(o1 - o2) * r) * E[i]
        for i, (ni, o1, o2, r) in enumerate(SAG)
    )

    CI = sum(
        (ni - E[i]) * (o1 - o2) ** 2
        for i, (ni, o1, o2, r) in enumerate(SAG)
    ) / n

    return E, esfuerzo_total, CI