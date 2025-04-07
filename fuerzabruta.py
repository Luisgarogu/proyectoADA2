import math

def modciFuerzaBruta(red_social):
    n = len(red_social.grupos)
    mejor_estrategia = [0] * n
    mejor_conflicto = red_social.calcular_conflicto_interno()
    mejor_esfuerzo = 0

    def generar_estrategias(indice, estrategia_actual, esfuerzo_actual):
        nonlocal mejor_estrategia, mejor_conflicto, mejor_esfuerzo

        if indice == n:
            if esfuerzo_actual <= red_social.R_max:
                # Aplicar estrategia y calcular nuevo conflicto
                nueva_red = red_social.aplicar_estrategia(estrategia_actual)
                conflicto = nueva_red.calcular_conflicto_interno()
                
                if conflicto < mejor_conflicto or (conflicto == mejor_conflicto and esfuerzo_actual < mejor_esfuerzo):
                    mejor_conflicto = conflicto
                    mejor_estrategia = estrategia_actual.copy()
                    mejor_esfuerzo = esfuerzo_actual
            return
        
        grupo = red_social.grupos[indice]
        
        for i in range(grupo.n + 1):
            nuevo_esfuerzo = esfuerzo_actual
            if i > 0:
                nuevo_esfuerzo += math.ceil(abs(grupo.op1 - grupo.op2) * grupo.rig * i)
            
            if nuevo_esfuerzo <= red_social.R_max:
                estrategia_actual[indice] = i
                generar_estrategias(indice + 1, estrategia_actual, nuevo_esfuerzo)

    generar_estrategias(0, [0] * n, 0)
    return (mejor_estrategia, mejor_esfuerzo, mejor_conflicto)