import pygame
import check_valid_move
import json
import os
from Minimax import get_best_move, evaluate_board, get_all_valid_moves, get_piece_moves
import time
import copy

# Khởi tạo Pygame
pygame.init()

# Kích thước bàn cờ
WIDTH, HEIGHT = 640, 640
SQ_SIZE = WIDTH // 8  # Kích thước mỗi ô cờ

# Tăng chiều rộng màn hình để phần nút bấm rộng rãi hơn
SIDE_PANEL_WIDTH = 200  # Tăng từ 120 lên 200
screen_width = WIDTH + SIDE_PANEL_WIDTH

screen = pygame.display.set_mode((screen_width, HEIGHT))
pygame.display.set_caption("Cờ Vua AI")

# Tải và thiết lập logo
logo = pygame.image.load("images/wN.png")
logo = pygame.transform.scale(logo, (32, 32))
pygame.display.set_icon(logo)

# Màu sắc
WHITE = pygame.Color("white")
GRAY = pygame.Color("gray")
YELLOW = pygame.Color(255, 255, 0, 100)  # Màu vàng cho quân cờ được chọn
GREEN = pygame.Color(0, 255, 0, 100)
RED = pygame.Color(255, 0, 0, 100)     # Màu đỏ cho chiếu

# Biến game
selected_piece = None
valid_moves = []
move_history = [] # Danh sách lịch sử nước đi
current_player = "white"
check = False
w_king_pos = (4, 7)  # Vị trí vua trắng
b_king_pos = (4, 0)  # Vị trí vua đen
promotion_piece = None  # Quân cờ được chọn để phong cấp
count_draw = 0
save_button = pygame.Rect(WIDTH + 40, 10, 100, 40)  # Dời nút sang phải và tăng kích thước
load_button = pygame.Rect(WIDTH + 40, 60, 100, 40)
button_font = pygame.font.Font(None, 36)  # Font cho nút Save và Load
message_font = pygame.font.Font(None, 74)  # Font cho thông báo chiếu và chiếu hết
save_text = button_font.render("Save", True, (255, 255, 255))
load_text = button_font.render("Load", True, (255, 255, 255))

# Xóa nút chọn chế độ chơi và biến is_ai_mode vì chỉ có một chế độ
is_ai_mode = True  # Luôn là True vì chỉ có chế độ chơi với AI

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

# Thêm biến cho màn hình hiển thị thời gian
thinking_time_history = []  # Danh sách lưu thời gian suy nghĩ
history_font = pygame.font.Font(None, 24)  # Font cho text trong history
history_area = pygame.Rect(WIDTH + 40, 120, 160, HEIGHT - 140)  # Vị trí và kích thước vùng hiển thị
scroll_offset = 0  # Vị trí cuộn hiện tại
max_scroll = 0  # Vị trí cuộn tối đa

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
        piece = board[row][col]
        
        if piece:  # Thêm kiểm tra piece không phải None
            # Thêm các nước đi nhập thành cho vua
            if "king" in piece:
                # Nhập thành bên phải
                if col + 2 < 8:
                    # Kiểm tra không có quân cờ nào ở giữa
                    if all(board[row][x] is None for x in range(col + 1, col + 3)):
                        # Kiểm tra xe có đúng vị trí và màu không
                        rook_piece = board[row][7]
                        if rook_piece and rook_piece.startswith(current_player + "_rook"):
                            # Kiểm tra các ô vua đi qua có bị chiếu không
                            temp_board = [row[:] for row in board]
                            is_safe = True
                            for x in range(col, col + 3):
                                temp_board[row][x] = piece
                                if check_valid_move.is_check(temp_board, current_player):
                                    is_safe = False
                                    break
                                temp_board[row][x] = None
                            if is_safe:
                                valid_moves.append((col + 2, row))
                
                # Nhập thành bên trái
                if col - 2 >= 0:
                    # Kiểm tra không có quân cờ nào ở giữa
                    if all(board[row][x] is None for x in range(col - 2, col)):
                        # Kiểm tra xe có đúng vị trí và màu không
                        rook_piece = board[row][0]
                        if rook_piece and rook_piece.startswith(current_player + "_rook"):
                            # Kiểm tra các ô vua đi qua có bị chiếu không
                            temp_board = [row[:] for row in board]
                            is_safe = True
                            for x in range(col - 2, col + 1):
                                temp_board[row][x] = piece
                                if check_valid_move.is_check(temp_board, current_player):
                                    is_safe = False
                                    break
                                temp_board[row][x] = None
                            if is_safe:
                                valid_moves.append((col - 2, row))
            
            # Thêm các nước đi thông thường
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
                            # Nếu không bị chiếu, kiểm tra xem nước đi có khiến bị chiếu không
                            if not check_valid_move.is_check(temp_board, current_player):
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
    # Vẽ nền menu ở giữa màn hình
    menu_width = SQ_SIZE * 4
    menu_height = SQ_SIZE
    menu_x = (WIDTH - menu_width) // 2
    menu_y = (HEIGHT - menu_height) // 2
    
    # Vẽ nền mờ cho toàn màn hình
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Màu đen với độ trong suốt
    screen.blit(overlay, (0, 0))
    
    # Vẽ nền menu
    menu_surface = pygame.Surface((menu_width, menu_height))
    menu_surface.fill(WHITE)
    screen.blit(menu_surface, (menu_x, menu_y))
    
    # Vẽ viền menu
    pygame.draw.rect(screen, GRAY, (menu_x, menu_y, menu_width, menu_height), 2)
    
    # Vẽ các quân cờ có thể phong cấp
    pieces_to_show = ["queen", "rook", "bishop", "knight"]
    for i, piece in enumerate(pieces_to_show):
        # Vẽ nền cho từng ô
        pygame.draw.rect(screen, GRAY, (menu_x + i * SQ_SIZE, menu_y, SQ_SIZE, SQ_SIZE), 1)
        
        # Vẽ quân cờ
        piece_name = f"{current_player}_{piece}"
        piece_surface = pieces[piece_name]
        screen.blit(piece_surface, (menu_x + i * SQ_SIZE, menu_y))
        
        # Highlight ô khi di chuột qua
        mx, my = pygame.mouse.get_pos()
        if menu_x + i * SQ_SIZE <= mx <= menu_x + (i + 1) * SQ_SIZE and menu_y <= my <= menu_y + SQ_SIZE:
            s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
            s.fill((255, 255, 0, 100))  # Màu vàng với độ trong suốt
            screen.blit(s, (menu_x + i * SQ_SIZE, menu_y))

