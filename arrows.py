import random
import curses

# Define the size of the board
SIZE = 4

# # Function to generate a shuffled board with guaranteed solvability
# def generate_solvable_board():
#     numbers = list(range(1, SIZE * SIZE))  # Create list 1 to 15
#     numbers.append(0)  # Add the empty space
#     random.shuffle(numbers)
#     return numbers


# Function to generate a shuffled board with guaranteed solvability
def generate_solvable_board():
    numbers = list(range(SIZE * SIZE))
    random.shuffle(numbers)

    # Ensure the generated board is solvable
    while not is_solvable(numbers):
        random.shuffle(numbers)

    return numbers

# Function to count the number of inversions in a list
def count_inversions(lst):
    count = 0
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j] and lst[i] != 0 and lst[j] != 0:
                count += 1
    return count

# Function to check if a board is solvable
def is_solvable(board):
    inversions = count_inversions(board)
    if SIZE % 2 != 0:  # For odd-sized boards
        return inversions % 2 == 0
    else:  # For even-sized boards
        blank_row = SIZE - board.index(0) // SIZE
        return (inversions + blank_row) % 2 != 0
    

# Function to print the board
def print_board(stdscr, board):
    max_number_length = len(str(SIZE * SIZE)) + 1  # Determine the maximum length of a number
    for i in range(SIZE):
        for j in range(SIZE):
            number = board[i * SIZE + j]
            padding = max_number_length - len(str(number))  # Calculate padding for each number
            stdscr.addstr(" " * padding + str(number) + " ")
        stdscr.addstr("\n")
    stdscr.refresh()

# Function to check if the game is won
def is_won(board):
    return all(board[i] == i + 1 for i in range(len(board) - 1)) and board[-1] == 0


# Function to move the number adjacent to the empty space
def move(board, blank_index, direction):
    def swap(board, i, j):
        board[i], board[j] = board[j], board[i]
        return board
    if direction == "↓" and blank_index >= SIZE:
        neighbor_index = blank_index - SIZE
    elif direction == "↑" and blank_index < SIZE * (SIZE - 1):
        neighbor_index = blank_index + SIZE
    elif direction == "→" and blank_index % SIZE != 0:
        neighbor_index = blank_index - 1
    elif direction == "←" and (blank_index + 1) % SIZE != 0:
        neighbor_index = blank_index + 1
    else:
        print("Invalid move!")
        return board, blank_index
    
    board = swap(board, blank_index, neighbor_index)
    return board, neighbor_index

# Main game loop
def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    board = generate_solvable_board()
    blank_index = board.index(0)
    stdscr.addstr("Welcome to the 15 Puzzle!\n")
    print_board(stdscr, board)
    while not is_won(board):
        stdscr.addstr("Use arrow keys to move (press 'q' to quit): ")
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            move_direction = "↓"
        elif key == curses.KEY_UP:
            move_direction = "↑"
        elif key == curses.KEY_LEFT:
            move_direction = "←"
        elif key == curses.KEY_RIGHT:
            move_direction = "→"
        elif key == ord('q'):
            break
        else:
            continue
        board, blank_index = move(board, blank_index, move_direction)
        stdscr.clear()
        stdscr.addstr("Welcome to the 15 Puzzle!\n")
        print_board(stdscr, board)

    stdscr.addstr("Congratulations! You solved the puzzle!\n")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
