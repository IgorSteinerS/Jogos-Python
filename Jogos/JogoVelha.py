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
        winning_sequences = [[1, 2, 3], [4, 5, 6], [7, 8, 9], 
                            [1, 4, 7], [2, 5, 8], [3, 6, 9],  
                            [1, 5, 9], [3, 5, 7]]
        
        blocking_sequences = [[1,2,3], [1,3,2], [2,3,1], [4,5,6], [4,6,5], [5,6,4], [7,8,9], [7,9,8], [8,9,7],
                                [1,4,7], [1,7,4], [4,7,1], [2,5,8], [2,8,5], [5,8,2], [3,6,9], [3,7,5], [6,9,3],
                                [1,5,9], [1,9,5], [5,9,1], [3,5,7], [3,7,5], [5,7,3]]
            
        while True:
            play_game = input("Você quer jogar mesmo? \n [S|N] \n ")
            if play_game == "n" or play_game == "N":
                winner = "End"
                break
            if play_game == "s" or play_game == "S":
                winner = None
                break
            else:
                print("Sim ou Não")
        if play_game == "n" or play_game == "N":
            break

        def win(player, enemy, used_positions):   
            for sequence in winning_sequences:
                if all(str(position) + player in used_positions for position in sequence):
                    return 1 
                elif all(str(position) + enemy in used_positions for position in sequence):
                    return 2
                elif total_moves >= 9:
                    return 3  
            return None              
          
        def update():
            used_positions.append(str(enemy_choice) + f"{enemy}")
            num_used.append(enemy_choice)
            not_num_used.remove(enemy_choice)
            if enemy_choice == 1 or enemy_choice == 4 or enemy_choice == 7:
                current_game_grid.update({enemy_choice : f"|{enemy}"})
            elif enemy_choice == 2 or enemy_choice == 5 or enemy_choice == 8:
                current_game_grid.update({enemy_choice : f"|{enemy}|"})
            elif enemy_choice == 3 or enemy_choice == 6 or enemy_choice == 9:                        
                current_game_grid.update({enemy_choice : f"{enemy}|"})

            print(*[current_game_grid[i] for i in range(1, 4)], sep="")
            print(*[current_game_grid[i] for i in range(4, 7)], sep="")
            print(*[current_game_grid[i] for i in range(7, 10)], sep="")

            print(used_positions)       

        initial_grid_info = [["|1","|2|","3|"],
                ["|4","|5|","6|"],
                ["|7","|8|","9|"]]

        current_game_grid = {1 : "|_",
                2 : "|_|",
                3 : "_|",
                4 : "|_",
                5 : "|_|",
                6 : "_|",
                7 : "|_",
                8 : "|_|",
                9 : "_|"}
        
        for line in initial_grid_info:
            print(*line, sep="")

        while True:
            difficulty_level = input("Escolha a dificuldade: \n Facil(1)  Médio(2)   Difícil(3) \n")
            if difficulty_level not in ['1', '2', '3']:
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
                try:
                    player_choice = int(input(f"({player})Escolha um número de 1 à 9 que está disponivel: "))

                    if player_choice in range(1,10) and player_choice not in num_used:
                        used_positions.append(str(player_choice) + f"{player}")
                        num_used.append(player_choice)
                        not_num_used.remove(player_choice)
                        if player_choice == 1 or player_choice == 4 or player_choice == 7:
                            current_game_grid.update({player_choice : f"|{player}"})
                        elif player_choice == 2 or player_choice == 5 or player_choice == 8:
                            current_game_grid.update({player_choice : f"|{player}|"})
                        elif player_choice == 3 or player_choice == 6 or player_choice == 9:
                            current_game_grid.update({player_choice : f"{player}|"})

                        print(*[current_game_grid[i] for i in range(1, 4)], sep="")
                        print(*[current_game_grid[i] for i in range(4, 7)], sep="")
                        print(*[current_game_grid[i] for i in range(7, 10)], sep="")

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
                        print("Escolha inválida: Escolha uma posição que ainda não foi usada.")
                except ValueError:
                    print("Escolha Inválida: Valor não numérico.")
    #---------------------------------------------------------------------------------------------------------------------
            while player_turn == 2:
                if difficulty_level == "1":
                    if not_num_used:
                        enemy_choice = random.choice(not_num_used)
                    else:
                        winner = "tie"
                        print(f"Everyone Loses!!!!")
                        break
                    update()
                
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

                elif difficulty_level == "2":
                    if not_num_used:
                        enemy_choice = None
                        for sequence in blocking_sequences:
                            for spot in sequence[0:2]:
                                if all(str(spot) + player in used_positions for spot in sequence[0:2]) and str(sequence[2]) + enemy not in used_positions:
                                    enemy_choice = int(sequence[2])
                                    break    
                        if enemy_choice is None:
                            enemy_choice = random.choice(not_num_used)                           
                    else:
                        winner = "tie"
                        print("Everyone Loses!!!!")
                        break

                    update()

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

                elif difficulty_level == "3":
                    if not_num_used:
                        enemy_choice = None
                        for sequence in blocking_sequences:
                            for spot in sequence[0:2]:
                                if all(str(spot) + enemy in used_positions for spot in sequence[0:2]) and str(sequence[2]) + player not in used_positions:
                                    enemy_choice = int(sequence[2])
                                    break
                                elif all(str(spot) + player in used_positions for spot in sequence[0:2]) and str(sequence[2]) + enemy not in used_positions:
                                    enemy_choice = int(sequence[2])
                                    break
                        if enemy_choice is None:
                            enemy_choice = random.choice(not_num_used)                           
                    else:
                        winner = "tie"
                        print("Everyone Loses!!!!")
                        break

                    update()

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