def handle_promotion(row, col):
    """Xử lý phong quân"""
    global promotion_piece
    mx, my = pygame.mouse.get_pos()
    
    # Tính toán vị trí menu ở giữa màn hình
    menu_width = SQ_SIZE * 4
    menu_height = SQ_SIZE
    menu_x = (WIDTH - menu_width) // 2
    menu_y = (HEIGHT - menu_height) // 2
    
    # Kiểm tra click có trong menu phong quân không
    if menu_y <= my <= menu_y + menu_height and menu_x <= mx <= menu_x + menu_width:
        menu_col = (mx - menu_x) // SQ_SIZE
        if 0 <= menu_col < 4:  # Kiểm tra menu_col có hợp lệ không
            pieces_to_show = ["queen", "rook", "bishop", "knight"]
            selected_piece = pieces_to_show[menu_col]
            promotion_piece = f"{current_player}_{selected_piece}"
            return True
    return False

def reset_board():
    """Reset bàn cờ về trạng thái ban đầu"""
    global board, current_player, check, selected_piece, valid_moves, w_king_pos, b_king_pos, move_history
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
    move_history = []  # Xóa lịch sử nước đi
    w_king_pos = (4, 7)
    b_king_pos = (4, 0)
    save_button = pygame.Rect(WIDTH + 40, 10, 100, 40)
    load_button = pygame.Rect(WIDTH + 40, 60, 100, 40)
    check_valid_move.white_king_moved = False
    check_valid_move.black_king_moved = False

def save_game():
    """Lưu trạng thái game vào file"""
    game_state = {
        'board': board,
        'current_player': current_player,
        'check': check,
        'w_king_pos': w_king_pos,
        'b_king_pos': b_king_pos,
        'white_king_moved': check_valid_move.white_king_moved,
        'black_king_moved': check_valid_move.black_king_moved
    }
    
    try:
        with open('game_state.json', 'w') as f:
            json.dump(game_state, f)
        return True
    except:
        return False

def load_game():
    """Tải trạng thái game từ file"""
    global board, current_player, check, w_king_pos, b_king_pos
    
    try:
        if not os.path.exists('game_state.json'):
            return False
            
        with open('game_state.json', 'r') as f:
            game_state = json.load(f)
            
        board = game_state['board']
        current_player = game_state['current_player']
        check = game_state['check']
        w_king_pos = tuple(game_state['w_king_pos'])
        b_king_pos = tuple(game_state['b_king_pos'])
        check_valid_move.white_king_moved = game_state['white_king_moved']
        check_valid_move.black_king_moved = game_state['black_king_moved']
        return True
    except:
        return False

