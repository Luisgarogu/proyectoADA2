# fuerzaBruta.py
# ---------------------------------------------------------------
# Algoritmo de búsqueda exhaustiva (fuerza bruta) para el problema ModCI
#
# Autor:  <Tu nombre>
# Fecha:  2025‑04‑21
#
# ---------------------------------------------------------------
"""
posibles <e0, …, en‑1> y escoge la que:
  1. Cumple Esfuerzo ≤ R_max, y
  2. Minimiza el conflicto interno resultante
     (si hay empate, la de menor esfuerzo).

* Complejidad temporal   :  Θ(n_i (n_i+1))  ≈  Θ(2^N)   (N = total de agentes)
* Complejidad de memoria :  Θ(n)    (la estrategia actual + mejor hallada)

"""
import math
from typing import List, Tuple, Dict, Any


def modciFB(red_social) -> Tuple[List[int], int, float, Dict[str, Any]]:
    """
    FUERZA BRUTA
    ------------
    Parámetro
    ---------
    red_social : RedSocial
        Objeto que contiene los grupos y R_max.

    Retorna
    -------
    (
        estrategia_opt : List[int],   # agentes moderados por grupo
        esfuerzo_opt   : int,
        CI_opt         : float,
        stats          : dict         # métricas adicionales
    )
    """
    n = len(red_social.grupos)

    # ---- variables de la mejor solución ----
    mejor_estrategia = [0] * n
    mejor_conflicto = red_social.calcular_conflicto_interno()
    mejor_esfuerzo = 0

    # ---- estadísticas de búsqueda ----
    nodos_visitados = 0          # llamadas recursivas totales
    hojas_factibles = 0          # estrategias válidas (esfuerzo ≤ R_max)
    combinaciones_podadas = 0    # ramas descartadas por superar R_max

    # -----------------------------------------------------------
    def backtrack(indice: int,
                  estrategia_act: List[int],
                  esfuerzo_act: int):
        """
        Recorre todas las combinaciones posibles asignando en
        `estrategia_act[indice]` los valores 0..n_i y avanzando
        recursivamente.  Se detiene si el esfuerzo parcial supera
        R_max (poda).
        """
        nonlocal mejor_estrategia, mejor_conflicto, mejor_esfuerzo
        nonlocal nodos_visitados, hojas_factibles, combinaciones_podadas

        nodos_visitados += 1

        # ---------- caso base: se fijó un valor para cada grupo ----------
        if indice == n:
            hojas_factibles += 1
            # Estrategia ya completa; aplicar y evaluar.
            nueva_red = red_social.aplicar_estrategia(estrategia_act)
            conflicto = nueva_red.calcular_conflicto_interno()

            if (conflicto < mejor_conflicto or
               (conflicto == mejor_conflicto and esfuerzo_act < mejor_esfuerzo)):
                mejor_conflicto = conflicto
                mejor_estrategia = estrategia_act.copy()
                mejor_esfuerzo = esfuerzo_act
            return

        # ---------- paso recursivo ----------
        grupo = red_social.grupos[indice]
        diff = abs(grupo.op1 - grupo.op2)        # |o1 - o2|
        costo_por_agente = diff * grupo.rig      # coste antes del techo

        for e in range(grupo.n + 1):
            # coste de moderar e agentes en este grupo
            costo_e = math.ceil(costo_por_agente * e)
            nuevo_esfuerzo = esfuerzo_act + costo_e

            # poda si ya superamos el presupuesto
            if nuevo_esfuerzo > red_social.R_max:
                combinaciones_podadas += 1
                continue

            estrategia_act[indice] = e
            backtrack(indice + 1, estrategia_act, nuevo_esfuerzo)

        # al volver, restauramos a 0 para evitar valores "fantasma"
        estrategia_act[indice] = 0
    # -----------------------------------------------------------

    backtrack(0, [0] * n, 0)

    stats = dict(
        nodos_visitados=nodos_visitados,
        hojas_factibles=hojas_factibles,
        combinaciones_podadas=combinaciones_podadas,
        total_comb_posibles=math.prod(g.n + 1 for g in red_social.grupos)
    )

    return mejor_estrategia, mejor_esfuerzo, mejor_conflicto, stats
