# Sudoku Solver

This Python program solves Sudoku puzzles using a combination of strategies, including elimination, only choice, and naked twins. It employs a depth-first search algorithm to find the solution.

## Features

- **Grid Values**: Converts a Sudoku grid string into a dictionary form for easier manipulation.
- **Cross Function**: Generates all possible boxes in the Sudoku grid.
- **Unitlist Generation**: Creates a list of units (rows, columns, and squares) for Sudoku constraints.
- **Peers Generation**: Determines the peers (related boxes) for each box in the Sudoku grid.
- **Display Function**: Displays the Sudoku grid in a readable format.
- **Eliminate Function**: Eliminates values from the peers of each box with a single value.
- **Only Choice Function**: Finalizes all values that are the only choice for a unit.
- **Naked Twins Function**: Implements the naked twins strategy to eliminate values from peers.
- **Reduce Puzzle Function**: Iteratively applies elimination and only choice strategies to reduce the puzzle.
- **Search Function**: Uses depth-first search and propagation to solve the Sudoku puzzle.

## Usage

1. Install Python (if not already installed).
2. Run the `main` function with a Sudoku grid string as input to solve the puzzle.

Example usage:

```python
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
main(grid)
