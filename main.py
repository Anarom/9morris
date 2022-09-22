import ui
from engine import Engine


class Player:
    def __init__(self, is_white, ui):
        self.is_white = is_white
        self.ui = ui()


class Game:
    def __init__(self, ui1, ui2):
        self.board = [None] * 24
        self.player1 = Player(True, ui1)
        self.player2 = Player(False, ui2)
        self.engine = Engine()
        if ui1 is ui2 and isinstance(ui1, ui.UIBoard):
            self.player1.ui.screen = self.player2.ui.screen
        self.moves_played = 0
        self.result = self.run()

    def play_move(self, move, player):
        if not move:
            print('NOMOVE')
            return 1 - player.is_white
        self.engine.apply_move(self.board, move)
        if self.engine.line_formed(self.board, move[1]):
            pieces = self.engine.get_pieces(self.board, not player.is_white)
            piece = player.ui.choose_piece(pieces)
            if not piece:
                print('NOPIECE')
                return 1 - player.is_white
            self.board[piece] = None
            if len(pieces) == 3 and self.moves_played > 18:
                print('GAMEOVER')
                return player.is_white

    def run(self):
        player = self.player1
        while True:
            moves = self.engine.get_moves(self.board, player.is_white, self.moves_played)
            if not moves:
                print('NOMOVES')
                return 0 if player.is_white else 1
            move = player.ui.choose_move(moves)
            result = self.play_move(move, player)
            if result is not None:
                return result
            self.moves_played += 1
            new_state = [x for x in self.board]
            player.ui.update(new_state)
            player = self.player2 if player is self.player1 else self.player1
            player.ui.update(new_state)


if __name__ == '__main__':
    results = [0, 0]
    game_count = 1
    for g in range(1, game_count + 1):
        game = Game(ui.UIBoard,ui.UIBoard)
        results[game.result] += 1
        if not g % (game_count / 10):
            print(f'{g} games done')
    print(f'resilts: {results}')
