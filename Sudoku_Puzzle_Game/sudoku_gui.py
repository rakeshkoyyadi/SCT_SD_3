"""
Sudoku Solver - Graphical Interface (Tkinter)
------------------------------------------------
A simple 9x9 grid GUI where the user types in a puzzle and clicks
"Solve Sudoku" to see the solution. Uses the same backtracking logic
as the command-line version (sudoku_solver.py).

Run with:  python3 sudoku_gui.py
(Tkinter ships with standard Python on Windows/Mac; on Linux you may
need to install it, e.g. `sudo apt install python3-tk`.)
"""

import random
import tkinter as tk
from tkinter import messagebox

# Re-use the exact same solving logic as the CLI version.
from sudoku_solver import (
    GRID_SIZE,
    BOX_SIZE,
    validate_initial_grid,
    solve_sudoku,
    generate_puzzle,
)


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Puzzle Game")
        self.entries = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Tracks whether we've already congratulated the user for the
        # CURRENT completed grid, so the popup doesn't appear repeatedly.
        self.success_shown = False

        self._build_title()
        self._build_grid()
        self._build_buttons()
        self._build_status_label()

    # ------------------------------------------------------------------
    # UI CONSTRUCTION
    # ------------------------------------------------------------------

    def _build_title(self):
        """A bold header banner shown at the very top of the window."""
        title_label = tk.Label(
            self.root,
            text="SUDOKU PUZZLE GAME",
            font=("Arial", 22, "bold"),
            fg="#1a1a2e",
            pady=12,
        )
        title_label.pack(fill="x")

    def _build_grid(self):
        """Create the 9x9 grid of entry boxes, with thicker borders every 3 cells."""
        grid_frame = tk.Frame(self.root, bg="black")
        grid_frame.pack(padx=10, pady=10)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                # Thicker padding around 3x3 box boundaries for a classic Sudoku look
                pad_top = 3 if r % BOX_SIZE == 0 else 1
                pad_left = 3 if c % BOX_SIZE == 0 else 1
                pad_bottom = 3 if r == GRID_SIZE - 1 else 1
                pad_right = 3 if c == GRID_SIZE - 1 else 1

                entry = tk.Entry(
                    grid_frame,
                    width=2,
                    font=("Arial", 18),
                    justify="center",
                    relief="flat",
                )
                entry.grid(
                    row=r,
                    column=c,
                    padx=(pad_left, pad_right),
                    pady=(pad_top, pad_bottom),
                    ipady=6,
                )
                # Only allow a single digit 1-9 to be typed
                entry.config(validate="key")
                entry["validatecommand"] = (
                    self.root.register(self._validate_single_digit),
                    "%P",
                )
                # After every keystroke, check whether the player has just
                # completed the puzzle (used for the "solved!" popup).
                entry.bind("<KeyRelease>", self.on_cell_changed)
                self.entries[r][c] = entry

    def _build_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=(0, 5))

        solve_btn = tk.Button(
            button_frame, text="Solve Sudoku", command=self.on_solve, width=13
        )
        solve_btn.grid(row=0, column=0, padx=5)

        hint_btn = tk.Button(
            button_frame, text="Hint", command=self.on_hint, width=13
        )
        hint_btn.grid(row=0, column=1, padx=5)

        sample_btn = tk.Button(
            button_frame, text="New Puzzle", command=self.on_load_sample, width=13
        )
        sample_btn.grid(row=0, column=2, padx=5)

        clear_btn = tk.Button(
            button_frame, text="Clear", command=self.on_clear, width=13
        )
        clear_btn.grid(row=0, column=3, padx=5)

    def _build_status_label(self):
        """A small status line under the buttons for quick feedback
        (e.g. 'Hint placed at row 3, column 5') without popping up a
        dialog box for every little action."""
        self.status_var = tk.StringVar(value="Enter a puzzle, then Solve or ask for a Hint.")
        status_label = tk.Label(
            self.root, textvariable=self.status_var, fg="gray20", font=("Arial", 10)
        )
        status_label.pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # VALIDATION OF KEYSTROKES
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_single_digit(proposed_text):
        """Only allow empty string or a single digit 1-9 in each cell."""
        if proposed_text == "":
            return True
        return len(proposed_text) == 1 and proposed_text in "123456789"

    # ------------------------------------------------------------------
    # READING / WRITING THE GRID FROM/TO THE UI
    # ------------------------------------------------------------------

    def read_grid(self):
        """Read the current contents of the entry boxes into a 9x9 int grid."""
        grid = []
        for r in range(GRID_SIZE):
            row = []
            for c in range(GRID_SIZE):
                text = self.entries[r][c].get().strip()
                # NOTE: `text in "123456789"` would be True even for an
                # EMPTY string (Python treats "" as a substring of every
                # string), so we must check text.isdigit() first.
                row.append(int(text) if text.isdigit() and text in "123456789" else 0)
            grid.append(row)
        return grid

    def write_grid(self, grid, only_fill_empty=False):
        """Write a 9x9 int grid into the entry boxes (0 -> blank)."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                entry = self.entries[r][c]
                value = grid[r][c]
                if only_fill_empty and entry.get().strip() != "":
                    continue
                entry.delete(0, tk.END)
                if value != 0:
                    entry.insert(0, str(value))

    # ------------------------------------------------------------------
    # BUTTON HANDLERS
    # ------------------------------------------------------------------

    def on_solve(self):
        grid = self.read_grid()

        is_valid, reason = validate_initial_grid(grid)
        if not is_valid:
            messagebox.showerror("Invalid Puzzle", reason)
            self.status_var.set("Fix the highlighted rule violation and try again.")
            return

        if solve_sudoku(grid):
            # Fill in only the previously-empty cells, in a different
            # color, so the user can see what was solved vs. given.
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    entry = self.entries[r][c]
                    was_empty = entry.get().strip() == ""
                    entry.delete(0, tk.END)
                    entry.insert(0, str(grid[r][c]))
                    entry.config(fg="blue" if was_empty else "black")

            self.success_shown = True  # avoid a duplicate completion popup
            self.status_var.set("Puzzle solved successfully!")
            messagebox.showinfo(
                "Solved!", "\u2705 The Sudoku puzzle was solved successfully!"
            )
        else:
            messagebox.showinfo(
                "No Solution", "No solution exists for this Sudoku puzzle."
            )
            self.status_var.set("No solution exists for this puzzle.")

    def on_hint(self):
        """
        Reveal one correct number for an empty cell, without solving the
        whole puzzle. Uses the backtracking solver on a COPY of the grid
        so the user's other entries are left untouched.
        """
        grid = self.read_grid()

        is_valid, reason = validate_initial_grid(grid)
        if not is_valid:
            messagebox.showerror("Invalid Puzzle", reason)
            self.status_var.set("Fix the highlighted rule violation and try again.")
            return

        empty_cells = [
            (r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0
        ]
        if not empty_cells:
            self.status_var.set("The grid is already full \u2014 try Solve or check your answers.")
            return

        # Solve a deep copy so we don't disturb the numbers already typed in.
        solved_copy = [row[:] for row in grid]
        if not solve_sudoku(solved_copy):
            messagebox.showinfo(
                "No Solution",
                "No solution exists from the numbers currently entered, "
                "so a hint isn't possible. Check for mistakes and try again.",
            )
            self.status_var.set("Can't give a hint \u2014 current entries have no solution.")
            return

        # Reveal the first empty cell found, in a distinct "hint" color.
        row, col = empty_cells[0]
        entry = self.entries[row][col]
        entry.delete(0, tk.END)
        entry.insert(0, str(solved_copy[row][col]))
        entry.config(fg="darkorange")

        self.status_var.set(f"Hint: placed {solved_copy[row][col]} at row {row + 1}, column {col + 1}.")
        self.on_cell_changed()  # in case that hint just completed the puzzle

    def on_load_sample(self):
        # Build a brand-new random puzzle from scratch every time this is
        # clicked (never the same puzzle twice), with a randomized number
        # of clues (28-40) so difficulty varies a bit too.
        num_clues = random.randint(28, 40)
        puzzle = generate_puzzle(num_clues)

        self.on_clear()
        self.write_grid(puzzle)
        self.status_var.set(f"New random puzzle generated ({num_clues} clues). Click Solve or Hint.")

    def on_clear(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.entries[r][c].delete(0, tk.END)
                self.entries[r][c].config(fg="black")
        self.success_shown = False
        self.status_var.set("Enter a puzzle, then Solve or ask for a Hint.")

    # ------------------------------------------------------------------
    # LIVE COMPLETION CHECK (fires the "you solved it!" celebration)
    # ------------------------------------------------------------------

    def on_cell_changed(self, event=None):
        """
        Called after every keystroke in any cell. If the grid has just
        become completely and correctly filled in (by the user typing,
        or by a hint), congratulate them. If it's full but breaks a rule,
        gently point that out instead.
        """
        grid = self.read_grid()
        is_full = all(grid[r][c] != 0 for r in range(GRID_SIZE) for c in range(GRID_SIZE))

        if not is_full:
            self.success_shown = False  # board changed, allow popup again later
            return

        is_valid, reason = validate_initial_grid(grid)

        if is_valid:
            if not self.success_shown:
                self.success_shown = True
                self.status_var.set("\U0001F389 Congratulations! You solved the puzzle!")
                messagebox.showinfo(
                    "Congratulations!",
                    "\U0001F389 Congratulations \u2014 you solved the puzzle correctly!",
                )
        else:
            self.status_var.set(f"Grid is full but not valid yet: {reason}")


def main():
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()