import math

def modciPD(red_social):
    grupos = red_social.grupos
    R_max = red_social.R_max
    n = len(grupos)
    INF = float('inf')

    # dp[i][r] = conflicto mínimo usando primeros i grupos y r esfuerzo
    dp = [[INF] * (R_max + 1) for _ in range(n + 1)]
    decision = [[-1] * (R_max + 1) for _ in range(n + 1)]

    dp[0][0] = 0  # Base: 0 grupos, 0 esfuerzo → 0 conflicto

    for i in range(1, n + 1):
        grupo = grupos[i - 1]
        cantidad = grupo.n
        diff = grupo.op1 - grupo.op2
        conflicto_agente = diff ** 2

        for r in range(R_max + 1):
            for m in range(cantidad + 1):  # m agentes moderados
                esfuerzo = math.ceil(abs(diff) * grupo.rig * m)
                if r >= esfuerzo and dp[i - 1][r - esfuerzo] != INF:
                    conflicto_restante = (cantidad - m) * conflicto_agente
                    total_conflicto = dp[i - 1][r - esfuerzo] + conflicto_restante

                    if total_conflicto < dp[i][r]:
                        dp[i][r] = total_conflicto
                        decision[i][r] = m

    # Buscar mejor solución
    mejor_conflicto_total = min(dp[n])
    mejor_r = dp[n].index(mejor_conflicto_total)

    # Reconstruir estrategia
    estrategia = [0] * n
    r = mejor_r
    for i in range(n, 0, -1):
        m = decision[i][r]
        estrategia[i - 1] = m
        grupo = grupos[i - 1]
        esfuerzo = math.ceil(abs(grupo.op1 - grupo.op2) * grupo.rig * m)
        r -= esfuerzo

    #Dividir entre n grupos para obtener el conflicto interno
    conflicto_final = mejor_conflicto_total / n
    esfuerzo_total = mejor_r

    #Estadisticas
    stats = {
        "Grupos moderados": sum(1 for e in estrategia if e > 0),
        "Moderaciones totales": sum(estrategia),
        #"Esfuerzo restante": R_max - esfuerzo_total
    }

    return estrategia, esfuerzo_total, conflicto_final, stats