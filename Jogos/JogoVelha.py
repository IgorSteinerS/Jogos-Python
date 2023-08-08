import random

def jogar():
    print("******************************")
    print("********JOGO DA VELHA!********")
    print("******************************")

    winner = None
    while winner == None:
        used_positions = []
        num_used = []
        not_num_used = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        player_turn = 1
        total_moves = 0

        while True:
            mesmo = input("Você quer jogar mesmo? \n [S|N] \n ")
            if mesmo == "n" or mesmo == "N":
                winner = "End"
                break
            if mesmo == "s" or mesmo == "S":
                winner = None
                break
            else:
                print("Sim ou Não")
        if mesmo == "n" or mesmo == "N":
            break

        def win(player, enemy, used_positions):
            winning_sequences = [[1, 2, 3], [4, 5, 6], [7, 8, 9], 
                                [1, 4, 7], [2, 5, 8], [3, 6, 9],  
                                [1, 5, 9], [3, 5, 7]]            

            for sequence in winning_sequences:
                if all(str(position) + player in used_positions for position in sequence):
                    print(f"Player \"{player}\" wins!")
                    return 1 
                elif all(str(position) + enemy in used_positions for position in sequence):
                    print(f"Enemy \"{enemy}\" wins!")
                    return 2
                elif total_moves >= 9:
                    return 3  
            return None
        
        info = [["|1","|2|","3|"],
                ["|4","|5|","6|"],
                ["|7","|8|","9|"]]

        grid = {1 : "|_",
                2 : "|_|",
                3 : "_|",
                4 : "|_",
                5 : "|_|",
                6 : "_|",
                7 : "|_",
                8 : "|_|",
                9 : "_|"}
        
        for line in info:
            print(*line, sep="")

        while True:
            difficulty_level = input("Escolha a dificuldade: \n Facil(1)  Médio(2)   Difícil(3) \n")
            if difficulty_level != '1' and difficulty_level != '2' and difficulty_level != '3':
                print("Escolha invalida!!!")
            else:
                break

        while True:
            player = input("Escolha a sua forma: \n [X|O]\n").upper()
            if player == "X":
                print("Você é X")
                enemy = "O"
                break
            elif player == "O":
                print("Você é O")
                enemy = "X"
                break
            else:
                print("Escolha invalida!!!")
                pass

        while winner == None:
            while player_turn == 1:
                player_choice = int(input(f"({player})Escolha um número de 1 à 9 que está disponivel: "))

                if player_choice in range(1,10) and player_choice not in num_used:
                    used_positions.append(str(player_choice) + f"{player}")
                    num_used.append(player_choice)
                    not_num_used.remove(player_choice)
                    if player_choice == 1 or player_choice == 4 or player_choice == 7:
                        grid.update({player_choice : f"|{player}"})
                    elif player_choice == 2 or player_choice == 5 or player_choice == 8:
                        grid.update({player_choice : f"|{player}|"})
                    elif player_choice == 3 or player_choice == 6 or player_choice == 9:
                        grid.update({player_choice : f"{player}|"})

                    print(*[grid[i] for i in range(1, 4)], sep="")
                    print(*[grid[i] for i in range(4, 7)], sep="")
                    print(*[grid[i] for i in range(7, 10)], sep="")

                    print(used_positions)
                    if win(player, enemy, used_positions) == 1:
                        winner = player
                        print(f"Player \"{player}\" wins!")
                        break
                    elif win(player, enemy, used_positions) == 3:
                        winner = "tie"
                        print(f"Everyone Loses!!!!")
                        break
                    else:
                        player_turn = 2
                        total_moves += 1
            
                else:
                    print("Escolha inválida!!!")

    #---------------------------------------------------------------------------------------------------------------------
            while player_turn == 2:
                if difficulty_level == "1":
                    if not_num_used:
                        enemy_choice = random.choice(not_num_used)
                    else:
                        winner = "tie"
                        print(f"Everyone Loses!!!!")
                        break
                    used_positions.append(str(enemy_choice) + f"{enemy}")
                    num_used.append(enemy_choice)
                    not_num_used.remove(enemy_choice)
                    if enemy_choice == 1 or enemy_choice == 4 or enemy_choice == 7:
                        grid.update({enemy_choice : f"|{enemy}"})
                    elif enemy_choice == 2 or enemy_choice == 5 or enemy_choice == 8:
                        grid.update({enemy_choice : f"|{enemy}|"})
                    elif enemy_choice == 3 or enemy_choice == 6 or enemy_choice == 9:                        
                        grid.update({enemy_choice : f"{enemy}|"})

                    print(*[grid[i] for i in range(1, 4)], sep="")
                    print(*[grid[i] for i in range(4, 7)], sep="")
                    print(*[grid[i] for i in range(7, 10)], sep="")

                    print(used_positions)
                
                    if win(player, enemy, used_positions) == 2:
                        print(f"Enemy \"{enemy}\" wins!")
                        winner = enemy
                        break
                    elif win(player, enemy, used_positions) == 3:
                        winner = "tie"
                        print(f"Everyone Loses!!!!")
                        break
                    else:
                        player_turn = 1
                        total_moves += 1

            if winner != None:
                break        
        while True:            
            replay = input("Você quer jogar novamente: \n [S|N] \n").upper()
            if replay == "S":
                winner = None
                break
            elif replay == "N":
                winner = "End"
                break
            else:
                print("Escolha invalida!!!")
if __name__ == "__main__":
    jogar()
