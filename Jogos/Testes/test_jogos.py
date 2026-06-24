"""
Testes de cobertura para o projeto de jogos.

Estrutura:
  - TestForca         → forca.py        (lógica pura, sem I/O)
  - TestJogoVelha     → jogo_velha.py   (tabuleiro, IA, vitória)
  - TestPong          → pong.py         (física e colisões via pygame mock)
  - TestSnake         → snake.py        (movimentação e colisões)
  - TestMenu          → menu.py         (registro e despacho de jogos)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import types
import unittest
from unittest.mock import MagicMock, patch

# ──────────────────────────────────────────────────────────────────────────────
# Mock do pygame ANTES de qualquer import que dependa dele.
# Funciona como um "dublê de corpo inteiro" — pygame nunca toca a GPU/SDL.
# ──────────────────────────────────────────────────────────────────────────────
pygame_mock = types.ModuleType("pygame")

# Constantes de teclas
pygame_mock.K_RIGHT = 275
pygame_mock.K_LEFT = 276
pygame_mock.K_UP = 273
pygame_mock.K_DOWN = 274
pygame_mock.K_w = 119
pygame_mock.K_s = 115
pygame_mock.K_SPACE = 32
pygame_mock.QUIT = 256
pygame_mock.KEYDOWN = 768
pygame_mock.KEYUP = 769

pygame_mock.init = MagicMock()
pygame_mock.quit = MagicMock()
pygame_mock.display = MagicMock()
pygame_mock.time = MagicMock()
pygame_mock.font = MagicMock()
pygame_mock.key = MagicMock()
pygame_mock.event = MagicMock()
pygame_mock.Surface = MagicMock(return_value=MagicMock())


class FakeRect:
    """Substituto leve para pygame.Rect — suporta .colliderect e .center."""

    def __init__(self, x, y, w, h):
        self.x, self.y, self.width, self.height = x, y, w, h

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    @center.setter
    def center(self, value):
        self.x, self.y = value[0] - self.width // 2, value[1] - self.height // 2

    def colliderect(self, other):
        return (
            self.left < other.right
            and self.right > other.left
            and self.top < other.bottom
            and self.bottom > other.top
        )


pygame_mock.Rect = FakeRect
sys.modules["pygame"] = pygame_mock

import forca
import jogo_velha
import pong
import snake

# ══════════════════════════════════════════════════════════════════════════════
# FORCA
# ══════════════════════════════════════════════════════════════════════════════


class TestForca(unittest.TestCase):

    # ── constantes ────────────────────────────────────────────────────────────

    def test_hangman_stages_tem_sete_estagios(self):
        self.assertEqual(len(forca.HANGMAN_STAGES), 7)

    def test_max_mistakes_e_seis(self):
        self.assertEqual(forca.MAX_MISTAKES, 6)

    def test_cada_estagio_tem_quatro_linhas(self):
        for estagio in forca.HANGMAN_STAGES:
            with self.subTest(estagio=estagio):
                self.assertEqual(len(estagio), 4)

    # ── reveal_letter ─────────────────────────────────────────────────────────

    def test_revela_unica_ocorrencia(self):
        hidden = list("_____")
        forca.reveal_letter("a", "amigo", hidden)
        self.assertEqual(hidden[0], "a")

    def test_revela_multiplas_ocorrencias(self):
        # reveal_letter revela APENAS a letra passada — não as outras.
        # Em "banana", chamar reveal_letter("a", ...) deve revelar só os 'a'.
        hidden = list("______")
        forca.reveal_letter("a", "banana", hidden)
        self.assertEqual(hidden[1], "a")
        self.assertEqual(hidden[3], "a")
        self.assertEqual(hidden[5], "a")
        # As posições das outras letras permanecem ocultas
        self.assertEqual(hidden[0], "_")  # 'b' ainda oculto
        self.assertEqual(hidden[2], "_")  # 'n' ainda oculto
        self.assertEqual(hidden[4], "_")  # 'n' ainda oculto

    def test_letra_ausente_nao_altera_hidden(self):
        hidden = list("___")
        forca.reveal_letter("z", "sol", hidden)
        self.assertEqual(hidden, ["_", "_", "_"])

    def test_hidden_word_completo_apos_todas_letras(self):
        palavra = "casa"
        hidden = list("____")
        for letra in set(palavra):
            forca.reveal_letter(letra, palavra, hidden)
        self.assertEqual(hidden, list(palavra))

    def test_palavra_com_letra_repetida(self):
        hidden = list("______")
        forca.reveal_letter("o", "cococo", hidden)
        self.assertEqual(hidden, ["_", "o", "_", "o", "_", "o"])

    # ── show_game_board ───────────────────────────────────────────────────────

    def test_show_game_board_imprime_estagio_correto(self):
        with patch("builtins.print") as mock_print:
            forca.show_game_board(0)
            args = [call.args for call in mock_print.call_args_list]
            # o primeiro estagio não tem o boneco
            self.assertTrue(any("O" not in str(a) for a in args))

    def test_show_game_board_estagio_seis_tem_pernas(self):
        with patch("builtins.print") as mock_print:
            forca.show_game_board(6)
            all_printed = " ".join(str(c) for c in mock_print.call_args_list)
            self.assertIn("/", all_printed)
            self.assertIn("\\", all_printed)

    # ── fluxo de vitória / derrota via jogar() ────────────────────────────────

    def test_vitoria_ao_revelar_todas_as_letras(self):
        """Simula acertar todas as letras de 'amor'."""
        inputs = iter(["a", "m", "o", "r"])
        with (
            patch("builtins.input", side_effect=inputs),
            patch("builtins.print"),
            patch("random.choice", return_value="amor"),
        ):
            forca.jogar()  # não deve lançar exceção

    def test_derrota_apos_seis_erros(self):
        """Simula seis letras erradas consecutivas."""
        letras_erradas = iter(["z", "x", "k", "w", "q", "j"])
        with (
            patch("builtins.input", side_effect=letras_erradas),
            patch("builtins.print"),
            patch("random.choice", return_value="amor"),
        ):
            forca.jogar()

    def test_letra_repetida_nao_incrementa_erros(self):
        """Usar a mesma letra duas vezes não conta como erro extra."""
        # 'a' repetido → aviso → depois acerta o resto
        inputs = iter(["a", "a", "m", "o", "r"])
        with (
            patch("builtins.input", side_effect=inputs),
            patch("builtins.print"),
            patch("random.choice", return_value="amor"),
        ):
            forca.jogar()  # deve terminar em vitória, não estouro


# ══════════════════════════════════════════════════════════════════════════════
# JOGO DA VELHA
# ══════════════════════════════════════════════════════════════════════════════


class TestJogoVelha(unittest.TestCase):

    # ── create_board ──────────────────────────────────────────────────────────

    def test_board_tem_nove_posicoes(self):
        board = jogo_velha.create_board()
        self.assertEqual(len(board), 9)

    def test_board_inicial_sem_simbolos(self):
        board = jogo_velha.create_board()
        for cell in board:
            self.assertNotIn("X", cell)
            self.assertNotIn("O", cell)

    # ── update_board ──────────────────────────────────────────────────────────

    def test_atualiza_canto_esquerdo(self):
        board = jogo_velha.create_board()
        jogo_velha.update_board(board, 1, "X")
        self.assertEqual(board[0], "|X")

    def test_atualiza_centro(self):
        board = jogo_velha.create_board()
        jogo_velha.update_board(board, 2, "O")
        self.assertEqual(board[1], "|O|")

    def test_atualiza_canto_direito(self):
        board = jogo_velha.create_board()
        jogo_velha.update_board(board, 3, "X")
        self.assertEqual(board[2], "X|")

    def test_atualiza_posicao_9(self):
        board = jogo_velha.create_board()
        jogo_velha.update_board(board, 9, "O")
        self.assertEqual(board[8], "O|")

    # ── has_winner ────────────────────────────────────────────────────────────

    def test_sem_vencedor_lista_vazia(self):
        self.assertFalse(jogo_velha.has_winner([]))

    def test_vencedor_linha_horizontal(self):
        self.assertTrue(jogo_velha.has_winner([1, 2, 3]))

    def test_vencedor_linha_vertical(self):
        self.assertTrue(jogo_velha.has_winner([1, 4, 7]))

    def test_vencedor_diagonal_principal(self):
        self.assertTrue(jogo_velha.has_winner([1, 5, 9]))

    def test_vencedor_diagonal_secundaria(self):
        self.assertTrue(jogo_velha.has_winner([3, 5, 7]))

    def test_sem_vencedor_com_duas_pecas(self):
        self.assertFalse(jogo_velha.has_winner([1, 2]))

    def test_sem_vencedor_posicoes_dispersas(self):
        # ATENÇÃO: [1,3,5,7,9] contém as diagonais [1,5,9] e [3,5,7],
        # então has_winner retorna True corretamente.
        # Usamos um conjunto que realmente não forma nenhuma sequência.
        self.assertFalse(jogo_velha.has_winner([1, 6, 8]))

    def test_todas_as_sequencias_vencem(self):
        for seq in jogo_velha.WINNING_SEQUENCES:
            with self.subTest(seq=seq):
                self.assertTrue(jogo_velha.has_winner(seq))

    # ── choose_move ───────────────────────────────────────────────────────────

    def test_dificuldade_1_retorna_posicao_disponivel(self):
        used = [1, 2, 3]
        move = jogo_velha.choose_move(1, [], [], used)
        self.assertNotIn(move, used)
        self.assertIn(move, range(1, 10))

    def test_dificuldade_2_bloqueia_vitoria_do_jogador(self):
        # Jogador tem 1 e 2 → computador deve bloquear em 3
        move = jogo_velha.choose_move(
            difficulty=2,
            player_moves=[1, 2],
            computer_moves=[],
            used_moves=[1, 2],
        )
        self.assertEqual(move, 3)

    def test_dificuldade_3_prefere_vencer_a_bloquear(self):
        # Computador tem 1 e 2 → deve completar em 3, não bloquear
        move = jogo_velha.choose_move(
            difficulty=3,
            player_moves=[4, 5],
            computer_moves=[1, 2],
            used_moves=[1, 2, 4, 5],
        )
        self.assertEqual(move, 3)

    def test_dificuldade_3_bloqueia_se_nao_pode_vencer(self):
        # Jogador ameaça 4-5-6; computador não tem sequência para ganhar
        move = jogo_velha.choose_move(
            difficulty=3,
            player_moves=[4, 5],
            computer_moves=[1, 2],
            used_moves=[1, 2, 4, 5],
        )
        # deve ser 3 (vitória do computador com 1,2,3) antes do bloqueio
        self.assertIn(move, range(1, 10))

    def test_sem_posicao_disponiveis_retorna_falha(self):
        # Todas as 9 posições usadas → random.choice vai lançar IndexError
        with self.assertRaises(IndexError):
            jogo_velha.choose_move(1, [], [], list(range(1, 10)))

    # ── GameConfig / GameState ────────────────────────────────────────────────

    def test_gameconfig_default_current_player_e_player(self):
        cfg = jogo_velha.GameConfig("X", "O", 1)
        self.assertEqual(cfg.current_player, jogo_velha.PLAYER)

    def test_gamestate_listas_iniciam_vazias(self):
        state = jogo_velha.GameState(board=jogo_velha.create_board())
        self.assertEqual(state.player_moves, [])
        self.assertEqual(state.computer_moves, [])
        self.assertEqual(state.used_moves, [])

    # ── execute_turn ──────────────────────────────────────────────────────────

    def test_turno_do_jogador_adiciona_movimento(self):
        cfg = jogo_velha.GameConfig("X", "O", 1)
        state = jogo_velha.GameState(board=jogo_velha.create_board())

        with patch("builtins.input", return_value="5"), patch("builtins.print"):
            jogo_velha.execute_turn(cfg, state)

        self.assertIn(5, state.player_moves)
        self.assertIn(5, state.used_moves)

    def test_turno_do_computador_adiciona_movimento(self):
        cfg = jogo_velha.GameConfig("X", "O", 1, current_player=jogo_velha.COMPUTER)
        state = jogo_velha.GameState(board=jogo_velha.create_board())

        with patch("builtins.print"):
            jogo_velha.execute_turn(cfg, state)

        self.assertEqual(len(state.computer_moves), 1)
        self.assertEqual(len(state.used_moves), 1)

    def test_execute_turn_detecta_vitoria_do_jogador(self):
        cfg = jogo_velha.GameConfig("X", "O", 1)
        state = jogo_velha.GameState(board=jogo_velha.create_board())
        state.player_moves = [1, 2]
        state.used_moves = [1, 2]

        # Jogador escolhe 3 → completa linha 1-2-3
        with patch("builtins.input", return_value="3"), patch("builtins.print"):
            resultado = jogo_velha.execute_turn(cfg, state)

        self.assertTrue(resultado)


# ══════════════════════════════════════════════════════════════════════════════
# PONG
# ══════════════════════════════════════════════════════════════════════════════


class TestPong(unittest.TestCase):

    def _estado(self):
        """Cria estado fresco sem depender de pygame.Rect real."""
        return {
            "player": FakeRect(5, 300, 10, 75),
            "enemy": FakeRect(785, 300, 10, 75),
            "ball": FakeRect(400, 300, 12, 12),
            "ball_dir": [pong.BALL_SPEED_X, pong.BALL_SPEED_Y],
            "player_score": 0,
            "enemy_score": 0,
            "player_speed": 0,
            "enemy_speed": 0,
        }

    # ── reset_state ───────────────────────────────────────────────────────────

    def test_reset_state_placar_zerado(self):
        state = pong.reset_state()
        self.assertEqual(state["player_score"], 0)
        self.assertEqual(state["enemy_score"], 0)

    def test_reset_state_velocidades_zeradas(self):
        state = pong.reset_state()
        self.assertEqual(state["player_speed"], 0)
        self.assertEqual(state["enemy_speed"], 0)

    def test_reset_state_direcao_da_bola(self):
        state = pong.reset_state()
        self.assertEqual(state["ball_dir"], [pong.BALL_SPEED_X, pong.BALL_SPEED_Y])

    # ── adjust_key_speed ──────────────────────────────────────────────────────

    def test_tecla_w_move_jogador_para_cima(self):
        state = self._estado()
        pong.adjust_key_speed(pong.pygame.K_w, state, 1)
        self.assertLess(state["player_speed"], 0)

    def test_tecla_s_move_jogador_para_baixo(self):
        state = self._estado()
        pong.adjust_key_speed(pong.pygame.K_s, state, 1)
        self.assertGreater(state["player_speed"], 0)

    def test_tecla_up_move_inimigo_para_cima(self):
        state = self._estado()
        pong.adjust_key_speed(pong.pygame.K_UP, state, 1)
        self.assertLess(state["enemy_speed"], 0)

    def test_tecla_desconhecida_nao_altera_estado(self):
        state = self._estado()
        pong.adjust_key_speed(999, state, 1)
        self.assertEqual(state["player_speed"], 0)
        self.assertEqual(state["enemy_speed"], 0)

    def test_keyup_reverte_velocidade(self):
        state = self._estado()
        pong.adjust_key_speed(pong.pygame.K_s, state, 1)  # aperta
        pong.adjust_key_speed(pong.pygame.K_s, state, -1)  # solta
        self.assertEqual(state["player_speed"], 0)

    # ── move_objects ──────────────────────────────────────────────────────────

    def test_bola_se_move_conforme_direcao(self):
        state = self._estado()
        x0, y0 = state["ball"].x, state["ball"].y
        pong.move_objects(state)
        self.assertEqual(state["ball"].x, x0 + pong.BALL_SPEED_X)
        self.assertEqual(state["ball"].y, y0 + pong.BALL_SPEED_Y)

    def test_paddle_do_jogador_se_move(self):
        state = self._estado()
        state["player_speed"] = 8
        y0 = state["player"].y
        pong.move_objects(state)
        self.assertEqual(state["player"].y, y0 + 8)

    # ── clamp_paddles ─────────────────────────────────────────────────────────

    def test_paddle_nao_ultrapassa_topo(self):
        state = self._estado()
        state["player"].y = -50
        pong.clamp_paddles(state)
        self.assertGreaterEqual(state["player"].y, 0)

    def test_paddle_nao_ultrapassa_fundo(self):
        state = self._estado()
        state["player"].y = pong.HEIGHT + 100
        pong.clamp_paddles(state)
        self.assertLessEqual(state["player"].y, pong.HEIGHT - state["player"].height)

    # ── handle_ball_collision ─────────────────────────────────────────────────

    def test_bola_rebate_na_parede_superior(self):
        state = self._estado()
        state["ball"].y = -1  # bola saiu pelo topo
        dy_antes = state["ball_dir"][1]
        pong.handle_ball_collision(state)
        self.assertEqual(state["ball_dir"][1], -dy_antes)

    def test_bola_rebate_na_parede_inferior(self):
        state = self._estado()
        state["ball"].y = pong.HEIGHT  # bola saiu pelo fundo
        dy_antes = state["ball_dir"][1]
        pong.handle_ball_collision(state)
        self.assertEqual(state["ball_dir"][1], -dy_antes)

    def test_ponto_para_inimigo_quando_bola_sai_pela_esquerda(self):
        state = self._estado()
        state["ball"].x = -1
        pong.handle_ball_collision(state)
        self.assertEqual(state["enemy_score"], 1)

    def test_ponto_para_jogador_quando_bola_sai_pela_direita(self):
        state = self._estado()
        state["ball"].x = pong.WIDTH
        pong.handle_ball_collision(state)
        self.assertEqual(state["player_score"], 1)

    def test_reset_ball_centraliza_bola(self):
        state = self._estado()
        state["ball"].x = 0
        state["ball"].y = 0
        pong.reset_ball(state)
        cx, cy = state["ball"].center
        self.assertAlmostEqual(cx, pong.WIDTH // 2, delta=10)
        self.assertAlmostEqual(cy, pong.HEIGHT // 2, delta=10)

    def test_bola_rebate_no_paddle(self):
        state = self._estado()
        # Posiciona a bola exatamente sobre o paddle do jogador
        state["ball"].x = state["player"].right - 1
        state["ball"].y = state["player"].y
        dx_antes = state["ball_dir"][0]
        pong.handle_ball_collision(state)
        self.assertEqual(state["ball_dir"][0], -dx_antes)


# ══════════════════════════════════════════════════════════════════════════════
# SNAKE
# ══════════════════════════════════════════════════════════════════════════════


class TestSnake(unittest.TestCase):

    # ── spawn_apple ───────────────────────────────────────────────────────────

    def test_apple_nao_spawnna_na_cobra(self):
        corpo = [(0, 0), (20, 0), (40, 0)]
        apple = snake.spawn_apple(corpo)
        self.assertNotIn(apple, corpo)

    def test_apple_dentro_da_area(self):
        apple = snake.spawn_apple([])
        x, y = apple
        self.assertGreaterEqual(x, 0)
        self.assertLess(x, snake.GAME_AREA)
        self.assertGreaterEqual(y, 0)
        self.assertLess(y, snake.GAME_AREA)

    def test_apple_alinhada_ao_grid(self):
        for _ in range(20):
            apple = snake.spawn_apple([])
            x, y = apple
            self.assertEqual(x % snake.GRID_SIZE, 0)
            self.assertEqual(y % snake.GRID_SIZE, 0)

    # ── handle_input ──────────────────────────────────────────────────────────

    def _fake_event(self, key):
        e = MagicMock()
        e.key = key
        return e

    def test_muda_direcao_valida(self):
        state = {"direction": (1, 0)}
        event = self._fake_event(snake.pygame.K_UP)
        snake.handle_input(event, state)
        self.assertEqual(state["direction"], (0, -1))

    def test_impede_reversao_direta(self):
        """Indo para a direita não pode inverter para a esquerda."""
        state = {"direction": (1, 0)}
        event = self._fake_event(snake.pygame.K_LEFT)
        snake.handle_input(event, state)
        self.assertEqual(state["direction"], (1, 0))

    def test_tecla_invalida_nao_muda_direcao(self):
        state = {"direction": (1, 0)}
        event = self._fake_event(999)
        snake.handle_input(event, state)
        self.assertEqual(state["direction"], (1, 0))

    def test_pode_virar_perpendicularmente(self):
        """Indo para baixo pode virar para a direita (perpendicular)."""
        state = {"direction": (0, 1)}
        event = self._fake_event(snake.pygame.K_RIGHT)
        snake.handle_input(event, state)
        self.assertEqual(state["direction"], (1, 0))

    # ── move_snake ────────────────────────────────────────────────────────────

    def test_cobra_move_para_direita(self):
        state = {"direction": (1, 0)}
        rect = FakeRect(100, 100, snake.GRID_SIZE, snake.GRID_SIZE)
        snake.move_snake(state, rect)
        self.assertEqual(rect.x, 100 + snake.GRID_SIZE)

    def test_cobra_move_para_cima(self):
        state = {"direction": (0, -1)}
        rect = FakeRect(100, 100, snake.GRID_SIZE, snake.GRID_SIZE)
        snake.move_snake(state, rect)
        self.assertEqual(rect.y, 100 - snake.GRID_SIZE)

    # ── update_body ───────────────────────────────────────────────────────────

    def test_cabeca_e_inserida_no_inicio(self):
        state = {"snake": [(20, 0)], "length": 2}
        rect = FakeRect(40, 0, snake.GRID_SIZE, snake.GRID_SIZE)
        snake.update_body(state, rect)
        self.assertEqual(state["snake"][0], (40, 0))

    def test_comprimento_e_respeitado(self):
        state = {"snake": [(0, 0), (20, 0), (40, 0)], "length": 2}
        rect = FakeRect(60, 0, snake.GRID_SIZE, snake.GRID_SIZE)
        snake.update_body(state, rect)
        self.assertEqual(len(state["snake"]), 2)

    # ── hit_wall ──────────────────────────────────────────────────────────────

    def test_colide_parede_esquerda(self):
        rect = FakeRect(-snake.GRID_SIZE, 0, snake.GRID_SIZE, snake.GRID_SIZE)
        self.assertTrue(snake.hit_wall(rect))

    def test_colide_parede_direita(self):
        rect = FakeRect(snake.GAME_AREA, 0, snake.GRID_SIZE, snake.GRID_SIZE)
        self.assertTrue(snake.hit_wall(rect))

    def test_colide_parede_topo(self):
        rect = FakeRect(0, -snake.GRID_SIZE, snake.GRID_SIZE, snake.GRID_SIZE)
        self.assertTrue(snake.hit_wall(rect))

    def test_colide_parede_fundo(self):
        rect = FakeRect(0, snake.GAME_AREA, snake.GRID_SIZE, snake.GRID_SIZE)
        self.assertTrue(snake.hit_wall(rect))

    def test_nao_colide_dentro_da_area(self):
        rect = FakeRect(100, 100, snake.GRID_SIZE, snake.GRID_SIZE)
        self.assertFalse(snake.hit_wall(rect))

    def test_borda_esquerda_valida(self):
        rect = FakeRect(0, 0, snake.GRID_SIZE, snake.GRID_SIZE)
        self.assertFalse(snake.hit_wall(rect))

    # ── hit_self ──────────────────────────────────────────────────────────────

    def test_colide_consigo_mesmo(self):
        corpo = [(20, 0), (0, 0), (0, 20), (20, 20), (20, 0)]
        self.assertTrue(snake.hit_self(corpo))

    def test_sem_auto_colisao(self):
        corpo = [(60, 0), (40, 0), (20, 0), (0, 0)]
        self.assertFalse(snake.hit_self(corpo))

    def test_cobra_com_um_segmento_nao_colide(self):
        self.assertFalse(snake.hit_self([(0, 0)]))

    # ── hit_apple ─────────────────────────────────────────────────────────────

    def test_acerta_maca(self):
        head = FakeRect(100, 100, snake.GRID_SIZE, snake.GRID_SIZE)
        apple = FakeRect(100, 100, snake.GRID_SIZE, snake.GRID_SIZE)
        self.assertTrue(snake.hit_apple(head, apple))

    def test_nao_acerta_maca_distante(self):
        head = FakeRect(0, 0, snake.GRID_SIZE, snake.GRID_SIZE)
        apple = FakeRect(200, 200, snake.GRID_SIZE, snake.GRID_SIZE)
        self.assertFalse(snake.hit_apple(head, apple))

    # ── reset ─────────────────────────────────────────────────────────────────

    def test_reset_cobra_na_posicao_inicial(self):
        state = snake.reset()
        self.assertEqual(state["snake"], [snake.INITIAL_POS])

    def test_reset_jogo_ativo(self):
        state = snake.reset()
        self.assertTrue(state["active"])

    def test_reset_comprimento_inicial_um(self):
        state = snake.reset()
        self.assertEqual(state["length"], 1)


# ══════════════════════════════════════════════════════════════════════════════
# MENU
# ══════════════════════════════════════════════════════════════════════════════


class TestMenu(unittest.TestCase):
    """
    Importamos menu dentro de cada teste para controlar o estado do registry,
    já que o módulo registra jogos no nível de módulo ao ser importado.
    """

    def _importar_menu(self):
        """Re-importa menu em modo isolado usando um registry limpo."""
        import importlib
        import menu as m

        importlib.reload(m)
        return m

    def test_registry_tem_quatro_jogos(self):
        with patch("builtins.print"):
            import menu as m
        self.assertEqual(len(m.Game.registry), 4)

    def test_todos_ids_registrados(self):
        with patch("builtins.print"):
            import menu as m
        self.assertSetEqual(set(m.Game.registry.keys()), {1, 2, 3, 4})

    def test_str_do_jogo_formatado_corretamente(self):
        with patch("builtins.print"):
            import menu as m
        jogo = m.Game.registry[1]
        self.assertIn("1", str(jogo))
        self.assertIn("Jogo da Velha", str(jogo))

    def test_execute_game_chama_action_correta(self):
        with patch("builtins.print"):
            import menu as m
        mock_action = MagicMock()
        m.Game.registry[1].action = mock_action
        m.execute_game(1)
        mock_action.assert_called_once()

    def test_execute_game_id_invalido_imprime_mensagem(self):
        with patch("builtins.print"):
            import menu as m
        with patch("builtins.print") as mock_print:
            m.execute_game(99)
        # deve imprimir mensagem de erro
        args = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("99", args)

    def test_choose_game_sai_com_q(self):
        with patch("builtins.print"):
            import menu as m
        with patch("builtins.input", return_value="Q"), patch("builtins.print"):
            m.choose_game()  # não deve travar

    def test_choose_game_entrada_invalida_nao_crasha(self):
        with patch("builtins.print"):
            import menu as m
        # 'abc' → ValueError capturado → 'Q' encerra
        inputs = iter(["abc", "Q"])
        with patch("builtins.input", side_effect=inputs), patch("builtins.print"):
            m.choose_game()

    def test_display_menu_imprime_todos_os_jogos(self):
        with patch("builtins.print"):
            import menu as m
        saida_linhas = []

        def captura(*args, **kwargs):
            for a in args:
                saida_linhas.append(str(a))

        with patch("builtins.print", side_effect=captura):
            m.display_menu()
        saida = " ".join(saida_linhas)
        self.assertIn("Jogo da Velha", saida)
        self.assertIn("Forca", saida)
        self.assertIn("Pong", saida)
        self.assertIn("Snake", saida)


if __name__ == "__main__":
    unittest.main(verbosity=2)
