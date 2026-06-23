from dataclasses import dataclass, field
import random

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

PLAYER = "player"
COMPUTER = "computer"


@dataclass
class GameConfig:
    player_symbol: str
    computer_symbol: str
    difficulty: int
    current_player: str = PLAYER

@dataclass
class GameState:
    board: list
    player_moves: list = field(default_factory=list)
    computer_moves: list = field(default_factory=list)
    used_moves: list = field(default_factory=list)

def display_board(board):
    for index in range(0, 9, 3):
        print("".join(board[index:index + 3]))

def create_board():
    return [
        "|_" if index % 3 == 0
        else ("_|" if index % 3 == 2 else "|_|")
        for index in range(9)
    ]

def update_board(board, position, symbol):
    board_index = position - 1

    if board_index % 3 == 0:
        board[board_index] = f"|{symbol}"
    elif board_index % 3 == 1:
        board[board_index] = f"|{symbol}|"
    else:
        board[board_index] = f"{symbol}|"

def has_winner(moves):
    return any(
        all(position in moves for position in sequence)
        for sequence in WINNING_SEQUENCES
    )

def choose_move(
    difficulty,
    player_moves,
    computer_moves,
    used_moves,
):

    available_positions = [
        position
        for position in range(1, 10)
        if position not in used_moves
    ]

    if difficulty == 1:
        return random.choice(available_positions)

    for sequence in BLOCKING_SEQUENCES:
        first, second, third = sequence

        if difficulty == 2:
            if (
                first in player_moves
                and second in player_moves
                and third not in used_moves
            ):
                return third

        if difficulty == 3:
            if (
                first in computer_moves
                and second in computer_moves
                and third not in used_moves
            ):
                return third

            if (
                first in player_moves
                and second in player_moves
                and third not in used_moves
            ):
                return third

    return random.choice(available_positions)


def choose_symbol():
    while True:
        symbol = input("Escolha sua forma [X|O]: ").upper()

        if symbol in ("X", "O"):
            computer_symbol = "O" if symbol == "X" else "X"
            return symbol, computer_symbol

        print("Escolha inválida!")


def choose_difficulty():
    while True:
        difficulty = input(
            "Escolha a dificuldade: Fácil(1) Médio(2) Difícil(3): "
        )

        if difficulty in ("1", "2", "3"):
            return int(difficulty)

        print("Dificuldade inválida!")


def get_player_move(player_symbol, used_moves):
    while True:
        try:
            move = int(
                input(
                    f"({player_symbol}) "
                    "Escolha uma posição [1-9]: "
                )
            )

            if move in range(1, 10) and move not in used_moves:
                return move

            print("Posição inválida ou já utilizada.")

        except ValueError:
            print("Entrada inválida.")


def ask_yes_no(message):
    while True:
        answer = input(message).strip().upper()

        if answer in ("S", "N"):
            return answer

        print("Entrada inválida!")


def execute_turn(game_config, game_state):
    if game_config.current_player == PLAYER:

        move = get_player_move(
            game_config.player_symbol,
            game_state.used_moves,
        )

        game_state.player_moves.append(move)

        update_board(
            game_state.board,
            move,
            game_config.player_symbol,
        )

    else:

        move = choose_move(
            game_config.difficulty,
            game_state.player_moves,
            game_state.computer_moves,
            game_state.used_moves,
        )

        game_state.computer_moves.append(move)

        update_board(
            game_state.board,
            move,
            game_config.computer_symbol,
        )

        print(
            f"O inimigo "
            f"({game_config.computer_symbol}) "
            f"escolheu: {move}"
        )

    game_state.used_moves.append(move)

    display_board(game_state.board)

    if (
        game_config.current_player == PLAYER
        and has_winner(game_state.player_moves)
    ):
        print(
            f'Você venceu como '
            f'"{game_config.player_symbol}"!'
        )
        return True

    if (
        game_config.current_player == COMPUTER
        and has_winner(game_state.computer_moves)
    ):
        print(
            f'O inimigo '
            f'"{game_config.computer_symbol}" venceu!'
        )
        return True

    return False


def start_match():
    player_symbol, computer_symbol = choose_symbol()

    game_config = GameConfig(
        player_symbol=player_symbol,
        computer_symbol=computer_symbol,
        difficulty=choose_difficulty(),
    )

    game_state = GameState(
        board=create_board()
    )

    for line in INITIAL_GRID_INFO:
        print(*line, sep="")

    for _ in range(9):

        finished = execute_turn(
            game_config,
            game_state,
        )

        if finished:
            return

        game_config.current_player = (
            COMPUTER
            if game_config.current_player == PLAYER
            else PLAYER
        )

    print("Empate!")


def jogar():

    print("******** JOGO DA VELHA ********")

    while ask_yes_no(
        "Você quer jogar? [S|N]: "
    ) == "S":

        start_match()


if __name__ == "__main__":
    jogar()
