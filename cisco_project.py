cd from random import randrange


def display_board(board):
    # The function accepts one parameter containing the board's current status
    # and prints it to the console.
    for row in board:
        print("+-------+-------+-------+")
        print("|       |       |       |")
        print(f"|   {row[0]}   |   {row[1]}   |   {row[2]}   |")
        print("|       |       |       |")
    print("+-------+-------+-------+")


def enter_move(board):
    # The function accepts the board's current status, asks the user about their move,
    # checks the input, and updates the board according to the user's decision.
    while True:
        try:
            move = int(input("Enter your move: "))
            if move < 1 or move > 9:
                print("Invalid move! Choose a number between 1 and 9.")
                continue

            # Map the 1-9 input to matrix row and column indices
            row = (move - 1) // 3
            col = (move - 1) % 3

            if board[row][col] in ['X', 'O']:
                print("That square is already occupied! Try again.")
                continue

            board[row][col] = 'O'
            break
        except\ ValueError:
            print("Please enter a valid integer.")


def make_list_of_free_fields(board):
    # The function browses the board and builds a list of all the free squares;
    # the list consists of tuples, while each tuple is a pair of row and column numbers.
    free_fields = []
    for r in range(3):
        for c in range(3):
            if board[r][c] not in ['X', 'O']:
                free_fields.append((r, c))
    return free_fields


def victory_for(board, sign):
    # The function analyzes the board's status to check if the player
    # using 'O's or 'X's has won the game.

    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == sign:  # Horizontal
            return True
        if board[0][i] == board[1][i] == board[2][i] == sign:  # Vertical
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == sign:
        return True
    if board[0][2] == board[1][1] == board[2][0] == sign:
        return True

    return False


def draw_move(board):
    # The function draws the computer's move and updates the board.
    free_fields = make_list_of_free_fields(board)
    if free_fields:
        # Pick a random field index from the available free slots
        random_index = randrange(len(free_fields))
        row, col = free_fields[random_index]
        board[row][col] = 'X'


# --- Main Game Loop Execution ---

# 1. Initialize the board with numbers 1 to 9 mapped into a 3x3 grid
board = [[str(3 * r + c + 1) for c in range(3)] for r in range(3)]

# 2. First move belongs to the computer: it always puts 'X' in the middle (5)
board[1][1] = 'X'

# Game loop
while True:
    display_board(board)

    # User's turn
    enter_move(board)
    if victory_for(board, 'O'):
        display_board(board)
        print("You won!")
        break

    if not make_list_of_free_fields(board):
        display_board(board)
        print("It's a tie!")
        break

    # Computer's turn
    draw_move(board)
    if victory_for(board, 'X'):
        display_board(board)
        print("Computer won!")
        break

    if not make_list_of_free_fields(board):
        display_board(board)
        print("It's a tie!")
        brea8