def save_state_to_history():
    global move_history
    state = {
        'board': [row[:] for row in board],
        'current_player': current_player,
        'check': check,
        'w_king_pos': w_king_pos,
        'b_king_pos': b_king_pos,
        'white_king_moved': check_valid_move.white_king_moved,
        'black_king_moved': check_valid_move.black_king_moved,
    }
    move_history.append(state)

def draw_thinking_time_history():
    """Vẽ màn hình hiển thị thời gian suy nghĩ"""
    # Vẽ nền trắng
    pygame.draw.rect(screen, WHITE, history_area)
    pygame.draw.rect(screen, (0, 0, 0), history_area, 2)  # Viền đen
    
    # Tính toán vị trí cuộn
    global max_scroll
    line_height = 25
    total_height = len(thinking_time_history) * line_height
    max_scroll = max(0, total_height - history_area.height)
    
    # Vẽ tiêu đề
    title = history_font.render("AI Thinking Time:", True, (0, 0, 0))
    screen.blit(title, (history_area.x + 5, history_area.y + 5))
    
    # Vẽ các dòng thời gian
    y = history_area.y + 30 - scroll_offset
    for i, time_value in enumerate(thinking_time_history):
        if y + line_height > history_area.y and y < history_area.y + history_area.height:
            text = history_font.render(f"Move {i+1}: {time_value:.2f}s", True, (0, 0, 0))
            screen.blit(text, (history_area.x + 5, y))
        y += line_height

def make_ai_move():
    """Thực hiện nước đi của AI"""
    global board, current_player, check, w_king_pos, b_king_pos
    
    # Hiển thị thông báo "AI đang suy nghĩ"
    text = message_font.render("AI is thinking...", True, (0, 0, 255))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    # Vẽ nền mờ cho toàn màn hình
    overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    # Vẽ thông báo
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    # Đo thời gian suy nghĩ
    start_time = time.time()
    
    # Lấy nước đi tốt nhất từ AI
    best_move = get_best_move(board, current_player, depth=3)
    
    # Tính thời gian suy nghĩ
    thinking_time = time.time() - start_time
    thinking_time_history.append(thinking_time)
    
    if best_move:
        start_pos, end_pos = best_move
        start_col, start_row = start_pos
        end_col, end_row = end_pos
        
        # Lưu trạng thái trước khi thực hiện nước đi
        save_state_to_history()
        
        # Thực hiện nước đi
        piece = board[start_row][start_col]
        if piece:  # Kiểm tra piece không phải None
            board[start_row][start_col] = None
            board[end_row][end_col] = piece
            
            # Cập nhật vị trí vua nếu cần
            update_king_positions()
            
            # Đổi lượt chơi
            current_player = "white"
            
            # Kiểm tra chiếu sau khi di chuyển
            if check_valid_move.is_check(board, current_player):
                if check_valid_move.is_checkmate(board, current_player):
                    # Hiển thị thông báo chiếu hết
                    text = message_font.render("AI wins!", True, (255, 0, 0))
                    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                    # Vẽ nền mờ cho toàn màn hình
                    overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 128))
                    screen.blit(overlay, (0, 0))
                    # Vẽ thông báo
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    # Reset bàn cờ và bắt đầu ván mới
                    reset_board()
                else:
                    # Hiển thị thông báo chiếu
                    king_pos = w_king_pos
                    s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                    s.fill(RED)
                    screen.blit(s, (king_pos[0] * SQ_SIZE, king_pos[1] * SQ_SIZE))
                    pygame.display.flip()
                    text = message_font.render("Check!", True, (255, 0, 0))
                    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(750)
                    check = True
            elif check:
                check = False
            
            # Vẽ lại bàn cờ
            draw_board()
            draw_highlight()
            draw_pieces()
            pygame.display.flip()

