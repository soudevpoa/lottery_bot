import ast  # usado para converter string de lista em lista real

class Analyzer:
    def __init__(self, resultados):
        self.resultados = resultados

    def analisar_cartoes(self, cartoes):
        analises = []

        for idx, cartao in enumerate(cartoes, 1):
            for resultado in self.resultados:
                dezenas_raw = resultado["dezenas"]

                # Converte string "03,07,12,..." em lista de inteiros
                if isinstance(dezenas_raw, str):
                    try:
                        dezenas_limpa = dezenas_raw.strip("[]")  # remove colchetes
                        dezenas_sorteadas = set(int(d.strip()) for d in dezenas_limpa.split(","))
                    except Exception as e:
                        print(f"⚠️ Erro ao interpretar dezenas do concurso {resultado['concurso']}: {e}")
                        continue

                else:
                    dezenas_sorteadas = set(map(int, dezenas_raw))

                dezenas_cartao = set(cartao)
                acertos = dezenas_cartao.intersection(dezenas_sorteadas)

                analises.append({
                    "cartao_id": idx,
                    "concurso": resultado["concurso"],
                    "data": resultado["data"],
                    "acertos": len(acertos),
                    "dezenas_acertadas": sorted(acertos)
                })

        return analises

    def filtrar_zero_acertos(self, analises):
        return [a for a in analises if a["acertos"] == 0]

