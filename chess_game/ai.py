# ai.py

def evaluate_board(white_pieces, white_locations, black_pieces, black_locations):
    piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 1000}
    value = 0

    for piece, location in zip(white_pieces, white_locations):
        value += piece_values[piece]

    for piece, location in zip(black_pieces, black_locations):
        value -= piece_values[piece]

    return value

def minimax(depth, alpha, beta, maximizing_player, white_pieces, white_locations, black_pieces, black_locations):
    if depth == 0 or game_over(white_pieces, white_locations, black_pieces, black_locations):
        return evaluate_board(white_pieces, white_locations, black_pieces, black_locations)

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_all_moves('white', white_pieces, white_locations, black_pieces, black_locations):
            new_white_pieces, new_white_locations, new_black_pieces, new_black_locations = apply_move(*move, white_pieces, white_locations, black_pieces, black_locations)
            evaluation = minimax(depth - 1, alpha, beta, False, new_white_pieces, new_white_locations, new_black_pieces, new_black_locations)
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_all_moves('black', white_pieces, white_locations, black_pieces, black_locations):
            new_white_pieces, new_white_locations, new_black_pieces, new_black_locations = apply_move(*move, white_pieces, white_locations, black_pieces, black_locations)
            evaluation = minimax(depth - 1, alpha, beta, True, new_white_pieces, new_white_locations, new_black_pieces, new_black_locations)
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(white_pieces, white_locations, black_pieces, black_locations):
    best_move = None
    best_value = float('inf')

    for move in get_all_moves('black', white_pieces, white_locations, black_pieces, black_locations):
        new_white_pieces, new_white_locations, new_black_pieces, new_black_locations = apply_move(*move, white_pieces, white_locations, black_pieces, black_locations)
        move_value = minimax(3, float('-inf'), float('inf'), True, new_white_pieces, new_white_locations, new_black_pieces, new_black_locations)
        if move_value < best_value:
            best_value = move_value
            best_move = move

    return best_move

def get_all_moves(color, white_pieces, white_locations, black_pieces, black_locations):
    moves = []
    pawn_locations = []

    if color == 'black':
        pawn_locations = [loc for piece, loc in zip(black_pieces, black_locations) if piece == 'pawn']
        for idx, (piece, loc) in enumerate(zip(black_pieces, black_locations)):
            if piece == 'pawn':
                moves.extend(get_pawn_moves(loc, 'black', white_locations, black_locations))
            elif piece == 'rook':
                moves.extend(get_rook_moves(loc, 'black', white_locations, black_locations))
            elif piece == 'knight':
                moves.extend(get_knight_moves(loc, 'black', white_locations, black_locations))
            elif piece == 'bishop':
                moves.extend(get_bishop_moves(loc, 'black', white_locations, black_locations))
            elif piece == 'queen':
                moves.extend(get_queen_moves(loc, 'black', white_locations, black_locations))
            elif piece == 'king':
                moves.extend(get_king_moves(loc, 'black', white_locations, black_locations))
    elif color == 'white':
        pawn_locations = [loc for piece, loc in zip(white_pieces, white_locations) if piece == 'pawn']
        for idx, (piece, loc) in enumerate(zip(white_pieces, white_locations)):
            if piece == 'pawn':
                moves.extend(get_pawn_moves(loc, 'white', white_locations, black_locations))
            elif piece == 'rook':
                moves.extend(get_rook_moves(loc, 'white', white_locations, black_locations))
            elif piece == 'knight':
                moves.extend(get_knight_moves(loc, 'white', white_locations, black_locations))
            elif piece == 'bishop':
                moves.extend(get_bishop_moves(loc, 'white', white_locations, black_locations))
            elif piece == 'queen':
                moves.extend(get_queen_moves(loc, 'white', white_locations, black_locations))
            elif piece == 'king':
                moves.extend(get_king_moves(loc, 'white', white_locations, black_locations))
    
    # Filter out moves that land on the same color pawn
    if color == 'black':
        occupied_locations = black_locations  # All locations occupied by black pieces
    elif color == 'white':
        occupied_locations = white_locations  # All locations occupied by white pieces

    moves = [move for move in moves if move[2] not in occupied_locations]

    return moves


def apply_move(start, piece, end, white_pieces, white_locations, black_pieces, black_locations):
    print(f"Applying move: {piece} from {start} to {end}")
    new_white_pieces = white_pieces[:]
    new_white_locations = white_locations[:]
    new_black_pieces = black_pieces[:]
    new_black_locations = black_locations[:]

    if piece in black_pieces:
        if start not in black_locations:
            print(f"Error: {start} not in black_locations: {black_locations}")
            return white_pieces, white_locations, black_pieces, black_locations
        idx = black_locations.index(start)
        new_black_locations[idx] = end
        if end in white_locations:
            capture_idx = white_locations.index(end)
            new_white_pieces.pop(capture_idx)
            new_white_locations.pop(capture_idx)
    else:
        if start not in white_locations:
            print(f"Error: {start} not in white_locations: {white_locations}")
            return white_pieces, white_locations, black_pieces, black_locations
        idx = white_locations.index(start)
        new_white_locations[idx] = end
        if end in black_locations:
            capture_idx = black_locations.index(end)
            new_black_pieces.pop(capture_idx)
            new_black_locations.pop(capture_idx)

    return new_white_pieces, new_white_locations, new_black_pieces, new_black_locations

