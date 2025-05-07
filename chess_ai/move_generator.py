import check_valid_move

def get_all_valid_moves(board, current_player):
    """Lấy tất cả các nước đi hợp lệ cho người chơi hiện tại"""
    valid_moves = []
    
    # Duyệt qua tất cả các ô trên bàn cờ
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.startswith(current_player):
                # Duyệt qua tất cả các ô có thể đi
                for target_row in range(8):
                    for target_col in range(8):
                        if check_valid_move.is_valid_move(board, (col, row), (target_col, target_row)):
                            # Tạo bản sao của bàn cờ để kiểm tra nước đi
                            temp_board = [r[:] for r in board]
                            temp_board[row][col] = None
                            temp_board[target_row][target_col] = piece
                            
                            # Kiểm tra nước đi có khiến bị chiếu không
                            if not check_valid_move.is_check(temp_board, current_player):
                                valid_moves.append(((col, row), (target_col, target_row)))
    
    return valid_moves

def get_piece_moves(board, start_pos):
    """Lấy tất cả các nước đi hợp lệ cho một quân cờ"""
    col, row = start_pos
    piece = board[row][col]
    if not piece:
        return []
        
    current_player = "white" if piece.startswith("white") else "black"
    valid_moves = []
    
    # Duyệt qua tất cả các ô có thể đi
    for target_row in range(8):
        for target_col in range(8):
            if check_valid_move.is_valid_move(board, start_pos, (target_col, target_row)):
                # Tạo bản sao của bàn cờ để kiểm tra nước đi
                temp_board = [r[:] for r in board]
                temp_board[row][col] = None
                temp_board[target_row][target_col] = piece
                
                # Kiểm tra nước đi có khiến bị chiếu không
                if not check_valid_move.is_check(temp_board, current_player):
                    valid_moves.append((target_col, target_row))
    
    return valid_moves
