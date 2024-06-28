def split_by_position(player_info, captures):
    top = []
    left = []
    right = []
    bottom = []

    ref_x, ref_y = player_info[1], player_info[2]

    for coord in captures:
        x, y = coord
        if x == ref_x:
            if y < ref_y:
                bottom.append(coord)
            elif y > ref_y:
                top.append(coord)
        elif y == ref_y:
            if x < ref_x:
                left.append(coord)
            elif x > ref_x:
                right.append(coord)

    return top, left, right, bottom

def get_nearest_pieces(top, left, right, bottom):
    nearest_pieces = []

    if top:
        nearest_pieces.append(min(top, key=lambda p: p[1]))
    if bottom:
        nearest_pieces.append(max(bottom, key=lambda p: p[1]))
    if left:
        nearest_pieces.append(max(left, key=lambda p: p[0]))
    if right:
        nearest_pieces.append(min(right, key=lambda p: p[0]))

    return nearest_pieces

def add_black_figure(board_state, position):
    column, row = position[0], position[1]

    if column < "a" or column > "h" or row < "1" or row > "8":
        print("Invalid position. The column must be a letter from 'a' to 'h' and the row must be a number from '1' to '8'.")
        return False

    column_index = ord(column) - ord('a')
    row_index = int(row) - 1

    if board_state[row_index][column_index] != " ":
        print("Invalid move. The position is already occupied.")
        return False

    # Place the black piece on the board
    board_state[row_index][column_index] = "X"
    print("Black piece was placed successfully.")
    return True

def choose_figure():
    while True:
        player_move = input("Choose figure (pawn or rook) and position (letter a-h and number 1-8), e.g., 'pawn a5' or 'rook h8': ").lower()
        # to see how many items user have written
        parts = player_move.split()
        # input should contain 2 items
        if len(parts) != 2:
            print("Invalid format. Please follow the format 'figure position', e.g., 'pawn a5'.")
            continue

        figure, position = parts
        if figure == "pawn":
            player_figure = "P"
        elif figure == "rook":
            player_figure = "R"
        else:
            print("Invalid figure. Choose either 'pawn' or 'rook'.") # if user input other figure
            continue

        if len(position) != 2:
            print("Invalid position. The position should be a letter followed by a number, e.g., 'a5'.")
            continue

        column, row = position[0], position[1]
        if column < "a" or column > "h" or row < "1" or row > "8":
            print("Invalid position. The column must be a letter from 'a' to 'h' and the row must be a number from '1' to '8'.")
            continue

        column_index = ord(column) - ord('a') # to convert letter to index. Difference between letters gives index
        row_index = int(row) - 1 # user input starts from 1 to 8, to make move in program we need input-1

        return [player_figure, row_index, column_index]

def update_board_state(board_state, move):
    row_index, column_index = move[1], move[2]
    figure = move[0]
    board_state[row_index][column_index] = figure

def get_new_board_state():
    return [[" " for _ in range(8)] for _ in range(8)]

def print_board(board):
    print("   a   b   c   d   e   f   g   h")  # Column indices for clarity
    print(" +" + "---+" * 8)  # Top border with column separators
    for i, row in enumerate(board):
        print(f"{i + 1}| " + " | ".join(row) + " |")  # Rows with cell content and row separators
        print(" +" + "---+" * 8)  # Bottom border with column separators

def check_for_results(board_state, player_info):
    captures = []

    for row in range(8):
        for column in range(8):
            if board_state[row][column] == "P":
                # Check diagonally left for black pieces ('X')
                if row > 0 and column > 0 and board_state[row-1][column-1] == "X":
                    captures.append([row-1, column-1])
                # Check diagonally right for black pieces ('X')
                if row > 0 and column < 7 and board_state[row-1][column+1] == "X":
                    captures.append([row-1, column+1])
                return captures  # Return early for pawn captures

            elif board_state[row][column] == "R":
                # Check horizontally and vertically for black pieces ('X')
                for i in range(8):
                    if board_state[row][i] == "X":
                        captures.append([row, i])
                    if board_state[i][column] == "X":
                        captures.append([i, column])

                top, left, right, bottom = split_by_position(player_info, captures)
                nearest_pieces = get_nearest_pieces(top, left, right, bottom)
                return nearest_pieces  # Return the nearest pieces for rook

    return []  # Return an empty list if no captures are possible

def print_final_board(board_state, captures):
    final_board = [[" " for _ in range(8)] for _ in range(8)]
    for row in range(8):
        for column in range(8):
            if board_state[row][column] in ["P", "R"]:
                final_board[row][column] = board_state[row][column]
            elif [row, column] in captures:
                final_board[row][column] = "X"

    print("Final board state:")
    print_board(final_board)

def main():
    game_in_progress = True
    # to start I need clear board
    board_state = get_new_board_state()

    while game_in_progress:
        print_board(board_state)

        player_info = choose_figure()
        update_board_state(board_state, player_info)

        print_board(board_state)

        # Ask for the first black piece
        while True:
            first_black_piece = input("Choose where to put the first black piece, position (letter a-h and number 1-8) e.g., 'a5' or 'h8': ").lower()
            if len(first_black_piece) == 2 and first_black_piece[0].isalpha() and first_black_piece[1].isdigit():
                if add_black_figure(board_state, first_black_piece):
                    print_board(board_state)
                    break
            if first_black_piece.lower() == "done":
                print("You need to choose at least one black piece")

        # Ensure player places the black piece up to 16 times
        move_count = 1  # First piece has already been placed
        while move_count <= 16:
            another_piece = input("Choose where to put another black piece or write 'done' to finish: ").lower()
            if another_piece == "done":
                break
            if len(another_piece) == 2 and another_piece[0].isalpha() and another_piece[1].isdigit():
                if add_black_figure(board_state, another_piece):
                    print_board(board_state)
                    move_count += 1
                    if move_count == 16:
                        print("Game ended. You have placed all black pieces.")
                        break
            else:
                print("Invalid position. Please follow the format 'letter number', e.g., 'a5'.")

        # Check if any pawn or rook can capture a black piece
        captures = check_for_results(board_state, player_info)
        if captures:
            print("Pieces can capture black pieces at:")
            for capture in captures:
                print(f"{chr(capture[1] + ord('a'))}{capture[0] + 1}")

        # Print the final board state
        print_final_board(board_state, captures)

        # Placeholder for game termination condition
        game_in_progress = False

if __name__ == "__main__":
    main()
