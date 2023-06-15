import random

def jogar():
    print("******************************")
    print("********JOGO DA VELHA!********")
    print("******************************")
    jogando = True
    while jogando == True:
        resultado = 4
        jogador = 0
        usedPositions = []
        totalMoves = 0
        
        def win():
            nonlocal resultado
            if "1O" in usedPositions and "2O" in usedPositions and "3O" in usedPositions:
                resultado = 1
            elif "4O" in usedPositions and "5O" in usedPositions and "6O" in usedPositions:
                resultado = 1
            elif "7O" in usedPositions and "8O" in usedPositions and "9O" in usedPositions:
                resultado = 1
            elif "1O" in usedPositions and "4O" in usedPositions and "7O" in usedPositions:
                resultado = 1
            elif "2O" in usedPositions and "5O" in usedPositions and "8O" in usedPositions:
                resultado = 1
            elif "3O" in usedPositions and "6O" in usedPositions and "9O" in usedPositions:
                resultado = 1
            elif "1O" in usedPositions and "5O" in usedPositions and "9O" in usedPositions:
                resultado = 1
            elif "3O" in usedPositions and "5O" in usedPositions and "7O" in usedPositions:
                resultado = 1
            elif "1X" in usedPositions and "2X" in usedPositions and "3X" in usedPositions:
                resultado = 2
            elif "4X" in usedPositions and "5X" in usedPositions and "6X" in usedPositions:
                resultado = 2
            elif "7X" in usedPositions and "8X" in usedPositions and "9X" in usedPositions:
                resultado = 2
            elif "1X" in usedPositions and "4X" in usedPositions and "7X" in usedPositions:
                resultado = 2
            elif "2X" in usedPositions and "5X" in usedPositions and "8X" in usedPositions:
                resultado = 2
            elif "3X" in usedPositions and "6X" in usedPositions and "9X" in usedPositions:
                resultado = 2
            elif "1X" in usedPositions and "5X" in usedPositions and "9X" in usedPositions:
                resultado = 2
            elif "3X" in usedPositions and "5X" in usedPositions and "7X" in usedPositions:
                resultado = 2
            elif totalMoves >= 9 and resultado == 4:
                resultado = 3
            
        
        info = [["|1","|2|","3|"],["|4","|5|","6|"],["|7","|8|","9|"]]

        gridTop = {1 : "|_",
                    2 : "|_|",
                    3 : "_|"
                    }

        gridMid = {4 : "|_",
                    5 : "|_|",
                    6 : "_|"
                    }

        gridBot = {7 : "|_",
                    8 : "|_|",
                    9 : "_|"
                    }
        for line in info:
            print(*line, sep="")



        print("(O)Jogador |(X)CPU ")

        posiçãoO = 0
        posiçãoX = 0
        jogador = 1
        while resultado == 4:

            while jogador == 1:
                win()
                if jogador == 1:
                    posiçãoO = int(input("(O)Escolha um número de 1 à 9 que está disponivel: "))
                if posiçãoO == 1:
                    if "1O" in usedPositions or "1X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridTop.update({1 : "|O"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        jogador = 2
                elif posiçãoO == 2:
                    if "2O" in usedPositions or "2X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridTop.update({2 : "|O|"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        
                        jogador = 2
                elif posiçãoO == 3:
                    if "3O" in usedPositions or "3X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridTop.update({3 : "O|"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        
                        jogador = 2
                elif posiçãoO == 4:
                    if "4O" in usedPositions or "4X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridMid.update({4 : "|O"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        
                        jogador = 2
                elif posiçãoO == 5:
                    if "5O" in usedPositions or "5X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridMid.update({5 : "|O|"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        
                        jogador = 2
                elif posiçãoO == 6:
                    if "6O" in usedPositions or "6X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridMid.update({6 : "O|"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        
                        jogador = 2
                elif posiçãoO == 7:
                    if "7O" in usedPositions or "7X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridBot.update({7 : "|O"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        
                        jogador = 2
                elif posiçãoO == 8:
                    if "8O" in usedPositions or "8X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridBot.update({8 : "|O|"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        
                        jogador = 2
                elif posiçãoO == 9:
                    if "9O" in usedPositions or "9X" in usedPositions:
                        print("Escolha inválida!!!")
                        jogador = 1
                    else:
                        gridBot.update({9 : "O|"})
                        usedPositions.append(str(posiçãoO) + "O")
                        totalMoves += 1
                        jogador = 2
                win()
                if resultado != 4:
                    break        
            #****************************************************************************
            while jogador == 2:
                win()
                if jogador == 2:
                    posiçãoX = random.randint(1, 9)
                if posiçãoX == 1:
                    if "1X" in usedPositions or "1O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridTop.update({1 : "|X"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1
                        
                        jogador = 1
                elif posiçãoX == 2:
                    if "2X" in usedPositions or "2O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridTop.update({2 : "|X|"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1
                        
                        jogador = 1
                elif posiçãoX == 3:
                    if "3X" in usedPositions or "3O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridTop.update({3 : "X|"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1
                        
                        jogador = 1
                elif posiçãoX == 4:
                    if "4X" in usedPositions or "4O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridMid.update({4 : "|X"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1
                        
                        jogador = 1
                elif posiçãoX == 5:
                    if "5X" in usedPositions or "5O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridMid.update({5 : "|X|"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1

                        jogador = 1
                elif posiçãoX == 6:
                    if "6X" in usedPositions or "6O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridMid.update({6 : "X|"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1

                        jogador = 1
                elif posiçãoX == 7:
                    if "7X" in usedPositions or "7O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridBot.update({7 : "|X"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1

                        jogador = 1
                elif posiçãoX == 8:
                    if "8X" in usedPositions or "8O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridBot.update({8 : "|X|"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1

                        jogador = 1
                elif posiçãoX == 9:
                    if "9X" in usedPositions or "9O" in usedPositions:
                        #print("Escolha inválida!!!")
                        jogador = 2
                    else:
                        gridBot.update({9 : "X|"})
                        usedPositions.append(str(posiçãoX) + "X")
                        totalMoves += 1

                        jogador = 1
                win()
                if resultado != 4:
                    break    
                #totalMoves += 1
            print(*gridTop.values(), sep="")
            print(*gridMid.values(), sep="")
            print(*gridBot.values(), sep="")
            print(usedPositions)
            win()
            if resultado == 1:
                print("-" * 20)
                print("Parabéns (O), você ganhou!!!")
                print("-" * 20)
                break
            
            elif resultado == 2:
                print("-" * 20)
                print("Parabéns (X), você ganhou!!!")
                print("-" * 20)
                break
            elif resultado == 3:
                print("-" * 20)
                print("Vocês empataram!!!")
                print("-" * 20)
                break

        gridTop.update({1 : "|_",
                    2 : "|_|",
                    3 : "_|"
                    })

        gridMid.update({4 : "|_",
                    5 : "|_|",
                    6 : "_|"
                    })

        gridBot.update({7 : "|_",
                    8 : "|_|",
                    9 : "_|"
                    })
        usedPositions.clear()

        escolha = (input("Você quer jogar de novo? \n [S|N] \n"))
        print("-" * 20)
        if escolha == "n" or escolha == "N":
            jogando = False
            break
        else:
            jogando = True       

if __name__ == "__main__":
    jogar()