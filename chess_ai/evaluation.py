"""
Module chứa các hàm đánh giá cho chess AI
"""

# Giá trị cơ bản của các quân cờ
PIECE_VALUES = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 0  # Vua không có giá trị cố định vì không thể bị ăn
}

# Bảng điểm vị trí cho tốt (pawn)
PAWN_POSITION_VALUES = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

# Bảng điểm vị trí cho mã (knight)
KNIGHT_POSITION_VALUES = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

# Bảng điểm vị trí cho tượng (bishop)
BISHOP_POSITION_VALUES = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

# Bảng điểm vị trí cho xe (rook)
ROOK_POSITION_VALUES = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

# Bảng điểm vị trí cho hậu (queen)
QUEEN_POSITION_VALUES = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

# Bảng điểm vị trí cho vua (king)
KING_POSITION_VALUES = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

def get_piece_value(piece_name):
    """Lấy giá trị cơ bản của quân cờ"""
    if piece_name is None:
        return 0
    piece_type = piece_name.split('_')[1]  # Lấy phần sau dấu gạch dưới
    return PIECE_VALUES.get(piece_type, 0)

def get_position_value(piece_name, row, col):
    """Lấy giá trị vị trí của quân cờ"""
    if piece_name is None:
        return 0
    
    piece_type = piece_name.split('_')[1]
    position_tables = {
        'pawn': PAWN_POSITION_VALUES,
        'knight': KNIGHT_POSITION_VALUES,
        'bishop': BISHOP_POSITION_VALUES,
        'rook': ROOK_POSITION_VALUES,
        'queen': QUEEN_POSITION_VALUES,
        'king': KING_POSITION_VALUES
    }
    
    table = position_tables.get(piece_type)
    if table is None:
        return 0
        
    # Đảo ngược bảng nếu là quân đen
    if piece_name.startswith('black_'):
        row = 7 - row
        col = 7 - col
        
    return table[row][col]

def evaluate_board(board, current_player):
    """
    Đánh giá tổng thể bàn cờ
    Returns: Giá trị dương nếu thế cờ có lợi cho current_player, âm nếu bất lợi
    """
    score = 0
    
    # Đánh giá từng quân cờ
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is None:
                continue
                
            # Lấy giá trị cơ bản và giá trị vị trí
            piece_value = get_piece_value(piece)
            position_value = get_position_value(piece, row, col)
            
            # Cộng điểm nếu là quân của current_player, trừ điểm nếu là quân đối phương
            if piece.startswith(current_player + '_'):
                score += piece_value + position_value
            else:
                score -= piece_value + position_value
    
    return score 