def get_piece_info(piece):
    """Lấy thông tin về quân cờ từ tên file"""
    if piece is None:
        return None, None
    
    # Lấy tên file từ hình ảnh
    filename = str(piece)
    
    # Xác định màu và loại quân cờ
    if filename.startswith("w_"):
        color = "white"
    elif filename.startswith("b_"):
        color = "black"
    else:
        return None, None
        
    if "pawn" in filename:
        piece_type = "pawn"
    elif "rook" in filename:
        piece_type = "rook"
    elif "knight" in filename:
        piece_type = "knight"
    elif "bishop" in filename:
        piece_type = "bishop"
    elif "queen" in filename:
        piece_type = "queen"
    elif "king" in filename:
        piece_type = "king"
    else:
        return None, None
        
    return color, piece_type

def is_valid_pawn_move(board, start_pos, end_pos, piece):
    s_x, s_y = start_pos
    e_x, e_y = end_pos
    
    # Lấy thông tin về quân cờ
    piece_color, _ = get_piece_info(piece)
    if piece_color is None:
        return False
        
    # Tốt trắng đi lên (y giảm), tốt đen đi xuống (y tăng)
    direction = -1 if piece_color == "white" else 1

    # Di chuyển tiến 1 ô
    if s_x == e_x and e_y == s_y + direction and board[e_y][e_x] is None:
        return True

    # Di chuyển tiến 2 ô từ vị trí ban đầu
    if (s_x == e_x and e_y == s_y + 2 * direction and
            ((s_y == 1 and piece_color == "black") or (s_y == 6 and piece_color == "white")) and
            board[e_y][e_x] is None and board[s_y + direction][s_x] is None):
        return True

    # Ăn chéo
    if abs(e_x - s_x) == 1 and e_y == s_y + direction:
        target_piece = board[e_y][e_x]
        if target_piece is not None:
            target_color, _ = get_piece_info(target_piece)
            if target_color is not None and piece_color != target_color:
                return True

    return False

def is_valid_rook_move(board, start_pos, end_pos):
    s_x, s_y = start_pos
    e_x, e_y = end_pos

    # Xe chỉ di chuyển ngang hoặc dọc
    if s_x != e_x and s_y != e_y:
        return False

    # Kiểm tra các ô giữa
    step = 1 if e_x > s_x or e_y > s_y else -1
    if s_x == e_x:  # Di chuyển dọc
        for y in range(s_y + step, e_y, step):
            if board[y][s_x] is not None:
                return False
    else:  # Di chuyển ngang
        for x in range(s_x + step, e_x, step):
            if board[s_y][x] is not None:
                return False

    return True

def is_valid_knight_move(board, start_pos, end_pos):
    s_x, s_y = start_pos
    e_x, e_y = end_pos

    # Mã đi hình chữ L (2 ô một hướng và 1 ô hướng vuông góc)
    dx = abs(e_x - s_x)
    dy = abs(e_y - s_y)
    return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

def is_valid_bishop_move(board, start_pos, end_pos):
    s_x, s_y = start_pos
    e_x, e_y = end_pos

    # Tượng chỉ di chuyển chéo
    if abs(e_x - s_x) != abs(e_y - s_y):
        return False

    # Kiểm tra các ô giữa
    step_x = 1 if e_x > s_x else -1
    step_y = 1 if e_y > s_y else -1
    x, y = s_x + step_x, s_y + step_y
    while x != e_x and y != e_y:
        if board[y][x] is not None:
            return False
        x += step_x
        y += step_y

    return True

def is_valid_queen_move(board, start_pos, end_pos):
    return is_valid_rook_move(board, start_pos, end_pos) or is_valid_bishop_move(board, start_pos, end_pos)

def is_valid_king_move(board, start_pos, end_pos):
    s_x, s_y = start_pos
    e_x, e_y = end_pos

    # Vua di chuyển 1 ô theo mọi hướng
    return abs(e_x - s_x) <= 1 and abs(e_y - s_y) <= 1

def can_capture(board, start_pos, end_pos):
    """Kiểm tra xem quân cờ có thể ăn quân đối phương không"""
    s_x, s_y = start_pos
    e_x, e_y = end_pos
    
    # Lấy quân cờ tại vị trí bắt đầu và đích
    piece = board[s_y][s_x]
    target_piece = board[e_y][e_x]
    
    # Nếu không có quân cờ ở vị trí bắt đầu hoặc không có quân đối phương ở vị trí đích
    if piece is None or target_piece is None:
        return False
        
    # Lấy màu của quân cờ
    piece_color, _ = get_piece_info(piece)
    target_color, _ = get_piece_info(target_piece)
    
    # Kiểm tra xem có phải là quân đối phương không
    if piece_color is None or target_color is None or piece_color == target_color:
        return False
        
    # Kiểm tra nước đi hợp lệ
    return is_valid_move(board, start_pos, end_pos)

def is_valid_move(board, start_pos, end_pos):
    """Kiểm tra xem nước đi từ start_pos đến end_pos có hợp lệ không"""
    s_x, s_y = start_pos
    e_x, e_y = end_pos

    # Kiểm tra nếu vị trí bắt đầu hoặc kết thúc nằm ngoài bàn cờ
    if not (0 <= s_x < 8 and 0 <= s_y < 8 and 0 <= e_x < 8 and 0 <= e_y < 8):
        return False

    piece = board[s_y][s_x]  # Lấy quân cờ tại vị trí bắt đầu
    if piece is None:
        return False  # Không có quân nào ở vị trí bắt đầu

    # Kiểm tra nếu vị trí kết thúc trùng với vị trí bắt đầu
    if s_x == e_x and s_y == e_y:
        return False

    # Lấy thông tin về quân cờ
    piece_color, piece_type = get_piece_info(piece)
    if piece_color is None or piece_type is None:
        return False

    # Kiểm tra nếu đang ăn quân
    target_piece = board[e_y][e_x]
    if target_piece is not None:
        target_color, _ = get_piece_info(target_piece)
        if target_color is not None and piece_color == target_color:
            return False

    # Logic kiểm tra theo từng loại quân cờ
    if piece_type == "pawn":
        return is_valid_pawn_move(board, start_pos, end_pos, piece)
    elif piece_type == "rook":
        return is_valid_rook_move(board, start_pos, end_pos)
    elif piece_type == "knight":
        return is_valid_knight_move(board, start_pos, end_pos)
    elif piece_type == "bishop":
        return is_valid_bishop_move(board, start_pos, end_pos)
    elif piece_type == "queen":
        return is_valid_queen_move(board, start_pos, end_pos)
    elif piece_type == "king":
        return is_valid_king_move(board, start_pos, end_pos)

    return False  # Nếu không phải quân cờ hợp lệ