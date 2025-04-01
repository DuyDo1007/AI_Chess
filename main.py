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
GREEN = pygame.Color(0, 255, 0, 100)
RED = pygame.Color(255, 0, 0, 100)     # Màu đỏ cho chiếu

# Biến game
selected_piece = None
valid_moves = []
current_player = "white"
check = False
w_king_pos = (4, 7)  # Vị trí vua trắng
b_king_pos = (4, 0)  # Vị trí vua đen
promotion_piece = None  # Quân cờ được chọn để phong cấp

# Load hình ảnh quân cờ
pieces = {
    "white_pawn": pygame.image.load("images/wP.png"),
    "black_pawn": pygame.image.load("images/bP.png"),
    "white_rook": pygame.image.load("images/wR.png"),
    "black_rook": pygame.image.load("images/bR.png"),
    "white_knight": pygame.image.load("images/wN.png"),
    "black_knight": pygame.image.load("images/bN.png"),
    "white_bishop": pygame.image.load("images/wB.png"),
    "black_bishop": pygame.image.load("images/bB.png"),
    "white_queen": pygame.image.load("images/wQ.png"),
    "black_queen": pygame.image.load("images/bQ.png"),
    "white_king": pygame.image.load("images/wK.png"),
    "black_king": pygame.image.load("images/bK.png")
}

# Scale hình ảnh
pieces = {name: pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE)) for name, img in pieces.items()}

