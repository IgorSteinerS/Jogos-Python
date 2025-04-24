"""Menu de jogos
1 - Jogo da Velha
2 - Forca
3 - Jogo da Velha Minimax
4 - Pong
5 - Snake
"""

import forca
import jogo_velha
import jogo_velha_minimax
import pong
import snake


class Jogos:
    """Classe que representa os jogos disponíveis no menu"""

    todos_jogos = {}

    def __init__(self, jogo_id, name):
        self.__id = jogo_id
        self.__name = name
        Jogos.todos_jogos[self.__id] = self

    def __str__(self):
        return f"({self.__id}){self.__name}"

    def escolher_jogo(self):
        """Método que exibe o menu de jogos e permite ao usuário escolher um jogo para jogar"""
        while True:
            print("******************************")
            print("*******Escolha o Jogo!********")
            print("******************************")
            for _, instance in Jogos.todos_jogos.items():
                print(f"{instance}")
            print("-" * 25)
            print('Digite "Q" para sair.')
            jogo = input("Qual jogo? \n")

            try:
                if jogo.upper() == "Q":
                    return
                if int(jogo) not in Jogos.todos_jogos:
                    print(f"Escolha Invalida: Jogo ({jogo}) não existe")
                else:
                    run = int(jogo)
                    if run == 1:
                        jogo_velha.jogar()
                    elif run == 2:
                        forca.jogar()
                    elif run == 3:
                        jogo_velha_minimax.jogar()
                    elif run == 4:
                        pong.jogar()
                    elif run == 5:
                        snake.jogar()
            except ValueError:
                print("Escolha invalida: Valor não numérico")


jogo1 = Jogos(1, "Jogo da Velha")
jogo2 = Jogos(2, "Forca")
jogo3 = Jogos(3, "Jogo da Velha Minimax")
jogo4 = Jogos(4, "Pong")
jogo5 = Jogos(5, "Snake")


if __name__ == "__main__":
    jogo1.escolher_jogo()
