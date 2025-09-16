import requests
import pandas as pd
import os
from dotenv import load_dotenv
import time

load_dotenv()

class DataFetcher:
    def __init__(self, modalidade="lotomania"):
        self.modalidade = modalidade
        self.token = os.getenv("APILOTERIAS_TOKEN")
        self.api_url = "http://apiloterias.com.br/app/resultado"
        self.resultados = []

    def baixar_resultados(self, limite=10, concurso_inicial=None):
        """
        Baixa os últimos resultados reais da Lotomania via API oficial.
        Se concurso_inicial for None, começa pelo último disponível.
        """
        print(f"🔎 Buscando últimos {limite} resultados da {self.modalidade}...")

        concursos = []
        concurso_atual = concurso_inicial or ""

        for i in range(limite):
            params = {
                "loteria": self.modalidade,
                "token": self.token,
                "concurso": concurso_atual
            }

            try:
                response = requests.get(self.api_url, params=params)
                response.raise_for_status()
                data = response.json()

                if "erro" in data:
                    print(f"⚠️ Erro no concurso {concurso_atual or 'último'}: {data['erro']}")
                    break

                concurso_num = data.get("numero_concurso")
                if not concurso_num:
                    print("⚠️ Concurso inválido recebido, encerrando busca.")
                    break

                dezenas = data.get("dezenas", [])
                data_concurso = data.get("data_concurso", "sem data")

                concursos.append({
                    "concurso": concurso_num,
                    "data": data_concurso,
                    "dezenas": dezenas
                })

                concurso_atual = str(int(concurso_num) - 1)

            except requests.RequestException as e:
                print(f"❌ Erro de conexão: {e}")
                break

        self.resultados = concursos
        return concursos

    def salvar_resultados(self, path="data/processed/lotomania_resultados.csv"):
        """
        Salva os resultados em CSV para uso posterior.
        """
        if not self.resultados:
            print("⚠️ Nenhum resultado para salvar.")
            return

        df = pd.DataFrame(self.resultados)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
        print(f"💾 Resultados salvos em {path}")

    def carregar_resultados(self, path="data/processed/lotomania_resultados.csv"):
        """
        Carrega resultados salvos anteriormente.
        """
        if not os.path.exists(path):
            print("⚠️ Arquivo de resultados não encontrado.")
            return []

        df = pd.read_csv(path)
        self.resultados = df.to_dict(orient="records")
        print(f"📂 {len(self.resultados)} resultados carregados de {path}")
        return self.resultados

# 🔽 Função utilitária fora da classe
def baixar_concursos_lotomania(inicio=1, fim=2500):
    """
    Baixa concursos da Lotomania usando a API apiloterias.com.br
    """
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv("APILOTERIAS_TOKEN")

    if not token:
        print("❌ Token da API não encontrado no .env.")
        return

    concursos = []
    for numero in range(inicio, fim + 1):
        url = f"http://apiloterias.com.br/app/resultado?loteria=lotomania&token={token}&concurso={numero}"
        try:
            r = requests.get(url)
            if r.status_code == 200 and r.text.strip():
                dados = r.json()
                dezenas = dados.get("dezenas", [])
                concursos.append({
                    "concurso": dados.get("numero_concurso", numero),
                    "data": dados.get("data_concurso", ""),
                    "dezenas": [int(d) for d in dezenas]
                })
                print(f"✅ Concurso {numero} baixado.")
            else:
                print(f"⚠️ Concurso {numero} retornou resposta inválida.")
        except Exception as e:
            print(f"❌ Erro no concurso {numero}: {e}")
        time.sleep(0.2)

    df = pd.DataFrame(concursos)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/lotomania_resultados.csv", index=False)
    print(f"\n✅ {len(concursos)} concursos salvos em data/processed/lotomania_resultados.csv")

