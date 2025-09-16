from core.data_fetcher import DataFetcher
from core.card_generator import CardGenerator
from core.analyzer import Analyzer
from core.strategist import Strategist
from core.utils import formatar_dezenas
from collections import defaultdict


def exibir_menu():
    print("\n🎰 LOTOMANIA BOT - MENU PRINCIPAL")
    print("1. Baixar concursos históricos")
    print("2. Gerar cartões inteligentes")
    print("3. Analisar desempenho")
    print("4. Gerar cartão estratégico")
    print("5. Sair")

def executar_bot():
    while True:
        exibir_menu()
        escolha = input("👉 Escolha uma opção: ")

        if escolha == "1":
            from core.data_fetcher import baixar_concursos_lotomania
            baixar_concursos_lotomania()

        elif escolha == "2":
            gerador = CardGenerator()
            cartoes = gerador.gerar_cartoes(quantidade=5)
            for i, c in enumerate(cartoes, 1):
                print(f"Cartão {i}: {formatar_dezenas(c)}")

        elif escolha == "3":
            resultados = DataFetcher().carregar_resultados()
            cartoes = CardGenerator().gerar_cartoes(quantidade=5)
            analises = Analyzer(resultados).analisar_cartoes(cartoes)

            resumo = defaultdict(list)
            for a in analises:
                resumo[a["cartao_id"]].append(a["acertos"])

            print("\n📈 Desempenho dos cartões:")
            for cartao_id, acertos_lista in resumo.items():
                media = sum(acertos_lista) / len(acertos_lista)
                print(f"Cartão {cartao_id}: média {media:.2f} acertos")

        elif escolha == "4":
            resultados = DataFetcher().carregar_resultados()
            estrategista = Strategist(resultados)
            cartao = estrategista.gerar_cartao_estrategico()
            print(f"\n🧠 Cartão estratégico gerado: {formatar_dezenas(cartao)}")

        elif escolha == "5":
            print("👋 Encerrando o bot. Até a próxima!")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    executar_bot()
