import forca
import jogo_velha
import pong
import snake


class Game:

    registry = {}

    def __init__(self, game_id, name, action):
        self.game_id = game_id
        self.name = name
        self.action = action

        Game.registry[self.game_id] = self

    def __str__(self):
        return f"({self.game_id}) {self.name}"


def display_menu():

    print("******************************")
    print("******* ESCOLHA O JOGO *******")
    print("******************************")

    for game in Game.registry.values():
        print(game)

    print("-" * 30)
    print('Digite "Q" para sair.')


def execute_game(selected_option):

    game = Game.registry.get(selected_option)

    if game:
        game.action()
    else:
        print(
            f"Escolha inválida: jogo ({selected_option}) não existe."
        )


def choose_game():

    while True:
        display_menu()

        option = input("Qual jogo deseja jogar?\n").strip()

        if option.upper() == "Q":
            print("Encerrando aplicação...")
            break

        try:
            game_id = int(option)
            execute_game(game_id)

        except ValueError:
            print(
                "Escolha inválida: informe um número válido."
            )

Game(
    1,
    "Jogo da Velha",
    jogo_velha.jogar
)

Game(
    2,
    "Forca",
    forca.jogar
)

Game(
    3,
    "Pong",
    pong.jogar
)

Game(
    4,
    "Snake",
    snake.jogar
)


if __name__ == "__main__":
    choose_game()