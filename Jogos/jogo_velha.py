"""
Jogo da Velha
"""

import random

# Constantes
INITIAL_GRID_INFO = [
    ["|1", "|2|", "3|"],
    ["|4", "|5|", "6|"],
    ["|7", "|8|", "9|"],
]

WINNING_SEQUENCES = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
    [1, 5, 9],
    [3, 5, 7],
]

BLOCKING_SEQUENCES = (
    [[a, b, c] for a, b, c in WINNING_SEQUENCES]
    + [[b, c, a] for a, b, c in WINNING_SEQUENCES]
    + [[c, a, b] for a, b, c in WINNING_SEQUENCES]
)



def exibir_tabuleiro(tabuleiro):
    """Exibe o tabuleiro formatado."""
    for i in range(0, 9, 3):
        print("".join(tabuleiro[i : i + 3]))


def criar_tabuleiro():
    """Cria o tabuleiro inicial."""
    return [
        "|_" if (i % 3 == 0) else ("_|" if (i % 3 == 2) else "|_|") for i in range(9)
    ]


def atualizar_tabuleiro(tabuleiro, posicao, simbolo):
    """Atualiza o tabuleiro com a jogada do jogador ou da IA."""
    idx = posicao - 1
    if idx % 3 == 0:
        tabuleiro[idx] = f"|{simbolo}"
    elif idx % 3 == 1:
        tabuleiro[idx] = f"|{simbolo}|"
    else:
        tabuleiro[idx] = f"{simbolo}|"


def verificar_vitoria(jogadas, simbolo):  # pylint: disable=unused-argument
    """Verifica se há uma combinação vencedora."""
    return any(all(pos in jogadas for pos in seq) for seq in WINNING_SEQUENCES)


def obter_jogada_ia(nivel, jogador, inimigo, jogadas_usadas):
    """Obtém a jogada da IA com base no nível de dificuldade."""
    opcoes_disponiveis = [i for i in range(1, 10) if i not in jogadas_usadas]

    if nivel == 1:
        return random.choice(opcoes_disponiveis)

    for seq in BLOCKING_SEQUENCES:
        a, b, c = seq
        if nivel == 2:
            if a in jogador and b in jogador and c not in jogadas_usadas:
                return c
        if nivel == 3:
            if a in inimigo and b in inimigo and c not in jogadas_usadas:
                return c
            if a in jogador and b in jogador and c not in jogadas_usadas:
                return c

    return random.choice(opcoes_disponiveis)


def escolher_simbolo():
    """Escolhe o símbolo do jogador e da IA."""
    while True:
        simbolo = input("Escolha sua forma [X|O]: ").upper()
        if simbolo in ["X", "O"]:
            return simbolo, "O" if simbolo == "X" else "X"
        print("Escolha inválida!")


def escolher_dificuldade():
    """Escolhe a dificuldade do jogo."""
    while True:
        nivel = input("Escolha a dificuldade: Facil(1) Médio(2) Difícil(3): ")
        if nivel in ["1", "2", "3"]:
            return int(nivel)
        print("Dificuldade inválida!")


def obter_jogada_jogador(simbolo_jogador, jogadas_usadas):
    """Obtém a jogada do jogador, garantindo que a entrada seja válida."""
    while True:
        try:
            jogada = int(input(f"({simbolo_jogador}) Escolha uma posição [1-9]: "))
            if jogada in range(1, 10) and jogada not in jogadas_usadas:
                return jogada
            print("Posição inválida ou já usada.")
        except ValueError:
            print("Entrada inválida.")


# Função principal modificada
def executar_turno(config_jogo, estado_jogo):
    """Executa um turno do jogo com parâmetros agrupados em dicionários."""
    if config_jogo["jogador_atual"] == "player":
        jogada = obter_jogada_jogador(
            config_jogo["simbolo_jogador"], estado_jogo["jogadas_usadas"]
        )
        estado_jogo["jogadas_jogador"].append(jogada)
        atualizar_tabuleiro(
            estado_jogo["tabuleiro"], jogada, config_jogo["simbolo_jogador"]
        )
    else:
        jogada = obter_jogada_ia(
            config_jogo["dificuldade"],
            estado_jogo["jogadas_jogador"],
            estado_jogo["jogadas_ia"],
            estado_jogo["jogadas_usadas"],
        )
        estado_jogo["jogadas_ia"].append(jogada)
        atualizar_tabuleiro(estado_jogo["tabuleiro"], jogada, config_jogo["simbolo_ia"])
        print(f"O inimigo ({config_jogo['simbolo_ia']}) escolheu: {jogada}")

    estado_jogo["jogadas_usadas"].append(jogada)
    exibir_tabuleiro(estado_jogo["tabuleiro"])

    if config_jogo["jogador_atual"] == "player" and verificar_vitoria(
        estado_jogo["jogadas_jogador"], config_jogo["simbolo_jogador"]
    ):
        print(f'Você venceu como "{config_jogo["simbolo_jogador"]}"!')
        return True
    if config_jogo["jogador_atual"] == "ia" and verificar_vitoria(
        estado_jogo["jogadas_ia"], config_jogo["simbolo_ia"]
    ):
        print(f'O inimigo "{config_jogo["simbolo_ia"]}" venceu!')
        return True
    return False


def jogo():
    """Função principal do jogo."""
    print("******** JOGO DA VELHA ********")

    confirmacao = input("Você quer jogar? [S|N]: ")
    while confirmacao not in ("S", "s", "N", "n"):
        print("Entrada inválida!")
        confirmacao = input("Você quer jogar? [S|N]: ")

    while confirmacao.upper() == "S":
        # Configurações do jogo
        config_jogo = {
            "simbolo_jogador": None,
            "simbolo_ia": None,
            "dificuldade": None,
            "jogador_atual": "player",
        }

        # Estado do jogo
        estado_jogo = {
            "tabuleiro": criar_tabuleiro(),
            "jogadas_jogador": [],
            "jogadas_ia": [],
            "jogadas_usadas": [],
        }

        # Configuração inicial
        config_jogo["simbolo_jogador"], config_jogo["simbolo_ia"] = escolher_simbolo()
        config_jogo["dificuldade"] = escolher_dificuldade()

        for line in INITIAL_GRID_INFO:
            print(*line, sep="")

        for turno in range(9):  # pylint: disable=unused-variable
            terminou = executar_turno(config_jogo, estado_jogo)
            if terminou:
                break
            config_jogo["jogador_atual"] = (
                "ia" if config_jogo["jogador_atual"] == "player" else "player"
            )
        else:
            print("Empate!")

        confirmacao = input("Você quer jogar novamente? [S|N]: ")
        while confirmacao not in ("S", "s", "N", "n"):
            print("Entrada inválida!")
            confirmacao = input("Você quer jogar novamente? [S|N]: ")


if __name__ == "__main__":
    jogo()
