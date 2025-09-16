def evitar_dezenas_recentes(cartao, resultados, n_concursos=3):
    """
    Remove dezenas que apareceram nos últimos n concursos.
    """
    recentes = set()
    for r in resultados[:n_concursos]:
        dezenas = r["dezenas"]
        if isinstance(dezenas, str):
            dezenas = eval(dezenas)
        recentes.update(map(int, dezenas))

    return [d for d in cartao if d not in recentes]

def tem_distribuicao_balanceada(dezenas):
    """
    Verifica se há equilíbrio entre pares/ímpares e altos/baixos.
    """
    from core.utils import contar_pares_impares, contar_altos_baixos
    pares, impares = contar_pares_impares(dezenas)
    baixos, altos = contar_altos_baixos(dezenas)
    return abs(pares - impares) <= 10 and abs(baixos - altos) <= 10
