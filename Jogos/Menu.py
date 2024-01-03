import Forca
import JogoVelha

class Jogos:
    todos_jogos = {}

    def __init__(self, id, name):
        self.__id = id
        self.__name = name
        Jogos.todos_jogos[self.__id] = self
                
    def __str__(self):
        return f"({self.__id}){self.__name}"    

    def escolherJogo(self):
        while True:
            print("******************************")
            print("*******Escolha o Jogo!********")
            print("******************************")
            for id, instance in Jogos.todos_jogos.items():
                print(f"{instance}")
            print("-" * 25)
            print("Digite \"Q\" para sair.")
            jogo = input("Qual jogo? \n")
            
            try:
                if jogo.upper() == "Q":
                    return 
                elif int(jogo) not in Jogos.todos_jogos.keys():
                    print(f"Escolha Invalida: Jogo ({jogo}) não existe")
                else:
                    run = int(jogo)
                    if run == 1:
                        JogoVelha.jogar()
                    elif run == 2:
                        Forca.jogar()        
            except ValueError:
                print("Escolha invalida: Valor não numérico")

                

jogo1 = Jogos(1, "Jogo da Velha")
jogo2 = Jogos(2, "Forca")


jogo1.escolherJogo()

if __name__ == '__main__':
    Jogos.escolherJogo()
    