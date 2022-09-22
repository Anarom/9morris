import random
import time
import pygame
from engine import Engine


class UI:
    def __init__(self):
        self.state = [None] * 24
        self.moves_played = 0
        self.move_delay = 0
        self.quick_start = True

    def choose_move(self, moves):
        raise NotImplementedError

    def choose_piece(self, pieces):
        raise NotImplementedError

    def update(self, new_state):
        self.state = new_state
        self.moves_played += 1


class UIBoard(UI):
    def __init__(self, cell_size=50, board_color='brown', bg_color='gray', line_width=4):
        super().__init__()
        self.cell_size = cell_size
        self.color = board_color
        self.bg_color = bg_color
        self.line_width = line_width
        self.centres = [None] * 24
        self.cell_rect = pygame.Rect(0, 0, self.cell_size, self.cell_size)
        self.screen = self.get_screen()
        self.draw()

    def get_screen(self):
        screen_size = self.cell_size * 13
        screen = pygame.display.set_mode((screen_size, screen_size))
        screen.fill(self.bg_color)
        return screen

    def draw(self):
        # draw cells
        arrangement_dict = {0: 0, 1: 7, 2: 6, 3: 1, 4: 5, 5: 2, 6: 3, 7: 4}
        n = 0
        for d in range(6, 1, -2):
            d0 = 6 - d
            for dx in range(0, 3 * d, d):
                for dy in range(0, 3 * d, d):
                    if dx == d and dy == d:
                        continue
                    new_cell = self.cell_rect.move((dx + d0) * self.cell_size, (dy + d0) * self.cell_size)
                    self.centres[arrangement_dict[n % 8] + n // 8 * 8] = new_cell.center
                    pygame.draw.rect(self.screen, self.color, new_cell)
                    n += 1
        # draw rings
        for d in range(3):
            start_cell = self.centres[d * 8]
            for i in (2, 4, 6, 0):
                end_cell = self.centres[i + d * 8]
                pygame.draw.line(self.screen, self.color, start_cell, end_cell, width=self.line_width)
                start_cell = end_cell
        # draw ring connections
        for p0, p1 in ((1, 17), (3, 19), (5, 21), (7, 23)):
            pygame.draw.line(self.screen, self.color, self.centres[p0], self.centres[p1], width=self.line_width)
        pygame.display.update()

    def update(self, new_state):
        for n in range(len(self.state)):
            if self.state[n] != new_state[n]:
                if new_state[n] is None:
                    self.reset_cell(n)
                else:
                    self.draw_piece(n, new_state[n])
        self.state = new_state
        self.moves_played += 1
        e = pygame.event.get()
        pygame.display.update()

    def reset_cell(self, n):
        dx = self.centres[n][0] - self.cell_size // 2
        dy = self.centres[n][1] - self.cell_size // 2
        new_cell = self.cell_rect.move(dx, dy)
        rect = pygame.draw.rect(self.screen, self.color, new_cell)
        pygame.display.update(rect)

    def draw_piece(self, n, is_white):
        color = 'white' if is_white else 'black'
        piece = pygame.draw.circle(self.screen, color, self.centres[n], self.cell_size // 2)
        pygame.display.update(piece)

    def calc_cell_number(self, pos):
        max_distance = 2 ** 0.5 * self.cell_size // 2
        for n, center in enumerate(self.centres):
            dx = center[0] - pos[0]
            dy = center[1] - pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance <= max_distance:
                return n

    def choose_move(self, moves):
        if self.quick_start and self.moves_played < 18:
            return random.choice(moves)
        pygame.display.update()
        print('choose move')
        if moves[0][0] is None:
            n = self.choose_piece([move[1] for move in moves], not_capture=True)
            return moves[n] if n is not None else None
        while True:
            clicked = []
            while len(clicked) < 2:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        print(f'got {"1st" if not clicked else "2nd"} click')
                        clicked.append(self.calc_cell_number(event.pos))
                    elif event.type == pygame.QUIT:
                        return None
            for move in moves:
                if move[0] == clicked[0] and move[1] == clicked[1]:
                    return move

    def choose_piece(self, pieces, not_capture=False):
        print('choose piece')
        if self.quick_start and self.moves_played < 18:
            return random.choice(pieces)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = self.calc_cell_number(event.pos)
                    print('got click')
                    for n, piece in enumerate(pieces):
                        if piece == clicked:
                            return n if not_capture else piece
                elif event.type == pygame.QUIT:
                    return None


class UICmd(UI):
    def choose_move(self, moves):
        printing = True
        while True:
            if printing:
                print('### Choose move to play ###')
                for x, move in enumerate(moves):
                    if move[0]:
                        print(f'#{x}: From {move[0]} to {move[1]}')
                    else:
                        print(f'#{x}: Place at {move[1]}')
                printing = False
            ans = input('Enter move number: ')
            if ans:
                try:
                    ans = int(ans)
                except ValueError:
                    print(f'Error: specify INT [{0},{len(moves) - 1}], "" to resign or -1 to re-print moves')
                    continue
                if ans == -1:
                    printing = True
                else:
                    return moves[ans]
            else:
                return None

    def choose_piece(self, pieces):
        printing = True
        while True:
            if printing:
                print('### Choose piece to capture ###')
                for x, piece in enumerate(pieces):
                    print(f'#{x}: piece at {piece}')
                printing = False
            ans = input('Enter piece number: ')
            if ans:
                try:
                    ans = int(ans)
                except ValueError:
                    print(f'Error: specify INT [{0},{len(moves) - 1}], "" to resign or -1 to re-print pieces')
                    continue
                if ans == -1:
                    printing = True
                else:
                    return moves[ans]
            else:
                return None


class UIRandomBoard(UIBoard):
    def choose_move(self, moves):
        time.sleep(self.move_delay)
        return random.choice(moves)

    def choose_piece(self, pieces):
        return random.choice(pieces)


class UIRandom(UI):
    def choose_move(self, moves):
        return random.choice(moves)

    def choose_piece(self, pieces):
        return random.choice(pieces)


class UICalc(UI):
    def __init__(self):
        super().__init__()
        self.engine = Engine()

    def evaluate(self, image):
        piece_diff = len(self.engine.get_pieces(image, True)) - len(self.engine.get_pieces(image, False))
        print(f'eval:{piece_diff} image: {image}')
        return piece_diff

    def expand_image(self, image, is_white, wrap=False):
        moves = self.engine.get_moves(image, is_white, self.moves_played)
        new_images = []
        for n, move in enumerate(moves):
            new_image = [x for x in image]
            self.engine.apply_move(new_image, move)
            if self.engine.line_formed(new_image, move[1]):
                for piece in self.engine.get_pieces(new_image, not is_white):
                    capture_variant = [x for x in new_image]
                    capture_variant[piece] = None
                    new_images.append(capture_variant)
            else:
                new_images.append(new_image)
        return [new_images] if wrap else new_images

    def build(self, core_image, is_white):
        core_images = self.expand_image(core_image, is_white, wrap=True)
        for depth in range(4):
            for n in range(len(core_images)):
                new_images = []
                for image in core_images[n]:
                    new_images.append(self.expand_image(image, is_white))
                core_images[n] = new_images
            print(f'new len: {sum([len(x) for x in core_images[n]])}')
            is_white = not is_white
            input()
        func = min if is_white == core_is_white else max
        for j in range(len(new_images)):
            for k in range(len(new_images[j])):
                evaluation = self.build(new_images[j][k], not is_white, core_is_white, depth=depth + 1)
                new_images[j][k] = evaluation
            new_images[j] = func(new_images[j])
        if depth:
            return func(new_images)
        else:
            print('chose move with eval', min(new_images))
            return new_images.index(min(new_images))

    def choose_move(self, moves):
        if self.moves_played < 18:
            return random.choice(moves)
        else:
            print('chosing move')
            i = self.build(self.state, moves[0][2])
            print(f'move: {moves[i]}')
            return moves[i]

    def choose_piece(self, pieces):
        return random.choice(pieces)
