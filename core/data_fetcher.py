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
load_dotenv()
TOKEN = os.getenv("API_LOTERIAS_TOKEN")

def baixar_concursos_lotomania(inicio=1, fim=2850):
    path = "data/processed/lotomania_resultados.csv"
    concursos_existentes = []

    if os.path.exists(path):
        df_existente = pd.read_csv(path)
        concursos_existentes = df_existente["concurso"].tolist()
        inicio = max(concursos_existentes) + 1
        print(f"📂 Continuando a partir do concurso {inicio}...")
    else:
        df_existente = pd.DataFrame()

    resultados = []

    for numero in range(inicio, fim + 1):
        url = f"https://loteriascaixa-api.herokuapp.com/api/lotomania/{numero}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                dezenas = dados.get("dezenas", [])
                concurso_num = dados.get("concurso")
                data_sorteio = dados.get("data")

                if len(dezenas) == 20 and concurso_num and data_sorteio:
                    resultados.append({
                        "concurso": concurso_num,
                        "data": data_sorteio,
                        "dezenas": ",".join(dezenas)
                    })
                    print(f"✅ Concurso {numero} baixado.")
                else:
                    print(f"⚠️ Concurso {numero} ignorado (dados incompletos).")
            else:
                print(f"❌ Erro ao baixar concurso {numero}: {response.status_code}")
        except Exception as e:
            print(f"❌ Falha na requisição do concurso {numero}: {e}")

    df_novo = pd.DataFrame(resultados)
    df_final = pd.concat([df_existente, df_novo], ignore_index=True)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    df_final.to_csv(path, index=False)
    print(f"\n💾 Total de concursos salvos: {len(df_final)}")