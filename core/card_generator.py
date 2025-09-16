import random

class CardGenerator:
    def __init__(self, modalidade="lotomania"):
        self.modalidade = modalidade
        self.total_dezenas = 100
        self.dezenas_por_cartao = 50

    def gerar_cartao(self):
        """
        Gera um único cartão com 50 dezenas, evitando excesso de sequências.
        """
        tentativas = 0
        while True:
            dezenas = sorted(random.sample(range(self.total_dezenas), self.dezenas_por_cartao))
            if not self.tem_sequencia(dezenas, tamanho=3, max_sequencias=2):
                return dezenas

            tentativas += 1
            if tentativas > 10000:
                raise Exception("❌ Não foi possível gerar um cartão válido após 10.000 tentativas.")
            # Debug opcional:
            # print(f"🔁 Cartão rejeitado por sequência: {dezenas}")

    def gerar_cartoes(self, quantidade=10):
        """
        Gera múltiplos cartões válidos.
        """
        cartoes = []
        while len(cartoes) < quantidade:
            cartao = self.gerar_cartao()
            cartoes.append(cartao)
        print(f"🧾 {quantidade} cartões gerados com sucesso.")
        return cartoes

    def tem_sequencia(self, dezenas, tamanho=3, max_sequencias=1):
        """
        Verifica se há mais de 'max_sequencias' consecutivas de tamanho >= 'tamanho'.
        """
        count = 1
        sequencias = 0
        for i in range(1, len(dezenas)):
            if dezenas[i] == dezenas[i - 1] + 1:
                count += 1
                if count >= tamanho:
                    sequencias += 1
                    count = 1  # reinicia após contar uma sequência
            else:
                count = 1
        return sequencias > max_sequencias
