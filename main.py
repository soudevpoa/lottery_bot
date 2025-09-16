from core.data_fetcher import DataFetcher
from core.card_generator import CardGenerator
from core.analyzer import Analyzer
from core.strategist import Strategist
from core.utils import formatar_dezenas
from collections import defaultdict
import pandas as pd
import os


def exibir_menu():
    print("\n🎰 LOTOMANIA BOT - MENU PRINCIPAL")
    print("1. Baixar concursos históricos")
    print("2. Gerar cartões inteligentes")
    print("3. Analisar desempenho")
    print("4. Gerar cartão estratégico")
    print("5. Sair")
    print("6. Gerar lote de cartões estratégicos e ranquear desempenho")
    print("7. Modo Caçador de Fantasmas")


    

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

        elif escolha == "6":
            gerar_lote_estrategico(quantidade=100)
        elif escolha == "7":
            caçador_de_fantasmas()

            break

        else:
            print("❌ Opção inválida. Tente novamente.")

def gerar_lote_estrategico(quantidade=100):
    from core.data_fetcher import DataFetcher
    from core.strategist import Strategist
    from core.analyzer import Analyzer
    from core.utils import formatar_dezenas
    from collections import defaultdict

    resultados = DataFetcher().carregar_resultados()
    estrategista = Strategist(resultados)

    print(f"\n🧠 Gerando {quantidade} cartões estratégicos...")
    cartoes = []
    for i in range(quantidade):
        try:
            cartao = estrategista.gerar_cartao_estrategico()
            cartoes.append(cartao)
        except Exception as e:
            print(f"⚠️ Cartão {i+1} falhou: {e}")


    analisador = Analyzer(resultados)
    analises = analisador.analisar_cartoes(cartoes)

    resumo = defaultdict(list)
    for a in analises:
        resumo[a["cartao_id"]].append(a["acertos"])

    ranking = []
    for cartao_id, acertos_lista in resumo.items():
        media = sum(acertos_lista) / len(acertos_lista)
        ranking.append((cartao_id, media, acertos_lista))

    ranking.sort(key=lambda x: x[1])  # menor média primeiro

    print("\n🏆 Top 10 cartões com menor média de acertos:")
    for i, (cartao_id, media, acertos) in enumerate(ranking[:10], 1):
        print(f"{i}. Cartão {cartao_id}: média {media:.2f} | acertos: {acertos}")
        salvar_ranking_em_csv(ranking)


def salvar_ranking_em_csv(ranking, path="data/processed/ranking_fantasmas.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    registros = []
    for cartao_id, media, acertos_lista in ranking:
        registros.append({
            "cartao_id": cartao_id,
            "media_acertos": round(media, 2),
            "acertos": ",".join(map(str, acertos_lista))
        })
    df = pd.DataFrame(registros)
    df.to_csv(path, index=False)
    print(f"💾 Ranking salvo em {path}")

def caçador_de_fantasmas(limite_media=1.0):
    import pandas as pd

    path = "data/processed/ranking_fantasmas.csv"
    if not os.path.exists(path):
        print("⚠️ Ranking não encontrado. Gere os cartões primeiro.")
        return

    df = pd.read_csv(path)
    fantasmas = df[df["media_acertos"] <= limite_media]

    print(f"\n👻 Cartões com média ≤ {limite_media}:")
    for _, row in fantasmas.iterrows():
        print(f"Cartão {row['cartao_id']}: média {row['media_acertos']} | acertos: {row['acertos']}")


if __name__ == "__main__":
    executar_bot()
