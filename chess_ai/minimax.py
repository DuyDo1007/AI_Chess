import copy
from .evaluation import evaluate_board
from .move_generator import get_all_valid_moves as get_moves

def get_all_valid_moves(board, current_player):
    """
    Lấy tất cả các nước đi hợp lệ cho người chơi hiện tại
    Returns: List các tuple (start_pos, end_pos)
    """
    return get_moves(board, current_player)

def make_move(board, start_pos, end_pos):
    """
    Thực hiện nước đi trên bàn cờ
    Returns: Bàn cờ mới sau khi thực hiện nước đi
    """
    new_board = copy.deepcopy(board)
    start_col, start_row = start_pos
    end_col, end_row = end_pos
    
    # Di chuyển quân cờ
    new_board[end_row][end_col] = new_board[start_row][start_col]
    new_board[start_row][start_col] = None
    
    return new_board

def minimax(board, depth, is_maximizing, current_player):
    """
    Thuật toán Minimax
    Args:
        board: Bàn cờ hiện tại
        depth: Độ sâu tìm kiếm
        is_maximizing: True nếu là lượt của người chơi tối đa hóa điểm
        current_player: Người chơi hiện tại ('white' hoặc 'black')
    Returns:
        (best_score, best_move)
    """
    if depth == 0:
        return evaluate_board(board, current_player), None
    
    valid_moves = get_all_valid_moves(board, current_player)
    
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        
        for start_pos, end_pos in valid_moves:
            # Thực hiện nước đi
            new_board = make_move(board, start_pos, end_pos)
            
            # Đổi người chơi
            next_player = 'black' if current_player == 'white' else 'white'
            
            # Gọi đệ quy
            score, _ = minimax(new_board, depth - 1, False, next_player)
            
            if score > best_score:
                best_score = score
                best_move = (start_pos, end_pos)
                
        return best_score, best_move
        
    else:
        best_score = float('inf')
        best_move = None
        
        for start_pos, end_pos in valid_moves:
            # Thực hiện nước đi
            new_board = make_move(board, start_pos, end_pos)
            
            # Đổi người chơi
            next_player = 'black' if current_player == 'white' else 'white'
            
            # Gọi đệ quy
            score, _ = minimax(new_board, depth - 1, True, next_player)
            
            if score < best_score:
                best_score = score
                best_move = (start_pos, end_pos)
                
        return best_score, best_move

def get_best_move(board, current_player, depth=3):
    """
    Tìm nước đi tốt nhất cho người chơi hiện tại
    Args:
        board: Bàn cờ hiện tại
        current_player: Người chơi hiện tại ('white' hoặc 'black')
        depth: Độ sâu tìm kiếm
    Returns:
        (start_pos, end_pos) hoặc None nếu không có nước đi hợp lệ
    """
    _, best_move = minimax(board, depth, True, current_player)
    return best_move 