PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '


class TicTacToe:
    #1 10
    def __init__(self, board=None, current_player=PLAYER_X):
        if board is None:
            self.board = [EMPTY] * 9
        else:
            self.board = board.copy()

        self.current_player = current_player
    #2
    def get_available_moves(self):
        available_moves = []

        for i in range(9):
            if self.board[i] == EMPTY:
                available_moves.append(i)

        return available_moves
    #3
    def is_valid_move(self, pos):
        if pos < 0 or pos >= 9:
            return False

        if self.board[pos] != EMPTY:
            return False

        return True
    #4
    def make_move(self, pos):
        if not self.is_valid_move(pos):
            return False

        self.board[pos] = self.current_player

        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X

        return True
    #5
    def undo_move(self, pos):
        if self.board[pos] == EMPTY:
            return

        self.board[pos] = EMPTY

        if self.current_player == PLAYER_X:
            self.current_player = PLAYER_O
        else:
            self.current_player = PLAYER_X
    #6
    def get_winning_line(self):
        winning_lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        ]

        for line in winning_lines:
            a, b, c = line

            if self.board[a] != EMPTY:
                if self.board[a] == self.board[b] and self.board[b] == self.board[c]:
                    return line

        return None
    #7
    def check_winner(self):
        winning_line = self.get_winning_line()

        if winning_line is None:
            return None

        first_position = winning_line[0]
        return self.board[first_position]
    #8
    def is_draw(self):
        if self.check_winner() is not None:
            return False

        if len(self.get_available_moves()) == 0:
            return True

        return False
    #9
    def is_game_over(self):
        if self.check_winner() is not None:
            return True

        if self.is_draw():
            return True

        return False