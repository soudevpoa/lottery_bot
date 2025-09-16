from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class MLEngine:
    def __init__(self):
        self.model = RandomForestClassifier()

    def preparar_dados(self, resultados):
        """
        Converte resultados em dados binários para treino.
        """
        X = []
        y = []
        for r in resultados:
            dezenas = set(map(int, eval(r["dezenas"])) if isinstance(r["dezenas"], str) else r["dezenas"])
            linha = [1 if i in dezenas else 0 for i in range(100)]
            X.append(linha)
            y.append(1 if len(dezenas) == 0 else 0)  # Exemplo: classificar 0 acertos
        return X, y

    def treinar(self, resultados):
        X, y = self.preparar_dados(resultados)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        print("✅ Modelo treinado com sucesso.")

    def prever(self, cartoes):
        """
        Recebe lista de cartões e retorna probabilidade de 0 acertos.
        """
        X = [[1 if i in cartao else 0 for i in range(100)] for cartao in cartoes]
        return self.model.predict_proba(X)
