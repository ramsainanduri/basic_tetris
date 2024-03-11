import pygame
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),
    (255, 165, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 255),
    (255, 0, 0),
]

# Tetromino shapes and their rotations
TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[2, 2], [2, 2]],
    'T': [[0, 3, 0], [3, 3, 3]],
    'S': [[0, 4, 4], [4, 4, 0]],
    'Z': [[5, 5, 0], [0, 5, 5]],
    'J': [[6, 0, 0], [6, 6, 6]],
    'L': [[0, 0, 7], [7, 7, 7]],
}

# Game settings
BLOCK_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def create_tetromino():
    shape = random.choice(list(TETROMINOS.values()))
    return {'shape': shape, 'x': BOARD_WIDTH // 2 - len(shape[0]) // 2, 'y': 0, 'color': random.choice(COLORS)}

def rotate_tetromino(tetromino):
    rotated_shape = [list(row) for row in zip(*tetromino['shape'][::-1])]
    return rotated_shape

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            try:
                if cell and board[y + off_y][x + off_x]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for _ in range(BOARD_WIDTH)]] + board

def join_matrices(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for y, row in enumerate(mat2):
        for x, val in enumerate(row):
            if val:
                mat1[y + off_y][x + off_x] = val
    return mat1

def clear_rows(board):
    cleared = 0
    for i, row in enumerate(board[::-1]):
        if 0 not in row:
            board = remove_row(board, len(board) - 1 - i)
            cleared += 1
    return board, cleared

def draw_matrix(matrix, offset):
    off_x, off_y = offset
    for y, row in enumerate(matrix):
        for x, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, COLORS[val - 1],
                                 pygame.Rect((off_x + x) * BLOCK_SIZE,
                                             (off_y + y) * BLOCK_SIZE, 
                                             BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY,
                                 pygame.Rect((off_x + x) * BLOCK_SIZE,
                                             (off_y + y) * BLOCK_SIZE, 
                                             BLOCK_SIZE, BLOCK_SIZE), 1)

def main():
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 25)
    clock = pygame.time.Clock()

    current_piece = create_tetromino()
    next_piece = create_tetromino()
    board = [[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_x = current_piece['x'] - 1
                    if not check_collision(board, current_piece['shape'], (new_x, current_piece['y'])):
                        current_piece['x'] = new_x
                elif event.key == pygame.K_RIGHT:
                    new_x = current_piece['x'] + 1
                    if not check_collision(board, current_piece['shape'], (new_x, current_piece['y'])):
                        current_piece['x'] = new_x
                elif event.key == pygame.K_DOWN:
                    current_piece['y'] += 1
                    if check_collision(board, current_piece['shape'], (current_piece['x'], current_piece['y'])):
                        current_piece['y'] -= 1
                        board = join_matrices(board, current_piece['shape'], (current_piece['x'], current_piece['y']))
                        board, cleared = clear_rows(board)
                        score += cleared
                        current_piece = next_piece
                        next_piece = create_tetromino()
                        if check_collision(board, current_piece['shape'], (current_piece['x'], current_piece['y'])):
                            game_over = True
                elif event.key == pygame.K_UP:
                    new_shape = rotate_tetromino(current_piece)
                    if not check_collision(board, new_shape, (current_piece['x'], current_piece['y'])):
                        current_piece['shape'] = new_shape

        screen.fill((0, 0, 0))
        draw_matrix(board, (0, 0))
        draw_matrix(current_piece['shape'], (current_piece['x'], current_piece['y']))
        pygame.display.update()
        clock.tick(10)

    print("Game Over! Your score was:", score)
    pygame.quit()

if __name__ == '__main__':
    main()
