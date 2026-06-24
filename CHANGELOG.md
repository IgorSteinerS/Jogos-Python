# Changelog

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

---

## [1.3.0] - 2026-06-24

### Refatorado
- Refatoração do jogo da Forca com foco em separação de responsabilidades e legibilidade.
  - Estágios do enforcado extraídos para a constante `HANGMAN_STAGES`.
  - Lista de palavras movida para a constante `PORTUGUESE_WORDS`, fora do loop de jogo.
  - Limite de erros definido dinamicamente via constante `MAX_MISTAKES`.
  - Lógica de revelar letras isolada na função `reveal_letter()`.
  - Lógica de exibição do tabuleiro isolada na função `show_game_board()`.
  - Verificação de vitória simplificada: `"_" not in hidden` substitui o contador `win`.
  - `random.randrange()` substituído por `random.choice()`.
  - Entrada do jogador normalizada com `.lower().strip()`.
  - Anotações de tipo adicionadas (`list[str]`, `-> None`).

### Removido
- Loop externo de "jogar de novo" (`while jogar == True`) e variáveis associadas (`enforcado`, `win`, `novamente`, `jogar`).
- Função interna `end()` embutida dentro de `jogar()`.
- Recriação desnecessária da lista de palavras a cada iteração do loop.
- Incremento de erro ao usar letra já utilizada — substituído por `continue` com mensagem ao jogador.

---

## [1.2.0] - 2026-06-23

### Adicionado
- Integração de linters para melhoria da qualidade de código.
- Padronização adicional no README do projeto.

### Removido
- Algoritmo Minimax do Jogo da Velha.

### Refatorado
- Refatoração do Jogo da Velha com foco em legibilidade e separação de responsabilidades.
- Refatoração do Menu principal para reduzir acoplamento e melhorar extensibilidade.
- Refatoração de Pong para reduzir IFs e centralizar lógica de controles.
- Reestruturação da lógica de movimento utilizando vetores no Snake.
- Simplificação do controle de direção no Pong por meio de mapeamento de ações.

---

## [1.1.0] - 2026-06-22

### Refatorado
- Reorganização da estrutura do projeto.
- Padronização de nomenclatura de variáveis e funções.
- Melhoria da legibilidade do código.

### Adicionado
- Documentação do projeto.
- Branch `original` para preservação da versão inicial.
- Melhorias na organização dos arquivos.

### Corrigido
- Correção de trechos de código redundantes.
- Ajustes em validações e tratamento de erros.

---

## [1.0.0] - 2026-06-22

### Inicial
- Versão original do projeto recebida.
- Jogos desenvolvidos em Python.