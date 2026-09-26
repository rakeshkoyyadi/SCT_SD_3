"""
Sudoku Solver using the Backtracking Algorithm
------------------------------------------------
This program:
  1. Accepts a 9x9 Sudoku grid from the user (or uses a built-in sample).
  2. Validates that the given puzzle follows Sudoku rules (no duplicate
     numbers in any row, column, or 3x3 box).
  3. Solves the puzzle using backtracking.
  4. Prints the completed grid, or a message if no solution exists.

Author: Written to be clean, beginner-friendly, and well commented.
"""

import random

GRID_SIZE = 9
BOX_SIZE = 3


# ----------------------------------------------------------------------
# INPUT HANDLING
# ----------------------------------------------------------------------

def parse_row(row_text):
    """
    Convert a single line of user input into a list of 9 integers.
    Accepts '0' or '.' for empty cells, and digits '1'-'9' for filled cells.
    Any other character (commas, spaces) is simply ignored.
    """
    cleaned = []
    for ch in row_text:
        if ch in "123456789":
            cleaned.append(int(ch))
        elif ch in "0.":
            cleaned.append(0)
        # spaces, commas, etc. are ignored -> allows "5, 3, ., ., 7 ..." style input
    return cleaned


def get_grid_from_user():
    """
    Ask the user to type in 9 rows of the Sudoku puzzle.
    Typing 'sample' at the first prompt loads a built-in demo puzzle instead.
    """
    print("Enter your Sudoku puzzle, one row at a time (9 rows total).")
    print("Use digits 1-9 for filled cells and 0 or . for empty cells.")
    print("Example row: 5 3 . . 7 . . . .")
    print("(Or just type 'sample' to solve a built-in example puzzle.)\n")

    first_line = input("Row 1: ")
    if first_line.strip().lower() == "sample":
        return get_sample_grid()

    grid = [parse_row(first_line)]
    for i in range(2, GRID_SIZE + 1):
        while True:
            line = parse_row(input(f"Row {i}: "))
            if len(line) == GRID_SIZE:
                grid.append(line)
                break
            print(f"  -> That row had {len(line)} numbers, need exactly 9. Try again.")

    return grid


def get_sample_grid(index=None):
    """
    Return one of several built-in sample Sudoku puzzles (0 = empty cell).

    - Pass a specific `index` (0-based) to get that exact puzzle.
    - Leave `index` as None to get a puzzle at random.
    """
    if index is None:
        index = random.randrange(len(SAMPLE_PUZZLES))
    return [row[:] for row in SAMPLE_PUZZLES[index]]  # return a fresh copy


SAMPLE_PUZZLES = [
    # Puzzle 0 - classic easy example
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    # Puzzle 1 - easy
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ],
    # Puzzle 2 - medium
    [
        [0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 7, 0, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 1, 3],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 3, 6],
        [0, 0, 0, 3, 0, 6, 0, 9, 0],
    ],
    # Puzzle 3 - hard ("AI Escargot", one of the toughest known puzzles)
    [
        [1, 0, 0, 0, 0, 7, 0, 9, 0],
        [0, 3, 0, 0, 2, 0, 0, 0, 8],
        [0, 0, 9, 6, 0, 0, 5, 0, 0],
        [0, 0, 5, 3, 0, 0, 9, 0, 0],
        [0, 1, 0, 0, 8, 0, 0, 0, 2],
        [6, 0, 0, 0, 0, 4, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 7, 0, 0, 0, 3, 0, 0],
    ],
]


# ----------------------------------------------------------------------
# VALIDATION (checking the puzzle as GIVEN, before solving)
# ----------------------------------------------------------------------

def has_duplicates(values):
    """Return True if the non-zero numbers in `values` contain a duplicate."""
    seen = set()
    for v in values:
        if v == 0:
            continue
        if v in seen:
            return True
        seen.add(v)
    return False


def validate_initial_grid(grid):
    """
    Check that the puzzle, as typed in by the user, doesn't already break
    Sudoku rules (duplicate numbers in a row, column, or 3x3 box).
    Returns (True, "") if valid, or (False, "reason") if not.
    """
    # Check rows
    for r in range(GRID_SIZE):
        if has_duplicates(grid[r]):
            return False, f"Row {r + 1} contains a duplicate number."

    # Check columns
    for c in range(GRID_SIZE):
        column = [grid[r][c] for r in range(GRID_SIZE)]
        if has_duplicates(column):
            return False, f"Column {c + 1} contains a duplicate number."

    # Check 3x3 boxes
    for box_row in range(0, GRID_SIZE, BOX_SIZE):
        for box_col in range(0, GRID_SIZE, BOX_SIZE):
            box_values = [
                grid[r][c]
                for r in range(box_row, box_row + BOX_SIZE)
                for c in range(box_col, box_col + BOX_SIZE)
            ]
            if has_duplicates(box_values):
                return False, (
                    f"The 3x3 box starting at row {box_row + 1}, "
                    f"column {box_col + 1} contains a duplicate number."
                )

    return True, ""


