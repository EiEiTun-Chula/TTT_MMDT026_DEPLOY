import random

#from game import PLAYER_X, PLAYER_O
#update 20
from game import TicTacToe, PLAYER_X, PLAYER_O

class RandomAgent:
    def __init__(self, player):
        self.player = player
    #11
    def get_move(self, game):
        available_moves = game.get_available_moves()

        if len(available_moves) == 0:
            return None

        return random.choice(available_moves)

class HeuristicAgent:
    def __init__(self, player):
        self.player = player
    #12 
    def get_move(self, game):
        available_moves = game.get_available_moves()

        #choose an immediate winning move
        for pos in available_moves:
            game.board[pos] = self.player

            if game.check_winner() == self.player:
                game.board[pos] = ' '
                return pos

            game.board[pos] = ' '

        #13    
        #Blocking the opponent
        # Find the opponent
        if self.player == PLAYER_X:
            opponent = PLAYER_O
        else:
            opponent = PLAYER_X

        # Check whether the opponent can win
        for pos in available_moves:
            game.board[pos] = opponent

            if game.check_winner() == opponent:
                game.board[pos] = ' '
                return pos

            game.board[pos] = ' '

        #14
        # Priority 3: Choose the center
        if 4 in available_moves:
            return 4

        # Priority 4: Choose a corner
        corners = [0, 2, 6, 8]

        for pos in corners:
            if pos in available_moves:
                return pos

        # Priority 5: Choose a side
        sides = [1, 3, 5, 7]

        for pos in sides:
            if pos in available_moves:
                return pos

        return None

#15        
class MinimaxAgent:
    def __init__(self, player, use_alpha_beta=True):
        self.player = player
        self.use_alpha_beta = use_alpha_beta
        self.nodes_explored = 0        
    def evaluate(self, game, depth):
        winner = game.check_winner()

        if winner == self.player:
            return 10 - depth

        if winner is not None:
            return depth - 10

        if game.is_draw():
            return 0

        return None
    #16
    def _minimax(self, game, maximizing, alpha, beta, depth=0):
        self.nodes_explored += 1

        score = self.evaluate(game, depth)

        if score is not None:
            return score
        #update one with alpha beta 18
        if maximizing:
            best_score = float('-inf')

            for pos in game.get_available_moves():
                game.make_move(pos)
                #after the AI makes a move, it becomes the opponent's turn.
                score = self._minimax(game, False, alpha, beta, depth + 1)

                game.undo_move(pos)

                if score > best_score:
                    best_score = score

                if self.use_alpha_beta:
                    alpha = max(alpha, best_score)

                    if alpha >= beta:
                        break

            return best_score

        else:
            best_score = float('inf')

            for pos in game.get_available_moves():
                game.make_move(pos)
                #After the opponent makes a move, it becomes the AI's turn.
                score = self._minimax(game, True, alpha, beta, depth + 1)

                game.undo_move(pos)

                if score < best_score:
                    best_score = score

                if self.use_alpha_beta:
                    beta = min(beta, best_score)

                    if alpha >= beta:
                        break

            return best_score
    #17
    def get_move(self, game):
         # Reset the node counter for each AI move
        self.nodes_explored = 0
        available_moves = game.get_available_moves()
        

        if len(available_moves) == 0:
            return None

        
        best_score = float('-inf')
        best_move = None

        for pos in available_moves:
            game.make_move(pos)
            #update 19
            score = self._minimax(game, False, float('-inf'), float('inf'), 1)

            game.undo_move(pos)

            if score > best_score:
                best_score = score
                best_move = pos

        return best_move
    #26 - Calculate Minimax scores for available moves
    def get_move_scores(self, game):
        move_scores = {}

        for pos in game.get_available_moves():
            game.make_move(pos)

            score = self._minimax(
                game, False, float('-inf'), float('inf'), 1
            )

            game.undo_move(pos)

            move_scores[pos] = score

        return move_scores


#21        
def simulate_match(agent1, agent2, num_games=50):
    results = {
        "agent1_wins": 0,
        "agent2_wins": 0,
        "draws": 0
    }
    for i in range(num_games):
        game = TicTacToe() 
        while not game.is_game_over():

            if game.current_player == agent1.player:
                current_agent = agent1
            else:
                current_agent = agent2

            move = current_agent.get_move(game)
            game.make_move(move)   
            
        winner = game.check_winner()

        if winner == agent1.player:
            results["agent1_wins"] += 1

        elif winner == agent2.player:
            results["agent2_wins"] += 1

        else:
            results["draws"] += 1
    return results