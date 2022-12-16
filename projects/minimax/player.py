from cmath import inf
from contextlib import nullcontext
from shutil import move
from telnetlib import theNULL
import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if symbol == 'x' else 'x'))


class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): 
        super(MinimaxPlayer, self).__init__(symbol) 
        self.depth = depth #ADDED: depth feature

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]
    
    # minimax code
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)   #get legal moves
        if len(legalMoves) == None or self.depth == 0:
            return None
        #if no legal moves, return None -> we have no moves available
        elif len(legalMoves) == 1:
             return legalMoves[0]
        #if only one choice of legal move, automatically return that move

        def reverseplayer(player):
            #reverses player
            if player == 'x':
                return 'o'
            elif player =='o':
                return 'x'
            else:
                return None

        def max_value(currboard, depth, player):
            possibleMoves = game_rules.getLegalMoves(currboard, player) 
            if depth == 0 or len(possibleMoves) == 0:
                return self.h1(currboard, self.symbol), None
            
            maxEval = NEG_INF
            best_move = None
            for move in possibleMoves:
                newboard = game_rules.makeMove(currboard, move)
                newplayer = reverseplayer(player)
                newevaluation, newmove = min_value(newboard, depth - 1, newplayer)
                # we assign a score to each possible move 
                # we get the score by calling min_value with decremented depth and reversed player
                # this will recurse so we eventually get the final score for our move
                if newevaluation > maxEval:
                    maxEval, best_move = newevaluation, move
                # keep track of the best move we've seen
            return maxEval, best_move

        def min_value(currboard, depth, player):
            possibleMoves = game_rules.getLegalMoves(currboard, player)
            if depth == 0 or len(possibleMoves) == 0:
                return self.h1(currboard, self.symbol), None
            
            minEval = POS_INF
            best_move = None
            for move in possibleMoves:
                newboard = game_rules.makeMove(currboard, move)
                newplayer = reverseplayer(player)
                newevaluation, newmove = max_value(newboard, depth - 1, newplayer)
                if newevaluation < minEval:
                    minEval, best_move = newevaluation, move
            return minEval, best_move

        value, move = max_value(board, self.depth, self.symbol)
        return move
    

class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth #ADDED: depth feature

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # a-b pruning code
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) == None or self.depth == 0:
            return None
        elif len(legalMoves) == 1:
             return legalMoves[0]

        def reverseplayer(player):
            if player == 'x':
                return 'o'
            elif player =='o':
                return 'x'
            else:
                return None
            
        def max_value(currboard, depth, player, alpha, beta):
            possibleMoves = game_rules.getLegalMoves(currboard, player)
            if depth == 0 or len(possibleMoves) == 0:
                return self.h1(currboard, self.symbol), None
            maxEval = NEG_INF
            best_move = None
            for move in possibleMoves:
                newboard = game_rules.makeMove(currboard, move)
                newplayer = reverseplayer(player)
                newevaluation, newmove = min_value(newboard, depth - 1, newplayer, alpha, beta)
                if newevaluation > maxEval:
                    maxEval, best_move = newevaluation, move
                    alpha = max(alpha, maxEval)
                if maxEval >= beta:
                    return maxEval, best_move
            return maxEval, best_move

        def min_value(currboard, depth, player, alpha, beta):
            possibleMoves = game_rules.getLegalMoves(currboard, player)
            if depth == 0 or len(possibleMoves) == 0:
                return self.h1(currboard, self.symbol), None
            minEval = POS_INF
            best_move = None
            for move in possibleMoves:
                newboard = game_rules.makeMove(currboard, move)
                newplayer = reverseplayer(player)
                newevaluation, newmove = max_value(newboard, depth - 1, newplayer, alpha, beta)
                if newevaluation < minEval:
                    minEval, best_move = newevaluation, move
                    beta = min(beta, minEval)
                if minEval <= alpha:
                    return minEval, best_move
            return minEval, best_move
        
        value, move = max_value(board, self.depth, self.symbol, NEG_INF, POS_INF)
        return move


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
