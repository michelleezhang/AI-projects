# Game Engine
Konane (Hawaiian Checkers) is a strategy game played between two players. Players alternate taking turns, capturing their opponent's pieces by jumping their own pieces over them. The first player to be unable to capture any of their opponent's pieces loses.

Here, we implement two agents playing Konane -- one uses minimax (without alpha-beta pruning) and the other uses minimax with alpha-beta pruning.

### Minimax
Minimax is an algorithm for determing the best move in an adverserial game. It seeks to minimize the maximum loss posed by the opponent’s strategy. Minimax is typically employed in competitive, discrete-, and finite-space games with abstracted time and perfect information.

The implementation of `MinimaxPlayer` is in `player.py`.  
The maximum depth function is provided to the constructor of the `MinimaxPlayer` and defines the maximum number of plies that the player will simulate when choosing a move.  The evaluation function defines a score for a terminal node in the search.  Use the function `h1` defined in the parent class `Player` as your evaluation function.

Note: Minimax starts to get very slow when max search depth values are above ~4 -- the total number of nodes in the gamme tree is the branching factor to the power of the search depth.

### Alpha-Beta Pruning

Miniimax with alpha-beta pruning iis essentially the same algorithm, but it _ignores_ subtrees that are provably worse than any that it has considered so far. This drastically reduces the runtime
of the algorithm.\* 

\* Strictly speaking, it doesn't change the upper bound on the algorithm's runtime, since in the worst-case one must still search the entire tree. In practice, however, the performance difference is very noticeable.

# works best with Python 3.6-3.7

## Notes
* `player.py` — where `MinimaxPlayer` and `AlphaBetaPlayer` are implemented
* `main.py` — to play the game (in Human mode) or to watch your agents duke it out, run `python main.py`. Use the arrow 
keys and the spacebar to select your actions.
* `test.py` — run tests with `python test.py`.
* `game_manager.py` — holds the board representation and handles turn-taking.
* `game_rules.py` — code determining available moves, their legality, etc.
* You can change the type of player, the board size, etc. in `main.py`