def handle_move(start_pos, end_pos):
    """
    Xử lý nước đi và kiểm tra các điều kiện
    Returns: (is_valid, should_continue)
    """
    global board, current_player, check, selected_piece, valid_moves
    
    if not start_pos or not end_pos:
        return False, True
        
    start_col, start_row = start_pos
    end_col, end_row = end_pos
    
    # Kiểm tra vị trí hợp lệ
    if not (0 <= start_col < 8 and 0 <= start_row < 8 and 0 <= end_col < 8 and 0 <= end_row < 8):
        return False, True
        
    # Lấy quân cờ
    piece = board[start_row][start_col]
    if not piece:
        return False, True
    
    # Xử lý nhập thành
    if "king" in piece and abs(end_col - start_col) > 1:
        # Nhập thành bên phải
        if end_col > start_col:
            # Di chuyển vua
            board[start_row][start_col] = None
            board[end_row][end_col] = piece
            # Di chuyển xe
            rook = board[start_row][7]
            board[start_row][7] = None
            board[start_row][end_col - 1] = rook
        # Nhập thành bên trái
        else:
            # Di chuyển vua
            board[start_row][start_col] = None
            board[end_row][end_col] = piece
            # Di chuyển xe
            rook = board[start_row][0]
            board[start_row][0] = None
            board[start_row][end_col + 1] = rook
            
        # Cập nhật vị trí vua
        update_king_positions()
        
        # Đổi lượt chơi
        current_player = "black" if current_player == "white" else "white"
        
        # Kiểm tra chiếu
        if check_valid_move.is_check(board, current_player):
            if check_valid_move.is_checkmate(board, current_player):
                # Hiển thị thông báo chiếu hết
                text = message_font.render("AI wins!" if current_player == "white" else "You win!", True, (255, 0, 0))
                text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                screen.blit(overlay, (0, 0))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)
                reset_board()
                return False, True
            else:
                # Hiển thị thông báo chiếu
                king_pos = w_king_pos if current_player == "white" else b_king_pos
                s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                s.fill(RED)
                screen.blit(s, (king_pos[0] * SQ_SIZE, king_pos[1] * SQ_SIZE))
                pygame.display.flip()
                text = message_font.render("Check!", True, (255, 0, 0))
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
        
        return True, True
    
    # Tạo bản sao của bàn cờ để kiểm tra nước đi
    temp_board = [row[:] for row in board]
    temp_board[start_row][start_col] = None
    temp_board[end_row][end_col] = piece
    
    # Kiểm tra nếu nước đi sẽ khiến vua bị chiếu
    if check_valid_move.is_check(temp_board, current_player):
        return False, True
    
    # Lưu trạng thái trước khi thực hiện nước đi
    save_state_to_history()
    
    # Thực hiện nước đi
    board[start_row][start_col] = None
    board[end_row][end_col] = piece
    
    # Cập nhật vị trí vua
    update_king_positions()
    
    # Kiểm tra phong quân
    if "pawn" in piece:
        if (current_player == "white" and end_row == 0) or (current_player == "black" and end_row == 7):
            return True, False  # Cần phong quân
    
    # Đổi lượt chơi
    current_player = "black" if current_player == "white" else "white"
    
    # Kiểm tra chiếu
    if check_valid_move.is_check(board, current_player):
        if check_valid_move.is_checkmate(board, current_player):
            # Hiển thị thông báo chiếu hết
            text = message_font.render("AI wins!" if current_player == "white" else "You win!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            reset_board()
            return False, True
        else:
            # Hiển thị thông báo chiếu
            king_pos = w_king_pos if current_player == "white" else b_king_pos
            s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
            s.fill(RED)
            screen.blit(s, (king_pos[0] * SQ_SIZE, king_pos[1] * SQ_SIZE))
            pygame.display.flip()
            text = message_font.render("Check!", True, (255, 0, 0))
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
    
    return True, True

def execute_move(start_pos, end_pos):
    """
    Thực hiện nước đi và cập nhật bàn cờ
    Returns: True nếu nước đi thành công
    """
    global board, current_player
    
    if not start_pos or not end_pos:
        return False
        
    start_col, start_row = start_pos
    end_col, end_row = end_pos
    
    # Kiểm tra vị trí hợp lệ
    if not (0 <= start_col < 8 and 0 <= start_row < 8 and 0 <= end_col < 8 and 0 <= end_row < 8):
        return False
        
    # Lấy quân cờ
    piece = board[start_row][start_col]
    if not piece:
        return False
        
    # Thực hiện nước đi
    board[start_row][start_col] = None
    board[end_row][end_col] = piece
    
    # Cập nhật vị trí vua nếu cần
    update_king_positions()
    
    return True

def main_ai():
    global selected_piece, valid_moves, current_player, check, w_king_pos, b_king_pos, promotion_piece, save_button, load_button, move_history, board, scroll_offset
    running = True
    count_draw = 0
    promotion_pos = None
    game_started = False
    move_history = []
    thinking_time_history.clear()  # Xóa lịch sử thời gian khi bắt đầu game mới

    # Thêm nút Start Game
    start_button = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 - 30, 200, 60)
    start_font = pygame.font.Font(None, 48)

    # Tạo surface mới cho toàn bộ màn hình (bao gồm cả phần nút)
    full_screen = pygame.display.set_mode((screen_width, HEIGHT))
    pygame.display.set_caption("Cờ Vua AI")

    while running:
        # Vẽ bàn cờ
        draw_board()
        draw_highlight()
        draw_pieces()
        
        if not game_started:
            # Vẽ nền mờ cho toàn màn hình
            overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Màu đen với độ trong suốt
            full_screen.blit(overlay, (0, 0))
            
            # Vẽ nút Start Game
            pygame.draw.rect(full_screen, (50, 205, 50), start_button)  # Màu xanh lá
            pygame.draw.rect(full_screen, (0, 0, 0), start_button, 3)  # Viền đen
            start_text = start_font.render("Start Game", True, (255, 255, 255))
            text_rect = start_text.get_rect(center=start_button.center)
            full_screen.blit(start_text, text_rect)
        else:
            # Vẽ nút Save và Load
            pygame.draw.rect(full_screen, (50, 205, 50), save_button)  # Màu xanh lá
            pygame.draw.rect(full_screen, (0, 0, 0), save_button, 2)  # Viền đen
            pygame.draw.rect(full_screen, (50, 205, 50), load_button)  # Màu xanh lá
            pygame.draw.rect(full_screen, (0, 0, 0), load_button, 2)  # Viền đen
            save_text = button_font.render("Save", True, (255, 255, 255))
            load_text = button_font.render("Load", True, (255, 255, 255))
            full_screen.blit(save_text, (save_button.x + 20, save_button.y + 5))
            full_screen.blit(load_text, (load_button.x + 20, load_button.y + 5))
        
        # Vẽ menu phong quân nếu cần
        if promotion_pos:
            row, col = promotion_pos
            draw_promotion_menu(row, col)
        
        # Vẽ màn hình hiển thị thời gian suy nghĩ
        if game_started:
            draw_thinking_time_history()
        
        pygame.display.flip()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                # Xử lý sự kiện Ctrl+Z để undo
                if game_started and event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if move_history:
                        # Lấy ra trạng thái trước đó
                        previous_state = move_history.pop()
                        
                        # Khôi phục trạng thái
                        board = previous_state['board']
                        current_player = previous_state['current_player']
                        check = previous_state['check']
                        w_king_pos = previous_state['w_king_pos']
                        b_king_pos = previous_state['b_king_pos']
                        check_valid_move.white_king_moved = previous_state['white_king_moved']
                        check_valid_move.black_king_moved = previous_state['black_king_moved']
                        
                        # Reset lựa chọn
                        selected_piece = None
                        valid_moves = []
                        
                        # Hiển thị thông báo đã undo
                        text = message_font.render("Đã hoàn tác", True, (0, 255, 255))
                        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                        
                        # Vẽ nền mờ
                        overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 128))
                        full_screen.blit(overlay, (0, 0))
                        
                        # Vẽ thông báo
                        full_screen.blit(text, text_rect)
                        pygame.display.flip()
                        pygame.time.wait(750)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                if not game_started:
                    # Kiểm tra click vào nút Start Game
                    if start_button.collidepoint(mx, my):
                        game_started = True
                        continue
                else:
                    # Kiểm tra click vào nút Save
                    if save_button.collidepoint(mx, my):
                        if save_game():
                            text = message_font.render("Game Saved!", True, (0, 255, 0))
                        else:
                            text = message_font.render("Save Failed!", True, (255, 0, 0))
                        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                        # Vẽ nền mờ cho toàn màn hình
                        overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 128))
                        full_screen.blit(overlay, (0, 0))
                        # Vẽ thông báo
                        full_screen.blit(text, text_rect)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        continue
                        
                    # Kiểm tra click vào nút Load
                    if load_button.collidepoint(mx, my):
                        if load_game():
                            text = message_font.render("Game Loaded!", True, (0, 255, 0))
                            selected_piece = None
                            valid_moves = []
                            # Reset lịch sử nước đi khi load game
                            move_history = []
                        else:
                            text = message_font.render("Load Failed!", True, (255, 0, 0))
                        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                        # Vẽ nền mờ cho toàn màn hình
                        overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 128))
                        full_screen.blit(overlay, (0, 0))
                        # Vẽ thông báo
                        full_screen.blit(text, text_rect)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        continue

                if not game_started:
                    continue

                # Chỉ cho phép người chơi đi quân trắng
                if current_player != "white":
                    continue

                col, row = mx // SQ_SIZE, my // SQ_SIZE
                
                # Kiểm tra click có nằm trong phạm vi bàn cờ không
                if col < 0 or col >= 8 or row < 0 or row >= 8:
                    continue

                # Xử lý phong quân nếu đang trong trạng thái phong quân
                if promotion_pos:
                    if handle_promotion(promotion_pos[0], promotion_pos[1]):
                        # Lưu trạng thái trước khi thực hiện phong quân
                        save_state_to_history()
                        
                        # Thực hiện phong quân
                        board[promotion_pos[0]][promotion_pos[1]] = promotion_piece
                        promotion_pos = None
                        promotion_piece = None
                        # Đổi lượt chơi
                        current_player = "black"
                        
                        # Kiểm tra chiếu sau khi phong quân
                        if check_valid_move.is_check(board, current_player):
                            if check_valid_move.is_checkmate(board, current_player):
                                # Hiển thị thông báo chiếu hết
                                text = message_font.render("AI wins!", True, (255, 0, 0))
                                text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                                # Vẽ nền mờ cho toàn màn hình
                                overlay = pygame.Surface((screen_width, HEIGHT), pygame.SRCALPHA)
                                overlay.fill((0, 0, 0, 128))
                                full_screen.blit(overlay, (0, 0))
                                # Vẽ thông báo
                                full_screen.blit(text, text_rect)
                                pygame.display.flip()
                                pygame.time.wait(2000)
                                # Reset bàn cờ và bắt đầu ván mới
                                reset_board()
                                continue
                            else:
                                # Hiển thị thông báo chiếu
                                king_pos = b_king_pos
                                s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                                s.fill(RED)
                                screen.blit(s, (king_pos[0] * SQ_SIZE, king_pos[1] * SQ_SIZE))
                                pygame.display.flip()
                                text = message_font.render("Check!", True, (255, 0, 0))
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
                        
                        # Vẽ lại bàn cờ để hiển thị nước đi của người chơi
                        draw_board()
                        draw_highlight()
                        draw_pieces()
                        pygame.display.flip()
                        
                        # Đợi một chút để người chơi thấy nước đi của mình
                        pygame.time.wait(1000)
                        
                        # Thực hiện nước đi của AI
                        make_ai_move()

                # Click vào quân cờ
                if board[row][col]:
                    piece_color = get_piece_color(board[row][col])
                    if piece_color == current_player:
                        # Nếu click vào quân cờ khác, cập nhật selected_piece và valid_moves
                        if selected_piece is None or selected_piece != (col, row):
                            selected_piece = (col, row)
                            update_valid_moves()
                        # Nếu click lại vào quân cờ đã chọn, bỏ chọn
                        else:
                            selected_piece = None
                            valid_moves = []
                    elif selected_piece and check_valid_move.can_capture(board, selected_piece, (col, row)):
                        # Xử lý nước đi ăn quân
                        is_valid, should_continue = handle_move(selected_piece, (col, row))
                        if not should_continue:
                            promotion_pos = (row, col)
                            continue
                        
                        if is_valid:
                            # Vẽ lại bàn cờ
                            draw_board()
                            draw_highlight()
                            draw_pieces()
                            pygame.display.flip()
                            
                            # Đợi một chút
                            pygame.time.wait(1000)
                            
                            # Thực hiện nước đi của AI
                            make_ai_move()

                # Click vào ô trống
                elif selected_piece:
                    if (col, row) in valid_moves:
                        # Xử lý nước đi
                        is_valid, should_continue = handle_move(selected_piece, (col, row))
                        if not should_continue:
                            promotion_pos = (row, col)
                            continue
                        
                        if is_valid:
                            # Vẽ lại bàn cờ
                            draw_board()
                            draw_highlight()
                            draw_pieces()
                            pygame.display.flip()
                            
                            # Đợi một chút
                            pygame.time.wait(1000)
                            
                            # Thực hiện nước đi của AI
                            make_ai_move()

            elif event.type == pygame.MOUSEWHEEL:
                # Xử lý sự kiện cuộn chuột
                if game_started and history_area.collidepoint(pygame.mouse.get_pos()):
                    scroll_offset = max(0, min(scroll_offset - event.y * 30, max_scroll))

    pygame.quit()

if __name__ == "__main__":
    main_ai() 