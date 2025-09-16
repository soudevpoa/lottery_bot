from core.card_generator import CardGenerator
from lotomania.patterns import evitar_dezenas_recentes, tem_distribuicao_balanceada
from core.utils import formatar_dezenas
from core.ml_engine import MLEngine
import random

class Strategist:
    def __init__(self, resultados):
        self.resultados = resultados
        self.gerador = CardGenerator()
        self.ml = MLEngine()
        self.ml.treinar(resultados)

    def gerar_cartao_estrategico(self):
        """
        Gera um cartão filtrado por padrões e avaliado pelo modelo.
        """
        tentativas = 0
        while True:
            dezenas = self.gerador.gerar_cartao()
            dezenas_filtradas = evitar_dezenas_recentes(dezenas, self.resultados, n_concursos=3)

            if len(dezenas_filtradas) < 50:
                # Repreenche até 50 dezenas
                faltando = 50 - len(dezenas_filtradas)
                pool = [d for d in range(100) if d not in dezenas_filtradas]
                dezenas_filtradas += random.sample(pool, faltando)


            if tem_distribuicao_balanceada(dezenas_filtradas):
                prob = self.ml.prever([dezenas_filtradas])[0][0]  # probabilidade de 0 acertos
                if prob > 0.3:  # ajustável
                    return dezenas_filtradas

            tentativas += 1
            if tentativas > 20000:
                raise Exception("❌ Não foi possível gerar um cartão estratégico após 5000 tentativas.")
