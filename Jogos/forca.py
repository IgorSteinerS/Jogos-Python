import random
def jogar():
    print("******************************")
    print("************FORCA!************")
    print("******************************")
    
    jogar = True
    enforcado = False
    erros = 0
    letrasUsadas = []
    win = 0


    def end():
        
        if erros == 0:
            print(letrasUsadas)
            print("________")
            print("|     ")
            print("|     ")
            print("|     ")
            print(*hidden, sep="")
        elif erros == 1:
            print(letrasUsadas)
            print("________")
            print("|      O")
            print("|     ")
            print("|     ")
            print(*hidden, sep="")
        elif erros == 2:
            print(letrasUsadas)
            print("________")
            print("|      O")
            print("|      |")
            print("|     ")
            print(*hidden, sep="")
        elif erros == 3:
            print(letrasUsadas)
            print("________")
            print("|      O")
            print("|     /|")
            print("|     ")
            print(*hidden, sep="")
        elif erros == 4:
            print(letrasUsadas)
            print("________")
            print("|      O")
            print("|     /|\\")
            print("|     ")
            print(*hidden, sep="")
        elif erros == 5:
            print(letrasUsadas)
            print("________")
            print("|      O")
            print("|     /|\\")
            print("|     /")
            print(*hidden, sep="")
        elif erros == 6:
            print(letrasUsadas)
            print("________")
            print("|      O")
            print("|     /|\\")
            print("|     / \\")
            print(*hidden, sep="")

    while jogar == True:
        palavras = [
    "abacate", "acesso", "adeus", "agora", "amigo", "amor", "aniversario",
    "aprender", "ar", "arte", "aventura", "azul", "bala", "beleza",
    "brincar", "cachorro", "calma", "caminho", "campo", "caneta", "carinho",
    "carta", "casa", "celebrar", "chocolate", "chuva", "cidade", "coelho",
    "colorido", "coracao", "coragem", "correr", "crianca", "danca", "dia",
    "diferente", "doce", "energia", "esperanca", "estrela", "familia",
    "feliz", "floresta", "fogo", "fotografia", "girassol", "gratidao", "guitarra",
    "harmonia", "imaginar", "infinito", "janela", "lado", "liberdade", "luz",
    "magia", "mar", "memoria", "momento", "mundo", "musica", "natureza", "noite",
    "nuvem", "olhar", "paciencia", "paz", "perdao", "piano", "poesia", "por-do-sol",
    "porta", "preparar", "profundidade", "protecao", "raiz", "recordar", "refletir",
    "respeito", "rio", "riso", "rocha", "saudade", "segredo", "semente", "ser",
    "sorriso", "sonhar", "sorvete", "tempo", "terra", "tesouro", "tranquilidade",
    "unico", "universo", "valor", "vento", "verdade", "viagem", "vida", "viver",
    "andar", "aviao", "ave", "bambu", "barco", "barulho", "bela",
    "borboleta", "brilho", "caminhar", "cancao", "capaz", "carinho", "castelo",
    "cor", "cores", "corpo", "criatividade", "dar", "decidir", "descobrir",
    "desejo", "despertar", "doce", "elogiar", "encontrar", "equilibrio", "escalar",
    "esperar", "fe", "flor", "folha", "forte", "fruta", "garrafa", "gentileza",
    "gracejar", "grama", "grao", "guardar", "habito", "heroi", "hoje", "honrar",
    "humildade", "inocencia", "inspirar", "inventar", "jardim", "joia", "lado",
    "lealdade", "leveza", "liberdade", "livre", "lua", "luzir", "maravilha"
]

        palavra = random.randrange(0, len(palavras))
        palavraSecreta = palavras[palavra]
        palavraSecretaLis = list(palavraSecreta)
        hidden = "_" * len(palavraSecreta)
        hidden = list(hidden)


        while enforcado == False:
            end()
            if erros == 6:
                print(f"Você perdeu!!, a palavra secreta era {palavraSecreta} ")
                enforcado = True
                break
            letra = str(input("Escolha uma letra: "))

            if letra in letrasUsadas:
                erros += 1
            elif letra in palavraSecretaLis:
                letrasUsadas.append(letra)
                while letra in palavraSecretaLis:
                    hidden[palavraSecretaLis.index(letra)] = letra
                    palavraSecretaLis[palavraSecretaLis.index(letra)] = "-"
                for ganhou in hidden:
                    if ganhou in palavraSecreta:
                        win = win + 1
                if win >= len(palavraSecreta):
                    print("-" * len(palavraSecreta))
                    print(f"Você Ganhou!!!, a palavra era {palavraSecreta}")
                    print("-" * len(palavraSecreta))
                    break
                else:
                    win = 0
            else:
                letrasUsadas.append(letra)
                erros += 1

        letrasUsadas.clear()
        win = 0
        erros = 0
        enforcado = False
        novamente = True
        while novamente == True:
            escolha = input("Você quer jogar de novo? \n [S|N] \n")
            if escolha == "n" or escolha == "N":
                jogar = False
                novamente = False
            elif escolha == "s" or escolha == "S":
                jogar = True
                novamente = False
            else:
                print("Você só pode digitar S ou N")

if __name__ == '__main__':
    jogar()