def game_over(white_pieces, white_locations, black_pieces, black_locations):
    if 'king' not in white_pieces or 'king' not in black_pieces:
        return True
    return False

def get_pawn_moves(location, color, white_locations, black_locations):
    moves = []
    x, y = location
    if color == 'white':
        if (x, y + 1) not in white_locations + black_locations and y + 1 < 8:
            moves.append(((x, y), 'pawn', (x, y + 1)))
        if (x, y + 2) not in white_locations + black_locations and y == 1:
            moves.append(((x, y), 'pawn', (x, y + 2)))
        if (x + 1, y + 1) in black_locations:
            moves.append(((x, y), 'pawn', (x + 1, y + 1)))
        if (x - 1, y + 1) in black_locations:
            moves.append(((x, y), 'pawn', (x - 1, y + 1)))
    else:
        if (x, y - 1) not in white_locations + black_locations and y - 1 >= 0:
            moves.append(((x, y), 'pawn', (x, y - 1)))
        if (x, y - 2) not in white_locations + black_locations and y == 6:
            moves.append(((x, y), 'pawn', (x, y - 2)))
        if (x + 1, y - 1) in white_locations:
            moves.append(((x, y), 'pawn', (x + 1, y - 1)))
        if (x - 1, y - 1) in white_locations:
            moves.append(((x, y), 'pawn', (x - 1, y - 1)))
    return moves

def get_rook_moves(location, color, white_locations, black_locations):
    moves = []
    x, y = location
    for i in range(1, 8):
        if (x + i, y) not in white_locations + black_locations and x + i < 8:
            moves.append(((x, y), 'rook', (x + i, y)))
        elif (x + i, y) in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'rook', (x + i, y)))
            break
        else:
            break
    for i in range(1, 8):
        if (x - i, y) not in white_locations + black_locations and x - i >= 0:
            moves.append(((x, y), 'rook', (x - i, y)))
        elif (x - i, y) in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'rook', (x - i, y)))
            break
        else:
            break
    for i in range(1, 8):
        if (x, y + i) not in white_locations + black_locations and y + i < 8:
            moves.append(((x, y), 'rook', (x, y + i)))
        elif (x, y + i) in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'rook', (x, y + i)))
            break
        else:
            break
    for i in range(1, 8):
        if (x, y - i) not in white_locations + black_locations and y - i >= 0:
            moves.append(((x, y), 'rook', (x, y - i)))
        elif (x, y - i) in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'rook', (x, y - i)))
            break
        else:
            break
    return moves

def get_knight_moves(location, color, white_locations, black_locations):
    moves = []
    x, y = location
    possible_moves = [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                      (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]
    for move in possible_moves:
        if move not in white_locations + black_locations and 0 <= move[0] < 8 and 0 <= move[1] < 8:
            moves.append(((x, y), 'knight', move))
        elif move in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'knight', move))
    return moves

def get_bishop_moves(location, color, white_locations, black_locations):
    moves = []
    x, y = location
    for i in range(1, 8):
        if (x + i, y + i) not in white_locations + black_locations and x + i < 8 and y + i < 8:
            moves.append(((x, y), 'bishop', (x + i, y + i)))
        elif (x + i, y + i) in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'bishop', (x + i, y + i)))
            break
        else:
            break
    for i in range(1, 8):
        if (x - i, y + i) not in white_locations + black_locations and x - i >= 0 and y + i < 8:
            moves.append(((x, y), 'bishop', (x - i, y + i)))
        elif (x - i, y + i) in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'bishop', (x - i, y + i)))
            break
        else:
            break
    for i in range(1, 8):
        if (x + i, y - i) not in white_locations + black_locations and x + i < 8 and y - i >= 0:
            moves.append(((x, y), 'bishop', (x + i, y - i)))
        elif (x + i, y - i) in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'bishop', (x + i, y - i)))
            break
        else:
            break
    for i in range(1, 8):
        if (x - i, y - i) not in white_locations + black_locations and x - i >= 0 and y - i >= 0:
            moves.append(((x, y), 'bishop', (x - i, y - i)))
        elif (x - i, y - i) in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'bishop', (x - i, y - i)))
            break
        else:
            break
    return moves

def get_queen_moves(location, color, white_locations, black_locations):
    return get_rook_moves(location, color, white_locations, black_locations) + get_bishop_moves(location, color, white_locations, black_locations)

def get_king_moves(location, color, white_locations, black_locations):
    moves = []
    x, y = location
    possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                      (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]
    for move in possible_moves:
        if move not in white_locations + black_locations and 0 <= move[0] < 8 and 0 <= move[1] < 8:
            moves.append(((x, y), 'king', move))
        elif move in black_locations if color == 'white' else white_locations:
            moves.append(((x, y), 'king', move))
    return moves
