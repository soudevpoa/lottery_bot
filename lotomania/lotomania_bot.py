# lotomania/lotomania_bot.py

from core.data_fetcher import DataFetcher
from core.card_generator import CardGenerator
from core.analyzer import Analyzer
from core.ml_engine import MachineLearningEngine

class LotomaniaBot:
    def __init__(self):
        self.fetcher = DataFetcher(modalidade="lotomania")
        self.generator = CardGenerator(modalidade="lotomania")
        self.analyzer = Analyzer(modalidade="lotomania")
        self.ml_engine = MachineLearningEngine(modalidade="lotomania")

    def executar(self):
        print("🔄 Iniciando ciclo Lotomania...")
        resultados = self.fetcher.baixar_resultados()
        cartoes = self.generator.gerar_cartoes()
        self.analyzer.backtest(cartoes, resultados)
        self.ml_engine.treinar(cartoes, resultados)
        print("✅ Ciclo concluído.\n")
