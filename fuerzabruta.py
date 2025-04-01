def modciFB(RS):
    grupos, R_max = RS
    n = len(grupos)
    mejor_E = None
    mejor_costo = None
    mejor_CI = float('inf')
    solucion_actual = [0]*n
    
    def backtrack(i, costo_acumulado):
        nonlocal mejor_E, mejor_costo, mejor_CI
        # Si el costo acumulado ya excede el presupuesto, poda la búsqueda.
        if costo_acumulado > R_max:
            return
        # decisiones a todos los grupos:
        if i == n:
            # Calcular el conflicto interno resultante de la estrategia actual
            conflicto_sum = 0
            for idx, (n_i, o1, o2, r) in enumerate(grupos):
                d = o1 - o2
                # (n_i - e_i) agentes quedan sin moderar en ese grupo, aportan conflicto
                conflicto_sum += (n_i - solucion_actual[idx]) * (d**2)
            CI = conflicto_sum / n  # promedio sobre n grupos
            if CI < mejor_CI:
                mejor_CI = CI
                mejor_E = solucion_actual.copy()
                mejor_costo = costo_acumulado
            return
        # Caso contrario, intentar todas las posibilidades para el grupo i
        n_i, o1, o2, r = grupos[i]
        d = abs(o1 - o2)
        for e in range(0, n_i+1):
            # costo de moderar e agentes en el grupo i
            costo_e = math.ceil(d * r * e)
            solucion_actual[i] = e
            backtrack(i+1, costo_acumulado + costo_e)
        # restaurar estado (no estrictamente necesario al reescribir e en siguiente iteración)
        solucion_actual[i] = 0
    
    backtrack(0, 0)
    return mejor_E, mejor_costo, mejor_CI
