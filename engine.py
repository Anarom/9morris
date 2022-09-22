class Engine:
    def __init__(self):
        pass

    def encode_image(self, image):
        l_dict = {None: '0', 0: '1', 1: '2'}
        code = ''
        for cell in image:
            code += l_dict[cell]
        print(code)
        return code

    def decode_image(self, code):
        l_dict = {'0':None,'1':0,'2':1}
        image = []
        for letter in code:
            image.append(l_dict[letter])
        print(image)
        return image

    def get_empty_cells(self, board):
        cells = []
        for n, cell in enumerate(board):
            if cell is None:
                cells.append(n)
        return cells

    def get_pieces(self, board, is_white):
        pieces = []
        for n, cell in enumerate(board):
            if cell == bool(is_white):
                pieces.append(n)
        return pieces

    def get_moves(self, board, is_white, moves_played):
        if moves_played < 18:
            return [(None, cell, is_white) for cell in self.get_empty_cells(board)]
        moves = []
        pieces = self.get_pieces(board, is_white)
        for piece in pieces:
            if len(pieces) <= 3:
                for cell in self.get_empty_cells(board):
                    moves.append((piece, cell, is_white))
            else:
                for node in (self._nodes(piece) + self._inter_nodes(piece)):
                    if board[node] is None:
                        moves.append((piece, node, is_white))
        return moves

    def line_formed(self, board, cell):
        if cell % 2:
            lst1 = [board[node] for node in self._nodes(cell)]
            lst2 = [board[8 * x + cell % 8] for x in range(3)]
            for vals in (lst1, lst2):
                if len(set([board[cell]] + vals)) == 1:
                    return True
        else:
            for node in self._nodes(cell):
                diff = node - cell
                if (node + diff) // 8 != cell // 8:
                    if cell % 8:
                        next = cell // 8 * 8
                    else:
                        next = node - 1
                else:
                    next = node + diff
                vals = [board[x] for x in (cell, node, next)]
                if len(set(vals)) == 1:
                    return True
        return False

    def apply_move(self, board, move):
        board[move[1]] = 1 if move[2] else 0
        if move[0] is not None:
            board[move[0]] = None

    def _nodes(self, n):
        if n % 8:
            nodes = [n - 1] + ([n + 1] if n % 8 < 7 else [n // 8 * 8])
        else:
            nodes = [n + 7, n + 1]
        return nodes

    def _inter_nodes(self, n):
        nodes = []
        if n % 2:
            nodes += [n - 8] if n - 8 > 0 else []
            nodes += [n + 8] if n + 8 < 24 else []
        return nodes
