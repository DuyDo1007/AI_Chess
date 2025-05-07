# Giá trị của các quân cờ
PIECE_VALUES = {
    'white_pawn': 100,
    'white_knight': 320,
    'white_bishop': 330,
    'white_rook': 500,
    'white_queen': 900,
    'white_king': 20000,
    'black_pawn': -100,
    'black_knight': -320,
    'black_bishop': -330,
    'black_rook': -500,
    'black_queen': -900,
    'black_king': -20000
}

# Bảng điểm vị trí cho tốt
PAWN_POSITION_SCORES = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

# Bảng điểm vị trí cho mã
KNIGHT_POSITION_SCORES = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

# Bảng điểm vị trí cho tượng
BISHOP_POSITION_SCORES = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

# Bảng điểm vị trí cho xe
ROOK_POSITION_SCORES = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

# Bảng điểm vị trí cho hậu
QUEEN_POSITION_SCORES = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

# Bảng điểm vị trí cho vua
KING_POSITION_SCORES = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

def get_piece_position_score(piece, row, col):
    """Lấy điểm vị trí cho một quân cờ"""
    if piece is None:
        return 0
        
    if piece.startswith('white_'):
        if 'pawn' in piece:
            return PAWN_POSITION_SCORES[row][col]
        elif 'knight' in piece:
            return KNIGHT_POSITION_SCORES[row][col]
        elif 'bishop' in piece:
            return BISHOP_POSITION_SCORES[row][col]
        elif 'rook' in piece:
            return ROOK_POSITION_SCORES[row][col]
        elif 'queen' in piece:
            return QUEEN_POSITION_SCORES[row][col]
        elif 'king' in piece:
            return KING_POSITION_SCORES[row][col]
    else:
        if 'pawn' in piece:
            return -PAWN_POSITION_SCORES[7-row][col]
        elif 'knight' in piece:
            return -KNIGHT_POSITION_SCORES[7-row][col]
        elif 'bishop' in piece:
            return -BISHOP_POSITION_SCORES[7-row][col]
        elif 'rook' in piece:
            return -ROOK_POSITION_SCORES[7-row][col]
        elif 'queen' in piece:
            return -QUEEN_POSITION_SCORES[7-row][col]
        elif 'king' in piece:
            return -KING_POSITION_SCORES[7-row][col]
    
    return 0

def evaluate_board(board, current_player):
    """
    Đánh giá bàn cờ
    Returns: Điểm số (dương nếu tốt cho người chơi hiện tại, âm nếu không tốt)
    """
    score = 0
    
    # Tính điểm dựa trên giá trị quân cờ và vị trí
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                # Cộng điểm giá trị quân cờ
                score += PIECE_VALUES[piece]
                # Cộng điểm vị trí
                score += get_piece_position_score(piece, row, col)
    
    # Nếu là lượt của quân đen, đảo ngược điểm số
    if current_player == 'black':
        score = -score
        
    return score 