# Khởi tạo bàn cờ
board = [
    ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop", "black_knight", "black_rook"],
    ["black_pawn"] * 8,
    [None] * 8, [None] * 8, [None] * 8, [None] * 8,
    ["white_pawn"] * 8,
    ["white_rook", "white_knight", "white_bishop", "white_queen","white_king", "white_bishop", "white_knight", "white_rook"]
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
    return "white" if piece_name.startswith("white_") else "black"

def update_valid_moves():
    """Cập nhật danh sách các nước đi hợp lệ"""
    global valid_moves
    valid_moves = []
    
    if selected_piece:
        col, row = selected_piece
        for x in range(8):
            for y in range(8):
                if check_valid_move.is_valid_move(board, (col, row), (x, y)):
                    # Tạo bản sao của bàn cờ để kiểm tra nước đi
                    temp_board = [row[:] for row in board]
                    piece = temp_board[row][col]
                    temp_board[row][col] = None
                    temp_board[y][x] = piece
                    
                    # Nếu đang bị chiếu, kiểm tra xem nước đi có giải được chiếu không
                    if check:
                        if not check_valid_move.is_check(temp_board, current_player):
                            valid_moves.append((x, y))
                    else:
                        valid_moves.append((x, y))

def update_king_positions():
    """Cập nhật vị trí vua trên bàn cờ"""
    global w_king_pos, b_king_pos
    for row in range(8):
        for col in range(8):
            if board[row][col] == "white_king":
                w_king_pos = (col, row)
            elif board[row][col] == "black_king":
                b_king_pos = (col, row)

def draw_promotion_menu(row, col):
    """Vẽ menu phong quân"""
    # Vẽ nền menu
    menu_surface = pygame.Surface((SQ_SIZE * 4, SQ_SIZE))
    menu_surface.fill(WHITE)
    screen.blit(menu_surface, (col * SQ_SIZE, row * SQ_SIZE))
    
    # Vẽ các quân cờ có thể phong cấp
    pieces_to_show = ["queen", "rook", "bishop", "knight"]
    for i, piece in enumerate(pieces_to_show):
        piece_name = f"{current_player}_{piece}"
        piece_surface = pieces[piece_name]
        screen.blit(piece_surface, (col * SQ_SIZE + i * SQ_SIZE, row * SQ_SIZE))

def handle_promotion(row, col):
    """Xử lý phong quân"""
    global promotion_piece
    mx, my = pygame.mouse.get_pos()
    menu_col = mx // SQ_SIZE
    menu_row = my // SQ_SIZE
    
    # Kiểm tra click có trong menu phong quân không
    if menu_row == row and col <= menu_col <= col + 3:
        pieces_to_show = ["queen", "rook", "bishop", "knight"]
        selected_piece = pieces_to_show[menu_col - col]
        promotion_piece = f"{current_player}_{selected_piece}"
        return True
    return False

def reset_board():
    """Reset bàn cờ về trạng thái ban đầu"""
    global board, current_player, check, selected_piece, valid_moves, w_king_pos, b_king_pos
    board = [
        ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop", "black_knight", "black_rook"],
        ["black_pawn"] * 8,
        [None] * 8, [None] * 8, [None] * 8, [None] * 8,
        ["white_pawn"] * 8,
        ["white_rook", "white_knight", "white_bishop", "white_queen","white_king", "white_bishop", "white_knight", "white_rook"]
    ]
    current_player = "white"
    check = False
    selected_piece = None
    valid_moves = []
    w_king_pos = (4, 7)
    b_king_pos = (4, 0)
    check_valid_move.white_king_moved = False
    check_valid_move.black_king_moved = False

def main():
    global selected_piece, valid_moves, current_player, check, w_king_pos, b_king_pos, promotion_piece
    running = True
    promotion_pos = None  # Vị trí cần phong quân

    while running:
        # Vẽ bàn cờ
        draw_board()
        draw_highlight()
        draw_pieces()
        
        # Vẽ menu phong quân nếu cần
        if promotion_pos:
            row, col = promotion_pos
            draw_promotion_menu(row, col)
            
        pygame.display.flip()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                col, row = mx // SQ_SIZE, my // SQ_SIZE

                # Xử lý phong quân nếu đang trong trạng thái phong quân
                if promotion_pos:
                    if handle_promotion(promotion_pos[0], promotion_pos[1]):
                        # Thực hiện phong quân
                        board[promotion_pos[0]][promotion_pos[1]] = promotion_piece
                        promotion_pos = None
                        promotion_piece = None
                        # Đổi lượt chơi
                        current_player = "black" if current_player == "white" else "white"
                        
                        # Kiểm tra chiếu sau khi phong quân
                        if check_valid_move.is_check(board, current_player):
                            if check_valid_move.is_checkmate(board, current_player):
                                # Hiển thị thông báo chiếu hết
                                font = pygame.font.Font(None, 74)
                                text = font.render(f"{'White' if current_player == 'black' else 'Black'} win!", True, (255, 0, 0))
                                text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                                screen.blit(text, text_rect)
                                pygame.display.flip()
                                pygame.time.wait(2000)
                                # Reset bàn cờ và bắt đầu ván mới
                                reset_board()
                                continue
                            else:
                                # Hiển thị thông báo chiếu
                                if current_player == "white":
                                    check_valid_move.white_king_moved = True
                                else:
                                    check_valid_move.black_king_moved = True
                                king_pos = w_king_pos if current_player == "white" else b_king_pos
                                s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                                s.fill(RED)
                                screen.blit(s, (king_pos[0] * SQ_SIZE, king_pos[1] * SQ_SIZE))
                                font = pygame.font.Font(None, 74)
                                pygame.display.flip()
                                text = font.render("Check!", True, (255, 0, 0))
                                text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                                screen.blit(text, text_rect)
                                pygame.display.flip()
                                pygame.time.wait(750)
                                check = True
                        elif check:
                            check = False
                        continue

                # Click vào quân cờ
                if board[row][col]:
                    piece_color = get_piece_color(board[row][col])
                    if piece_color == current_player:
                        if selected_piece is None or selected_piece != (col, row):
                            selected_piece = (col, row)
                            update_valid_moves()
                    elif selected_piece and check_valid_move.can_capture(board, selected_piece, (col, row)):
                        # Tạo bản sao của bàn cờ để kiểm tra nước đi
                        temp_board = [row[:] for row in board]
                        piece = temp_board[selected_piece[1]][selected_piece[0]]
                        temp_board[selected_piece[1]][selected_piece[0]] = None
                        temp_board[row][col] = piece
                        
                        # Kiểm tra nước đi có hợp lệ không
                        is_valid_move = True
                        if check:
                            is_valid_move = not check_valid_move.is_check(temp_board, current_player)
                        
                        if is_valid_move:
                            # Ăn quân đối phương
                            board[selected_piece[1]][selected_piece[0]] = None
                            board[row][col] = piece
                            update_king_positions()
                            
                            # Kiểm tra phong quân sau khi ăn quân
                            if "pawn" in piece:
                                if (current_player == "white" and row == 0) or (current_player == "black" and row == 7):
                                    promotion_pos = (row, col)
                                    continue
                            
                            # Đổi lượt chơi
                            current_player = "black" if current_player == "white" else "white"
                            
                            # Kiểm tra chiếu sau khi di chuyển
                            if check_valid_move.is_check(board, current_player):
                                if check_valid_move.is_checkmate(board, current_player):
                                    # Hiển thị thông báo chiếu hết
                                    font = pygame.font.Font(None, 74)
                                    text = font.render(f"{'White' if current_player == 'black' else 'Black'} win!", True, (255, 0, 0))
                                    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                                    screen.blit(text, text_rect)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                    # Reset bàn cờ và bắt đầu ván mới
                                    reset_board()
                                    continue
                                else:
                                    # Hiển thị thông báo chiếu
                                    if current_player == "white":
                                        check_valid_move.white_king_moved = True
                                    else:
                                        check_valid_move.black_king_moved = True
                                    king_pos = w_king_pos if current_player == "white" else b_king_pos
                                    s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                                    s.fill(RED)
                                    screen.blit(s, (king_pos[0] * SQ_SIZE, king_pos[1] * SQ_SIZE))
                                    font = pygame.font.Font(None, 74)
                                    pygame.display.flip()
                                    text = font.render("Check!", True, (255, 0, 0))
                                    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                                    screen.blit(text, text_rect)
                                    pygame.display.flip()
                                    pygame.time.wait(750)
                                    check = True
                            elif check:
                                check = False
                            
                            # Reset selection
                            selected_piece = None
                            valid_moves = []

                # Click vào ô trống
                elif selected_piece:
                    if (col, row) in valid_moves:
                        # Tạo bản sao của bàn cờ để kiểm tra nước đi
                        temp_board = [row[:] for row in board]
                        piece = temp_board[selected_piece[1]][selected_piece[0]]
                        temp_board[selected_piece[1]][selected_piece[0]] = None
                        temp_board[row][col] = piece
                        
                        # Kiểm tra nước đi có hợp lệ không
                        is_valid_move = True
                        if check:
                            is_valid_move = not check_valid_move.is_check(temp_board, current_player)
                        
                        if is_valid_move:
                            # Di chuyển quân cờ
                            board[selected_piece[1]][selected_piece[0]] = None
                            board[row][col] = piece
                            
                            # Xử lý nhập thành
                            if "king" in piece and abs(col - selected_piece[0]) == 2:
                                # Xác định hướng nhập thành
                                step = 1 if col > selected_piece[0] else -1
                                rook_x = 0 if step == -1 else 7
                                new_rook_x = col - step
                                
                                # Di chuyển xe
                                board[row][new_rook_x] = board[row][rook_x]
                                board[row][rook_x] = None
                            
                            # Kiểm tra phong quân
                            if "pawn" in piece:
                                if (current_player == "white" and row == 0) or (current_player == "black" and row == 7):
                                    promotion_pos = (row, col)
                                    continue
                            
                            update_king_positions()
                            # Đổi lượt chơi
                            current_player = "black" if current_player == "white" else "white"
                            
                            # Kiểm tra chiếu sau khi di chuyển
                            if check_valid_move.is_check(board, current_player):
                                if check_valid_move.is_checkmate(board, current_player):
                                    # Hiển thị thông báo chiếu hết
                                    font = pygame.font.Font(None, 74)
                                    text = font.render(f"{'White' if current_player == 'black' else 'Black'} win!", True, (255, 0, 0))
                                    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                                    screen.blit(text, text_rect)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                    # Reset bàn cờ và bắt đầu ván mới
                                    reset_board()
                                    continue
                                else:
                                    # Hiển thị thông báo chiếu
                                    if current_player == "white":
                                        check_valid_move.white_king_moved = True
                                    else:
                                        check_valid_move.black_king_moved = True
                                    king_pos = w_king_pos if current_player == "white" else b_king_pos
                                    s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                                    s.fill(RED)
                                    screen.blit(s, (king_pos[0] * SQ_SIZE, king_pos[1] * SQ_SIZE))
                                    font = pygame.font.Font(None, 74)
                                    pygame.display.flip()
                                    text = font.render("Check!", True, (255, 0, 0))
                                    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                                    screen.blit(text, text_rect)
                                    pygame.display.flip()
                                    pygame.time.wait(750)
                                    check = True
                            elif check:
                                check = False
                            
                            # Reset selection
                            selected_piece = None
                            valid_moves = []

    pygame.quit()

if __name__ == "__main__":
    main()