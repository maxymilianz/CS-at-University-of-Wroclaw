from ReversiAux import *

from math import inf, log, sqrt


class MCTSPlayer:
    def __init__(self, exploration_param = sqrt(2), timeout = .5):
        self.exploration_param = exploration_param
        self.timeout = timeout
        self.move_to_wins_playouts = {}
        self.playouts_total = 0

    def uct(self, move):
        wins, playouts = self.move_to_wins_playouts.get(move, (0, 0))
        if playouts:
            if self.playouts_total:
                return wins / playouts + self.exploration_param * sqrt(log(self.playouts_total) / playouts)
            else:
                return wins / playouts
        else:
            return inf

    def mcts(self, board, empty_fields, color, start_time):
        possibilities = moves(board, empty_fields, color)
        wins, playouts = 0, 0

        for move in sorted(possibilities, key = self.uct, reverse = True):
            if not move[1]:     # no empty fields, someone won (TODO handle case when no move is available)
                black_count, white_count = count_score(move[0])
                return int((color == black) == (black_count > white_count)), 1

            if time() - start_time >= self.timeout:
                break
            else:
                new_wins, new_playouts = self.mcts(*move, opposite_color[color], start_time)      # wins of the opposite color
                wins += new_playouts - new_wins
                playouts += new_playouts

        old_wins, old_playouts = self.move_to_wins_playouts.get((board, empty_fields), (0, 0))
        self.move_to_wins_playouts[(board, empty_fields)] = old_wins + wins, old_playouts + playouts
        return wins, playouts

    def __call__(self, board, empty_fields, color):
        self.mcts(board, empty_fields, color, time())
        move = board, empty_fields
        playouts = -1       # < 0; artificial playouts count for no move
        possibilities = moves(board, empty_fields, color)

        for new_move in possibilities:
            new_wins, new_playouts = self.move_to_wins_playouts.get(new_move, (0, 0))       # I discard wins count

            if new_playouts > playouts:
                move = new_move
                playouts = new_playouts

            if move in self.move_to_wins_playouts:
                del self.move_to_wins_playouts[move]

        return move


class RandomMCTSPlayer:
    def __init__(self, simulations_count):
        self.simulations_count = simulations_count

    def play(self, board, empty_fields, color):
        not_moved = False

        while empty_fields:
            not_moved = False
            new_board, empty_fields = random_player(board, empty_fields, color)

            if not empty_fields:
                break

            if new_board == board:
                not_moved = True

            new_board, empty_fields = random_player(board, empty_fields, opposite_color[color])

            if not_moved and new_board == board:
                break

            board = new_board

        black_count, white_count = count_score(board)

        if black_count > white_count:
            return black
        elif black_count < white_count:
            return white
        else:
            return None

    def __call__(self, board, empty_fields, color):
        possibilities = {move: [self.play(*move, opposite_color[color]) for i in range(self.simulations_count)].count(color) for move in moves(board, empty_fields, color)}

        if possibilities:
            board, empty_fields = max(possibilities, key = lambda move: possibilities[move])

        return board, empty_fields
