# Jogos Python - Projeto Refatorado

## Descrição do Software

O projeto **Jogos Python** é uma coletânea de jogos desenvolvidos em Python com o objetivo de demonstrar conceitos de programação, lógica computacional e boas práticas de engenharia de software, com foco na **refatoração e melhoria de código legado**.

O sistema reúne diferentes jogos interativos executados via terminal, organizados a partir de um menu central que permite ao usuário selecionar qual jogo deseja executar.

### Jogos Disponíveis

* Jogo da Velha
* Jogo da Forca
* Pong
* Snake

---

## Principais Funcionalidades

### Menu Central

Permite ao usuário selecionar e iniciar qualquer jogo disponível no sistema, funcionando como ponto de entrada da aplicação.

### Jogo da Velha

* Partida entre jogador e computador.
* Verificação automática de vitória ou empate.
* Validação de jogadas inválidas.

### Forca

* Seleção aleatória de palavras.
* Controle de tentativas.
* Representação da forca no terminal.

### Pong

* Controle do jogador via teclado.
* Movimentação automática do adversário.
* Sistema de pontuação.

### Snake

* Movimentação contínua da cobra.
* Crescimento progressivo.
* Geração aleatória de alimentos.
* Detecção de colisões.

---

## Principais Problemas Detectados (Code Smells)

### 1. Long Method

As funções `jogar()` apresentam tamanho excessivo e concentram múltiplas responsabilidades, como entrada de dados, lógica do jogo, renderização e controle de fluxo.

**Arquivos afetados:**

* `forca.py`
* `pong.py`
* `snake.py`

**Impactos:**

* Baixa legibilidade.
* Dificuldade de manutenção.
* Alta complexidade cognitiva.

---

### 2. Magic Numbers

Presença de valores literais espalhados pelo código sem significado contextual.

**Exemplos:**

* Dimensões de tela (`800`, `600`)
* Tamanho do grid (`20`)
* Velocidades (`9`)

**Impactos:**

* Redução da legibilidade.
* Dificuldade de ajustes globais.
* Maior risco de inconsistências.

---

### 3. Duplicate Code

Repetição de blocos de código em diferentes módulos, especialmente relacionados a:

* Menus e interfaces.
* Mensagens de erro.
* Validações de entrada.
* Reinicialização de jogos.

**Impactos:**

* Dificuldade de manutenção.
* Maior risco de inconsistências.
* Violação do princípio **DRY (Don't Repeat Yourself)**.

---

### 4. Poor Naming

Utilização de nomes de variáveis e funções pouco descritivos ou inconsistentes.

**Problemas encontrados:**

* Uso de nomes genéricos como `x`, `y`, `run` e `end`.
* Mistura de português e inglês no mesmo projeto.
* Ausência de padronização.

**Impactos:**

* Baixa clareza do código.
* Dificuldade de leitura e manutenção.
* Redução da colaboração entre desenvolvedores.

---

### 5. High Coupling

O módulo `menu.py` depende diretamente de todos os jogos por meio de importações explícitas.

```python
import forca
import pong
import snake
import jogo_velha
```

**Impactos:**

* Dificuldade para adicionar novos jogos.
* Necessidade de alterar o menu constantemente.
* Arquitetura pouco escalável.

---

### 6. Mixed Responsibilities (Violação do SRP)

Os arquivos dos jogos acumulam múltiplas responsabilidades, tais como:

* Interface com o usuário.
* Regras do jogo.
* Controle de estado.
* Renderização.
* Fluxo principal.

**Arquivos afetados:**

* `forca.py`
* `pong.py`
* `snake.py`

**Impactos:**

* Violação do princípio **Single Responsibility Principle (SRP)**.
* Código difícil de testar.
* Baixa modularidade.

---

## Estratégias de Refatoração Utilizadas

As refatorações foram baseadas nos princípios apresentados no livro **Clean Code**, de Robert C. Martin.

### Extração de Métodos

Funções extensas foram divididas em métodos menores e especializados.

**Exemplos:**

```python
processar_eventos()
atualizar_jogo()
desenhar_tela()
verificar_fim()
```

**Benefícios:**

* Melhor organização do código.
* Maior reutilização.
* Facilidade para testes unitários.

---

### Criação de Constantes

Substituição de valores fixos por constantes nomeadas.

```python
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
BALL_SPEED = 9
```

**Benefícios:**

* Facilidade de manutenção.
* Redução de erros.
* Melhor legibilidade.

---

### Padronização de Nomenclatura

Adoção do padrão recomendado pela **PEP 8**, utilizando nomes consistentes e preferencialmente em inglês.

**Exemplos:**

```python
letras_usadas -> used_letters
hidden -> hidden_word
win -> game_over
```

**Benefícios:**

* Consistência no código.
* Melhor compreensão.
* Facilidade de colaboração.

---

### Modularização

Reorganização da estrutura do projeto em módulos específicos.

```text
games/
├── core/
├── forca/
├── snake/
├── pong/
└── tic_tac_toe/
```

**Benefícios:**

* Redução do acoplamento.
* Melhor organização estrutural.
* Maior escalabilidade.

---

### Inversão de Dependência no Menu

Substituição de chamadas diretas por um registro centralizado de jogos.

```python
JOGOS = {
    1: jogo_velha.jogar,
    2: forca.jogar,
    3: pong.jogar,
    4: snake.jogar
}
```

**Benefícios:**

* Facilidade para adicionar novos jogos.
* Redução do acoplamento.
* Arquitetura mais flexível.

---

### Organização de Imports

Reestruturação dos imports conforme as recomendações da **PEP 8**.

**Benefícios:**

* Código mais organizado.
* Melhor previsibilidade.
* Padronização estrutural.

---

## Resultados Esperados

Com as refatorações aplicadas, o projeto passa a apresentar:

* Maior legibilidade.
* Melhor organização arquitetural.
* Redução do acoplamento entre módulos.
* Maior reutilização de código.
* Melhor aderência aos princípios de Clean Code.
* Facilidade de manutenção e evolução futura.


## Padronização e Estilização de Código

Como parte do processo de refatoração, foi aplicada uma ferramenta de análise estática para garantir conformidade com as boas práticas recomendadas pela comunidade Python.

### Ferramentas Utilizadas

* Flake8
* Black
* isort

### Objetivos

* Padronizar a formatação do código.
* Identificar problemas de estilo.
* Detectar variáveis não utilizadas.
* Verificar inconsistências de nomenclatura.
* Melhorar a legibilidade e manutenibilidade.

### Benefícios Obtidos

* Maior aderência à PEP 8.
* Código mais consistente.
* Redução de problemas de manutenção.
* Melhor organização dos imports e estruturas do projeto.
