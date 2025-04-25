from math import ceil

def modciV(red_social):
    grupos = red_social.grupos
    R_max = red_social.R_max
    n = len(grupos)
    E = [0] * n  # Estrategia vacía
    R = R_max

    pasos = 0
    decisiones = []

    while True:
        mejor_i = -1
        mejor_utilidad = 0
        for i in range(n):
            g = grupos[i]
            if E[i] < g.n:
                delta = abs(g.op1 - g.op2)
                if delta == 0:
                    continue
                esfuerzo = ceil(delta * g.rig)
                utilidad = (delta ** 2) / esfuerzo
                if esfuerzo <= R and utilidad > mejor_utilidad:
                    mejor_utilidad = utilidad
                    mejor_i = i

        if mejor_i == -1:
            break

        g = grupos[mejor_i]
        delta = abs(g.op1 - g.op2)
        esfuerzo = ceil(delta * g.rig)
        E[mejor_i] += 1
        R -= esfuerzo
        pasos += 1
        decisiones.append(f"Paso {pasos}: Grupo {mejor_i+1} → Esfuerzo {esfuerzo}")

    # calcular esfuerzo total
    esfuerzo_total = sum(
        ceil(abs(g.op1 - g.op2) * g.rig) * E[i]
        for i, g in enumerate(grupos)
    )

    # aplicar estrategia
    red_moderada = red_social.aplicar_estrategia(E)
    CI = red_moderada.calcular_conflicto_interno()

    # estadísticas opcionales
    stats = {
        "Pasos ejecutados": pasos,
        "Decisiones": "\n".join(decisiones[:5]) + ("..." if len(decisiones) > 5 else ""),
        "Grupos moderados": sum(1 for x in E if x > 0)
    }

    return E, esfuerzo_total, CI, stats