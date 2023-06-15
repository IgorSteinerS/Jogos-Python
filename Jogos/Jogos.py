import Forca
import JogoVelha

def escolherJogo():
    loopEscolha = True
    while loopEscolha == True:

        print("******************************")
        print("*******Escolha o Jogo!********")
        print("******************************")
        print("(1)Forca | (2)Jogo da Velha")
        jogo = input("Qual jogo? \n")

        if jogo == "1":
            Forca.jogar()
        elif jogo == "2":
            JogoVelha.jogar()
        else:
            print("O valor escolhindo não tem jogo correspondente")
            pass
        loopOutro = True
        while loopOutro == True:
            print("-" * 20)
            acabou = input("Você quer escolher outro jogo? \n [S|N] \n")
            if acabou == "N" or acabou == "n":
                loopEscolha = False
                loopOutro = False
            elif acabou == "S" or acabou == "s":
                break
            else:
                print("Você só pode digitar S ou N")

if __name__ == '__main__':
    escolherJogo()