# 🧩 Sudoku Puzzle Game & Solver

A Python-based **Sudoku Puzzle Game and Solver** that uses the **Backtracking Algorithm** to solve 9×9 Sudoku puzzles. The project includes both a **Command-Line Interface (CLI)** and an interactive **Graphical User Interface (GUI)** built with Tkinter.

## 📌 Project Description

This project allows users to enter an unsolved Sudoku puzzle and automatically find its solution. The GUI version also allows users to generate random puzzles, enter their own numbers, request hints, solve the entire puzzle, and receive a success message when they complete the puzzle correctly.

Both versions use the same backtracking-based solving engine.

## ✨ Key Features

* 🧩 Solves standard 9×9 Sudoku puzzles
* 🔄 Uses recursive backtracking algorithm
* 💻 Command-line interface for solving custom puzzles
* 🖥️ Interactive Tkinter graphical interface
* 🎲 Generates random Sudoku puzzles
* 💡 Provides one-cell hints
* ⚡ Automatically solves the current puzzle
* ✅ Validates rows, columns, and 3×3 boxes
* 🚫 Detects invalid Sudoku puzzles
* ❌ Reports when no solution exists
* 🎉 Detects when the player completes the puzzle correctly
* 📝 Accepts `1–9` for filled cells and `0` or `.` for empty cells
* 📚 Beginner-friendly and commented code

## 🛠️ Technologies Used

* **Python 3.7+**
* **Tkinter** – Graphical User Interface
* **Backtracking Algorithm** – Sudoku solving
* **Recursion** – Searching possible solutions
* **Random Module** – Generating random puzzles

## 📂 Project Structure

```text
sudoku-puzzle-game/
│
├── sudoku_solver.py
├── sudoku_gui.py

```

### File Description

| File               | Description                                           |
| ------------------ | ----------------------------------------------------- |
| `sudoku_solver.py` | Core Sudoku solving engine and command-line interface |
| `sudoku_gui.py`    | Tkinter-based graphical Sudoku game                   |
| `README.md`        | Project documentation                                 |

> **Important:** Keep `sudoku_solver.py` and `sudoku_gui.py` in the same folder because the GUI imports the solving functions from the solver file.

## 📋 Requirements

* Python **3.7 or later**
* Tkinter for the graphical version

No external Python packages are required.

### Checking Python Installation

Open a terminal or command prompt and run:

```bash
python --version
```

or:

```bash
python3 --version
```

### Checking Tkinter

Run:

```bash
python -m tkinter
```

If Tkinter is installed correctly, a small test window should appear.

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sudoku-puzzle-game.git
```

### 2. Open the Project Folder

```bash
cd sudoku-puzzle-game
```

### 3. Run the Command-Line Solver

```bash
python sudoku_solver.py
```

You can either:

* Enter `sample` to solve the built-in sample puzzle.
* Enter your own Sudoku puzzle row by row.

Example:

```text
5 3 . . 7 . . . .
6 . . 1 9 5 . . .
. 9 8 . . . . 6 .
```

You can also enter rows without spaces:

```text
530070000
```

Use `0` or `.` to represent empty cells.

### 4. Run the Graphical Game

```bash
python sudoku_gui.py
```

The Sudoku GUI will open in a separate window.

## 🎮 GUI Controls

### 🆕 New Puzzle

Generates a new random Sudoku puzzle.

### 💡 Hint

Reveals one correct number in an empty cell.

### 🧠 Solve Sudoku

Automatically solves the current Sudoku puzzle.

### 🧹 Clear

Clears the entire Sudoku board.

## 🧠 Backtracking Algorithm

The Sudoku solver uses **recursive backtracking** to find a valid solution.

The basic process is:

1. Find an empty cell.
2. Try numbers from `1` to `9`.
3. Check whether the number is valid in the row.
4. Check whether the number is valid in the column.
5. Check whether the number is valid in the corresponding 3×3 box.
6. If the number is valid, place it in the cell.
7. Recursively solve the remaining puzzle.
8. If the choice leads to a dead end, remove the number.
9. Try another number.
10. Continue until the puzzle is solved.

This process is called **backtracking** because the algorithm goes back to previous decisions when a selected number cannot lead to a valid solution.

## 📐 Sudoku Rules

A valid Sudoku solution must satisfy three conditions:

### Row Rule

Each row must contain the numbers **1–9 exactly once**.

### Column Rule

Each column must contain the numbers **1–9 exactly once**.

### 3×3 Box Rule

Each 3×3 box must contain the numbers **1–9 exactly once**.

## 🎲 Random Puzzle Generation

The GUI can generate a new puzzle each time the **New Puzzle** button is clicked.

The generation process is:

1. Start with an empty Sudoku grid.
2. Generate a complete valid Sudoku solution using backtracking.
3. Randomize candidate numbers during generation.
4. Remove a random number of cells from the completed solution.
5. Use the remaining numbers as the puzzle clues.

Because the puzzle starts from a valid completed Sudoku grid, the generated puzzle is guaranteed to have at least one solution.

## 🧪 Sample Input

```text
5 3 . . 7 . . . .
6 . . 1 9 5 . . .
. 9 8 . . . . 6 .
8 . . . 6 . . . 3
4 . . 8 . 3 . . 1
7 . . . 2 . . . 6
. 6 . . . . 2 8 .
. . . 4 1 9 . . 5
. . . . 8 . . 7 9
```

## ✅ Sample Output

```text
Puzzle solved successfully!

5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
---------------------
8 5 9 | 7 6 1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8 5 6
---------------------
9 6 1 | 5 3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9
```

## ⚠️ Error Handling

The application validates the Sudoku puzzle before attempting to solve it.

For example, if a row contains duplicate numbers, it may display:

```text
Invalid puzzle: Row 1 contains a duplicate number.
```

If the puzzle follows the basic Sudoku rules but cannot be solved, the application displays:

```text
No solution exists for this Sudoku puzzle.
```

## 🎯 Learning Objectives

This project helps demonstrate:

* Python programming
* Functions
* Lists and 2D arrays
* Recursion
* Backtracking algorithms
* Constraint checking
* Exception and input handling
* Random number generation
* GUI development with Tkinter
* Modular Python programming

## ⏱️ Algorithm Complexity

The backtracking algorithm can have a large worst-case search space because it may need to try many possible combinations.

For a standard 9×9 Sudoku, the theoretical search space can be very large, but constraint checking eliminates invalid choices during the search, making typical puzzles practical to solve.

## 🔮 Future Improvements

Possible enhancements include:

* Add Sudoku difficulty levels
* Add a timer
* Add score tracking
* Add undo/redo functionality
* Highlight incorrect entries
* Add puzzle-solving statistics
* Add a pause/resume feature
* Improve the GUI design
* Add a puzzle uniqueness checker
* Add save/load game functionality

## 👨‍💻 Author

**Rakesh**

