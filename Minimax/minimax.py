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

def order_moves(moves, board, current_player):
    """
    Sắp xếp các nước đi theo thứ tự ưu tiên để tối ưu alpha-beta pruning
    """
    scored_moves = []
    for start_pos, end_pos in moves:
        score = 0
        start_col, start_row = start_pos
        end_col, end_row = end_pos
        
        # Ưu tiên nước ăn quân
        if board[end_row][end_col]:
            score += 10
            
        # Ưu tiên nước đi vào trung tâm
        center_distance = abs(3.5 - end_col) + abs(3.5 - end_row)
        score += (7 - center_distance)
        
        # Ưu tiên nước đi của quân có giá trị cao
        piece = board[start_row][start_col]
        if piece:
            if "queen" in piece:
                score += 5
            elif "rook" in piece:
                score += 4
            elif "bishop" in piece or "knight" in piece:
                score += 3
            elif "pawn" in piece:
                score += 2
                
        scored_moves.append((score, (start_pos, end_pos)))
    
    # Sắp xếp theo điểm số giảm dần
    scored_moves.sort(reverse=True)
    return [move for _, move in scored_moves]

def minimax(board, depth, alpha, beta, is_maximizing, current_player):
    """
    Thuật toán Minimax với Fail-Soft Alpha-Beta Pruning
    Args:
        board: Bàn cờ hiện tại
        depth: Độ sâu tìm kiếm
        alpha: Giá trị alpha cho alpha-beta pruning
        beta: Giá trị beta cho alpha-beta pruning
        is_maximizing: True nếu là lượt của người chơi tối đa hóa điểm
        current_player: Người chơi hiện tại ('white' hoặc 'black')
    Returns:
        (best_score, best_move)
    """
    if depth == 0:
        return evaluate_board(board, current_player), None
    
    valid_moves = get_all_valid_moves(board, current_player)
    
    if not valid_moves:
        return evaluate_board(board, current_player), None
    
    # Sắp xếp các nước đi để tối ưu alpha-beta pruning
    ordered_moves = order_moves(valid_moves, board, current_player)
    
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        
        for start_pos, end_pos in ordered_moves:
            # Thực hiện nước đi
            new_board = make_move(board, start_pos, end_pos)
            
            # Đổi người chơi
            next_player = 'black' if current_player == 'white' else 'white'
            
            # Gọi đệ quy với fail-soft
            score, _ = minimax(new_board, depth - 1, alpha, beta, False, next_player)
            
            if score > best_score:
                best_score = score
                best_move = (start_pos, end_pos)
            
            # Fail-soft: cập nhật alpha ngay cả khi bị cắt tỉa
            alpha = max(alpha, score)
            if beta <= alpha:
                break
                
        return best_score, best_move
        
    else:
        best_score = float('inf')
        best_move = None
        
        for start_pos, end_pos in ordered_moves:
            # Thực hiện nước đi
            new_board = make_move(board, start_pos, end_pos)
            
            # Đổi người chơi
            next_player = 'black' if current_player == 'white' else 'white'
            
            # Gọi đệ quy với fail-soft
            score, _ = minimax(new_board, depth - 1, alpha, beta, True, next_player)
            
            if score < best_score:
                best_score = score
                best_move = (start_pos, end_pos)
            
            # Fail-soft: cập nhật beta ngay cả khi bị cắt tỉa
            beta = min(beta, score)
            if beta <= alpha:
                break
                
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
    # AI luôn là quân đen, nên luôn là minimizing player
    _, best_move = minimax(board, depth, float('-inf'), float('inf'), False, current_player)
    return best_move 