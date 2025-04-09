# <font size="80">Wood Block</font>
*******
Trabalho realizado por:

* Ana Isaura Silva (FCUP_IACD:202406221)
* Bárbara Castanho (FCUP_IACD:202406023) 
* Maria da Luz Fiolhais (FCUP_IACD:202405130)
  
<div style="padding: 10px;padding-left:5%">
<img src="fotos/Cienciasporto.png" style="float:left; height:75px;width:200px">
<img src="fotos/Feuporto.png" style="float:left ; height:75px; padding-left:20px;width:200px">
</div>

<div style="clear:both;"></div>

******
### A CERCA DO PROJETO 
No segundo semestre do primeiro ano da Licenciatura em Inteligência Artificial e Ciência de Dados, na Faculdade de Ciências da Universidade do Porto, fomos desafiados a desenvolver uma Inteligência Artificial capaz de jogar jogos-puzzle, neste caso, um jogo para um jogador. O objetivo deste projeto passa por explorar algoritmos de busca informada, nomeadamente A* e Greedy Search, bem como algoritmos de busca não informada, tal como BFS e DFS. Estes métodos são aplicados com diferentes configurações e níveis de profundidade, sendo avaliados em função do seu desempenho em diferentes niveis de dificuldade e tipos de jogo.

## 🎮 Regras e funcionamento do jogo:
   - O objetivo é completar linhas e colunas no tabuleiro;
   - O jogador tem 3 peças disponíveis para colocar no tabuleiro;
   - Quando uma peça é colocada, uma nova é gerada;
   - Ao completar uma linha ou coluna, ela é eliminada;
   - O jogo termina quando nenhuma das 3 peças disponíveis couber nos espaços vazios do tabuleiro.
     
Woodblock Puzzle é um jogo de estratégia inspirado em clássicos como Tetris e Blokus, onde o objetivo é posicionar peças geométricas em um tabuleiro para completar linhas e colunas. Com mecânicas simples mas desafiadoras, o jogo testa o planejamento espacial do jogador enquanto procura obter a maior pontuação possível. A sua versão digital traz algoritmos de IA, múltiplas dificuldades e um design clean com temática de madeira.

### 🧠 Modos de Jogo

  **👤 Humano:** 
  **A\* (A-Star):** .
  **Greedy Search:** 
  **BFS (Busca em Largura):**
  **DFS (Busca em Profundidade):** 
  **Estabilidade Dinâmica:** heurística original
  **Heurística da Cascata:** heurística original
  
O modo de jogo é escolhido posteriormente à escolha do tamanho do tabuleiro: 5 por 5 ou 10 por 10; e da dificuldade: fácil, média ou difícil; pela ordem descrita.

## Como fazer o download e utilizar a interface 

## 🛠️ Requisitos do Sistema

- **Python:** 3.8 ou superior  
- **Pygame:** 2.1.0 ou superior
  
#### Primeiro passo:
Extraia o .zip da página github ou diretamente do moodle e descomprima o ficheiro

#### Segundo passo: 
Instale `numpy` no diretório pelo terminal 
```
pip install numpy
```
#### Terceiro passo: **IMPORTANTE** 
Entre no diretório do ficheiro woodblock_puzzle.py pelo terminal
```
cd (diretório da pasta)
```
#### Quarto passo 
Corra o programa 
```
python3 woodblock_puzzle.py
```
*****
