class TicTacToe:
    def __init__(self):
        self.total_moves = 0
        self.board = [1,2,3,4,5,6,7,8,9]
        self.available_nums = [1,2,3,4,5,6,7,8,9]
        self.current_game_grid = {1 : "|_",
                2 : "|_|",
                3 : "_|",
                4 : "|_",
                5 : "|_|",
                6 : "_|",
                7 : "|_",
                8 : "|_|",
                9 : "_|"}
        self.winning_sequences = [[0, 1, 2], [3, 4, 5], [6, 7, 8], 
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],  
                    [0, 4, 8], [2, 4, 6]]

    def show_Rules(self):
        initial_grid_info = [["|1","|2|","3|"],
                ["|4","|5|","6|"],
                ["|7","|8|","9|"]]
        for line in initial_grid_info:
            print(*line, sep="")

    def show_current_game_grid(self):
        print(*[self.current_game_grid[i] for i in range(1, 4)], sep="")
        print(*[self.current_game_grid[i] for i in range(4, 7)], sep="")
        print(*[self.current_game_grid[i] for i in range(7, 10)], sep="")

    def check_win(self, player_Symbol, enemy_Symbol):   
        for sequence in self.winning_sequences:
            if all(self.board[position] == player_Symbol for position in sequence):
                return -1  # Lower score for player win
            elif all(self.board[position] == enemy_Symbol for position in sequence):
                return 1  # Higher score for AI win
        if self.total_moves >= 9:
            return 0  # Draw
        return 2  # Game isn't over 
    
    def winner(self, player_Symbol, enemy_Symbol):
        game_over = False
        win_check = self.check_win(player_Symbol, enemy_Symbol)
        if win_check == -1:
            print(f"Player {player_Symbol} has won!")
            game_over = True
        elif win_check == 1:
            print(f"Player {enemy_Symbol} has won!")
            game_over = True
        elif win_check == 0:
            print(f"Draw!")
            game_over = True
        return game_over

    def start_Game(self):
        self.show_Rules()
        while True:
            player_Symbol = input("Choose your symbol: \n [X|O]\n").upper()
            if player_Symbol == "X":
                print("You are X.")
                enemy_Symbol = "O"
                break
            elif player_Symbol == "O":
                print("You are O.")
                enemy_Symbol = "X"
                break
            else:
                print("Invalid Choice!!!")
                
            
        while True:
            self.player_turn(player_Symbol)
            

            if self.winner(player_Symbol, enemy_Symbol):
                break

            self.enemy_Turn(enemy_Symbol, player_Symbol)

            if self.winner(player_Symbol, enemy_Symbol):
                break

    def player_turn(self, player_Symbol):
        self.show_current_game_grid()
        while True:
            try:

                player_choice = int(input("Choose a valid position: "))
                player_choice -= 1
                if player_choice not in range(0,9):
                    print("Invalid Choice: Non Existent Position.")
                elif self.board[player_choice] == "X" or self.board[player_choice] == "O":
                    print("Invalid Choice: Position has already been taken.")
                else:
                    self.board[player_choice] = player_Symbol
                    self.available_nums.remove(player_choice + 1)
                    print(self.board)

                    if player_choice == 0 or player_choice == 3 or player_choice == 6:
                        self.current_game_grid.update({player_choice + 1 : f"|{player_Symbol}"})
                    elif player_choice == 1 or player_choice == 4 or player_choice == 7:
                        self.current_game_grid.update({player_choice + 1 : f"|{player_Symbol}|"})
                    elif player_choice == 2 or player_choice == 5 or player_choice == 8:
                        self.current_game_grid.update({player_choice + 1 : f"{player_Symbol}|"})
                    self.total_moves += 1
                    break

            except ValueError:
                print("Invalid Choice: Non Numeric Value")

    def enemy_Turn(self, enemy_Symbol, player_Symbol):
        self.show_current_game_grid()
        enemy_choice = self.find_best_move(enemy_Symbol, player_Symbol)

        self.board[enemy_choice] = enemy_Symbol
        self.available_nums.remove(enemy_choice + 1)

        if enemy_choice == 0 or enemy_choice == 3 or enemy_choice == 6:
            self.current_game_grid.update({enemy_choice + 1 : f"|{enemy_Symbol}"})
        elif enemy_choice == 1 or enemy_choice == 4 or enemy_choice == 7:
            self.current_game_grid.update({enemy_choice + 1 : f"|{enemy_Symbol}|"})
        elif enemy_choice == 2 or enemy_choice == 5 or enemy_choice == 8:
            self.current_game_grid.update({enemy_choice + 1 : f"{enemy_Symbol}|"})
        self.total_moves += 1
        print(self.board)
        return

    def minimax(self, enemy_Symbol, player_Symbol, maximizing, max_depth):
        result = self.check_win(player_Symbol, enemy_Symbol)
        if result != 2 or max_depth == 0:  # O jogo acabou ou atingiu a profundidade máxima
            return result

        if maximizing:
            best = -10000  # Valor muito pequeno

            for i in range(9):  # Percorre todas as células
                if self.board[i] != "X" and self.board[i] != "O":  # Verifique se a célula está vazia
                    # Faça a jogada
                    self.board[i] = enemy_Symbol
                    self.total_moves += 1

                    # Chame minimax recursivamente e escolha o valor máximo
                    best = max(best, self.minimax(enemy_Symbol, player_Symbol, False, max_depth - 1))

                    # Desfaça a jogada
                    self.board[i] = i + 1
                    self.total_moves -= 1

            return best

        else:
            best = 10000  # Valor muito grande

            for i in range(9):  # Percorre todas as células
                if self.board[i] != "X" and self.board[i] != "O":  # Verifique se a célula está vazia
                    # Faça a jogada
                    self.board[i] = player_Symbol
                    self.total_moves += 1

                    # Chame minimax recursivamente e escolha o valor mínimo
                    best = min(best, self.minimax(enemy_Symbol, player_Symbol, True, max_depth - 1))

                    # Desfaça a jogada
                    self.board[i] = i + 1
                    self.total_moves -= 1

            return best

    def find_best_move(self, enemy_Symbol, player_Symbol):
        best_value = -10000  # Valor muito pequeno
        best_move = -1

        for i in range(9):  # Percorre todas as células
            if self.board[i] != "X" and self.board[i] != "O":  # Verifique se a célula está vazia
                # Faça a jogada
                self.board[i] = enemy_Symbol
                self.total_moves += 1

                # Avalie a jogada usando minimax
                move_value = self.minimax(enemy_Symbol, player_Symbol, False, 8)

                # Desfaça a jogada
                self.board[i] = i + 1
                self.total_moves -= 1

                # Se o valor da jogada atual for maior que o melhor valor, atualize o melhor valor e a melhor jogada
                if move_value > best_value:
                    best_move = i
                    best_value = move_value

        return best_move if best_move != -1 else 0

def jogar():
    Teste = TicTacToe()
    Teste.start_Game()

if __name__ == '__main__':
    jogar()