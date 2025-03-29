import pygame
import check_valid_move

# Khởi tạo Pygame
pygame.init()

# Kích thước bàn cờ
WIDTH, HEIGHT = 640, 640
SQ_SIZE = WIDTH // 8  # Kích thước mỗi ô cờ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Vua")

# Màu sắc
WHITE = pygame.Color("white")
GRAY = pygame.Color("gray")
YELLOW = pygame.Color(255, 255, 0, 100)  # Màu vàng cho quân cờ được chọn
GREEN = pygame.Color(0, 255, 0, 100)     # Màu xanh lá cho các nước đi hợp lệ

# Biến game
selected_piece = None
valid_moves = []
current_player = "white"

# Load hình ảnh quân cờ
pieces = {
    "w_pawn": pygame.image.load("images/white-pawn.png"),
    "b_pawn": pygame.image.load("images/black-pawn.png"),
    "w_rook": pygame.image.load("images/white-rook.png"),
    "b_rook": pygame.image.load("images/black-rook.png"),
    "w_knight": pygame.image.load("images/white-knight.png"),
    "b_knight": pygame.image.load("images/black-knight.png"),
    "w_bishop": pygame.image.load("images/white-bishop.png"),
    "b_bishop": pygame.image.load("images/black-bishop.png"),
    "w_queen": pygame.image.load("images/white-queen.png"),
    "b_queen": pygame.image.load("images/black-queen.png"),
    "w_king": pygame.image.load("images/white-king.png"),
    "b_king": pygame.image.load("images/black-king.png")
}

# Scale hình ảnh
pieces = {name: pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE)) for name, img in pieces.items()}

# Khởi tạo bàn cờ
board = [
    ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"],
    ["b_pawn"] * 8,
    [None] * 8, [None] * 8, [None] * 8, [None] * 8,
    ["w_pawn"] * 8,
    ["w_rook", "w_knight", "w_bishop", "w_king","w_queen", "w_bishop", "w_knight", "w_rook"]
]

def draw_board():
    """Vẽ bàn cờ"""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_highlight():
    """Vẽ highlight cho quân cờ được chọn và các nước đi hợp lệ"""
    # Vẽ highlight cho quân cờ được chọn
    if selected_piece:
        x, y = selected_piece
        s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        s.fill(YELLOW)
        screen.blit(s, (x * SQ_SIZE, y * SQ_SIZE))

    # Vẽ highlight cho các nước đi hợp lệ
    for move in valid_moves:
        x, y = move
        s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        s.fill(GREEN)
        screen.blit(s, (x * SQ_SIZE, y * SQ_SIZE))

def draw_pieces():
    """Vẽ các quân cờ"""
    for row in range(8):
        for col in range(8):
            piece_name = board[row][col]
            if piece_name:
                screen.blit(pieces[piece_name], (col * SQ_SIZE, row * SQ_SIZE))

def get_piece_color(piece_name):
    """Lấy màu của quân cờ từ tên file"""
    if piece_name is None:
        return None
    return "white" if piece_name.startswith("w_") else "black"

def update_valid_moves():
    """Cập nhật danh sách các nước đi hợp lệ"""
    global valid_moves
    valid_moves = []
    
    if selected_piece:
        col, row = selected_piece
        for x in range(8):
            for y in range(8):
                if check_valid_move.is_valid_move(board, (col, row), (x, y)):
                    valid_moves.append((x, y))
        print(f"Selected piece at ({col}, {row})")
        print(f"Valid moves: {valid_moves}")

def main():
    global selected_piece, valid_moves, current_player
    running = True

    while running:
        # Vẽ bàn cờ
        draw_board()
        draw_highlight()
        draw_pieces()
        pygame.display.flip()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                col, row = mx // SQ_SIZE, my // SQ_SIZE

                # Click vào quân cờ
                if board[row][col]:
                    piece_color = get_piece_color(board[row][col])
                    if piece_color == current_player:
                        if selected_piece is None or selected_piece != (col, row):
                            selected_piece = (col, row)
                            update_valid_moves()
                    elif selected_piece and check_valid_move.can_capture(board, selected_piece, (col, row)):
                        # Ăn quân đối phương
                        piece = board[selected_piece[1]][selected_piece[0]]
                        board[selected_piece[1]][selected_piece[0]] = None
                        board[row][col] = piece
                        # Đổi lượt chơi
                        current_player = "black" if current_player == "white" else "white"
                        print(f"Current player: {current_player}")
                        # Reset selection
                        selected_piece = None
                        valid_moves = []
                
                # Click vào ô trống
                elif selected_piece:
                    if (col, row) in valid_moves:
                        # Di chuyển quân cờ
                        piece = board[selected_piece[1]][selected_piece[0]]
                        board[selected_piece[1]][selected_piece[0]] = None
                        board[row][col] = piece
                        # Đổi lượt chơi
                        current_player = "black" if current_player == "white" else "white"
                        print(f"Current player: {current_player}")
                        # Reset selection
                        selected_piece = None
                        valid_moves = []

    pygame.quit()

if __name__ == "__main__":
    main()