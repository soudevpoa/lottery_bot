def formatar_dezenas(dezenas):
    """
    Formata dezenas como strings com dois dígitos: [1, 2] → ['01', '02']
    """
    return [f"{d:02d}" for d in dezenas]

def contar_pares_impares(dezenas):
    """
    Retorna a contagem de pares e ímpares em uma lista de dezenas.
    """
    pares = sum(1 for d in dezenas if d % 2 == 0)
    impares = len(dezenas) - pares
    return pares, impares

def contar_altos_baixos(dezenas, limite=50):
    """
    Retorna a contagem de dezenas abaixo e acima do limite.
    """
    baixos = sum(1 for d in dezenas if d < limite)
    altos = len(dezenas) - baixos
    return baixos, altos
