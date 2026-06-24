# Jogos/forca.py
import random

HANGMAN_STAGES = [
    ("________", "|     ", "|     ", "|     "),
    ("________", "|      O", "|     ", "|     "),
    ("________", "|      O", "|      |", "|     "),
    ("________", "|      O", "|     /|", "|     "),
    ("________", "|      O", "|     /|\\", "|     "),
    ("________", "|      O", "|     /|\\", "|     /"),
    ("________", "|      O", "|     /|\\", "|     / \\"),
]

PORTUGUESE_WORDS = [
    "abacate",
    "acesso",
    "adeus",
    "agora",
    "amigo",
    "amor",
    "aniversario",
    "aprender",
    "ar",
    "arte",
    "aventura",
    "azul",
    "bala",
    "beleza",
    "brincar",
    "cachorro",
    "calma",
    "caminho",
    "campo",
    "caneta",
    "carinho",
    "carta",
    "casa",
    "celebrar",
    "chocolate",
    "chuva",
    "cidade",
    "coelho",
    "colorido",
    "coracao",
    "coragem",
    "correr",
    "crianca",
    "danca",
    "dia",
    "diferente",
    "doce",
    "energia",
    "esperanca",
    "estrela",
    "familia",
    "feliz",
    "floresta",
    "fogo",
    "fotografia",
    "girassol",
    "gratidao",
    "guitarra",
    "harmonia",
    "imaginar",
    "infinito",
    "janela",
    "lado",
    "liberdade",
    "luz",
    "magia",
    "mar",
    "memoria",
    "momento",
    "mundo",
    "musica",
    "natureza",
    "noite",
    "nuvem",
    "olhar",
    "paciencia",
    "paz",
    "perdao",
    "piano",
    "poesia",
    "por-do-sol",
    "porta",
    "preparar",
    "profundidade",
    "protecao",
    "raiz",
    "recordar",
    "refletir",
    "respeito",
    "rio",
    "riso",
    "rocha",
    "saudade",
    "segredo",
    "semente",
    "ser",
    "sorriso",
    "sonhar",
    "sorvete",
    "tempo",
    "terra",
    "tesouro",
    "tranquilidade",
    "unico",
    "universo",
    "valor",
    "vento",
    "verdade",
    "viagem",
    "vida",
    "viver",
    "andar",
    "aviao",
    "ave",
    "bambu",
    "barco",
    "barulho",
    "bela",
    "borboleta",
    "brilho",
    "caminhar",
    "cancao",
    "capaz",
    "carinho",
    "castelo",
    "cor",
    "cores",
    "corpo",
    "criatividade",
    "dar",
    "decidir",
    "descobrir",
    "desejo",
    "despertar",
    "doce",
    "elogiar",
    "encontrar",
    "equilibrio",
    "escalar",
    "esperar",
    "fe",
    "flor",
    "folha",
    "forte",
    "fruta",
    "garrafa",
    "gentileza",
    "gracejar",
    "grama",
    "grao",
    "guardar",
    "habito",
    "heroi",
    "hoje",
    "honrar",
    "humildade",
    "inocencia",
    "inspirar",
    "inventar",
    "jardim",
    "joia",
    "lado",
    "lealdade",
    "leveza",
    "liberdade",
    "livre",
    "lua",
    "luzir",
    "maravilha",
]

MAX_MISTAKES = len(HANGMAN_STAGES) - 1


def reveal_letter(letter: str, secret_word: str, hidden_word: list) -> list:
    for i, char in enumerate(secret_word):
        if char == letter:
            hidden_word[i] = letter


def show_game_board(mistakes_made: int):
    print(*HANGMAN_STAGES[mistakes_made], sep="\n")


def jogar() -> None:
    chosen_word = random.choice(PORTUGUESE_WORDS)
    hidden = ["_"] * len(chosen_word)
    used_letters: list[str] = []
    mistakes = 0

    while True:
        print(used_letters)
        show_game_board(mistakes)
        print(*hidden, sep="")

        letter = input("Escolha uma letra: ").lower().strip()

        if letter in used_letters:
            print("Você já usou essa letra!")
            continue

        used_letters.append(letter)

        if letter in chosen_word:
            reveal_letter(letter, chosen_word, hidden)
            if "_" not in hidden:
                print(f"Você ganhou! A palavra era: {chosen_word}")
                break
        else:
            mistakes += 1
            if mistakes >= MAX_MISTAKES:
                show_game_board(mistakes)
                print(f"Você perdeu! A palavra era: {chosen_word}")
                break


if __name__ == "__main__":
    jogar()