# ----------------------------------------------------------------------
# BACKTRACKING SOLVER
# ----------------------------------------------------------------------

def find_empty_cell(grid):
    """
    Scan the grid left-to-right, top-to-bottom, and return the (row, col)
    of the first empty cell (value 0). Return None if the grid is full.
    """
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                return r, c
    return None


def is_valid_placement(grid, num, row, col):
    """
    Check whether placing `num` at grid[row][col] would be legal:
    - `num` must not already appear in that row
    - `num` must not already appear in that column
    - `num` must not already appear in that 3x3 box
    """
    # Row check
    if num in grid[row]:
        return False

    # Column check
    for r in range(GRID_SIZE):
        if grid[r][col] == num:
            return False

    # 3x3 box check
    box_row_start = (row // BOX_SIZE) * BOX_SIZE
    box_col_start = (col // BOX_SIZE) * BOX_SIZE
    for r in range(box_row_start, box_row_start + BOX_SIZE):
        for c in range(box_col_start, box_col_start + BOX_SIZE):
            if grid[r][c] == num:
                return False

    return True


def solve_sudoku(grid):
    """
    Solve the Sudoku puzzle in-place using backtracking.

    The algorithm:
      1. Find the next empty cell. If there isn't one, the grid is full
         and solved -> return True.
      2. Try each number 1-9 in that cell.
      3. If a number is valid there, place it and recursively try to
         solve the rest of the grid.
      4. If the recursive call succeeds, we're done -> return True.
      5. If it fails, undo the placement (backtrack) and try the next
         number.
      6. If no number from 1-9 works, return False so the previous call
         can backtrack further.
    """
    empty = find_empty_cell(grid)
    if empty is None:
        return True  # No empty cells left -> puzzle solved

    row, col = empty

    for num in range(1, 10):
        if is_valid_placement(grid, num, row, col):
            grid[row][col] = num  # Tentatively place the number

            if solve_sudoku(grid):  # Recurse
                return True

            grid[row][col] = 0  # Backtrack: undo and try the next number

    return False  # Triggers backtracking in the caller


# ----------------------------------------------------------------------
# RANDOM PUZZLE GENERATOR (for a fresh, new puzzle on every request)
# ----------------------------------------------------------------------

def _fill_grid_randomly(grid):
    """
    Fill an empty grid into a complete, valid, RANDOM Sudoku solution.
    Identical to solve_sudoku's backtracking, except the numbers 1-9 are
    tried in shuffled order instead of always 1,2,3..., so a different
    complete grid comes out almost every time this is called.
    """
    empty = find_empty_cell(grid)
    if empty is None:
        return True  # Grid is completely (and validly) filled

    row, col = empty
    numbers = list(range(1, 10))
    random.shuffle(numbers)  # <-- the only difference from solve_sudoku

    for num in numbers:
        if is_valid_placement(grid, num, row, col):
            grid[row][col] = num
            if _fill_grid_randomly(grid):
                return True
            grid[row][col] = 0

    return False


def generate_puzzle(num_clues=32):
    """
    Generate a brand-new, valid, solvable Sudoku puzzle.

    Steps:
      1. Build a complete, randomly-filled solution grid (every cell 1-9,
         following all Sudoku rules) using backtracking with shuffled
         candidate numbers.
      2. Punch holes in it: randomly clear cells until only `num_clues`
         numbers remain, leaving the rest as 0 (empty).

    Because the puzzle is created by erasing cells from an already-valid
    solution, it is guaranteed to be solvable. `num_clues` controls the
    difficulty: more clues left behind = easier puzzle.
    """
    num_clues = max(17, min(num_clues, 81))  # 17 is the known minimum for a unique puzzle

    solution = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    _fill_grid_randomly(solution)

    puzzle = [row[:] for row in solution]
    all_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(all_cells)

    cells_to_clear = (GRID_SIZE * GRID_SIZE) - num_clues
    for r, c in all_cells[:cells_to_clear]:
        puzzle[r][c] = 0

    return puzzle


def print_grid(grid):
    """Print the grid nicely, with lines separating the 3x3 boxes."""
    for r in range(GRID_SIZE):
        if r % BOX_SIZE == 0 and r != 0:
            print("-" * 21)

        row_str = ""
        for c in range(GRID_SIZE):
            if c % BOX_SIZE == 0 and c != 0:
                row_str += "| "
            value = grid[r][c]
            row_str += (str(value) if value != 0 else ".") + " "
        print(row_str)


# ----------------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------------

def main():
    grid = get_grid_from_user()

    print("\nYour puzzle:")
    print_grid(grid)

    is_valid, reason = validate_initial_grid(grid)
    if not is_valid:
        print(f"\nInvalid puzzle: {reason}")
        print("Please fix the input and try again.")
        return

    print("\nSolving...\n")
    if solve_sudoku(grid):
        print("\u2705 Puzzle solved successfully!\n")
        print_grid(grid)
    else:
        print("No solution exists for this Sudoku puzzle.")


if __name__ == "__main__":
    main()