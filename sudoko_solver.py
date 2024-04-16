import sys

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(rows, cols):
    return [r+c for r in rows for c in cols]



def get_unitlist():
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = row_units + column_units + square_units
    return unitlist


def get_peers(boxes, unitlist):
    unit = []
    units = []
    for b in boxes:
        for u in unitlist:
            if b in u:
                unit.append(u)
        units.append(unit)
        unit = []

    units2 = []
    last_units = []
    for u in units:
        for x in u:
            units2.extend(x)
        last_units.append(units2)
        units2 = []

    last_units2 = []
    for u in last_units:
        last_units2.append(set(u))

    for i, u in enumerate(last_units2):
        for j, b in enumerate(boxes):
            if i == j:
                u.discard(b)

    peers = dict(zip(boxes, last_units2))
    return peers


def display(values, boxes):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def grid_values(grid, boxes):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    if len(grid) != len(boxes):
        print(f"Please check that your grid length = {len(boxes)}")
        sys.exit()
    else:
        grid = [i.replace('.', cols) for i in grid]
        sudoko_dict = dict(zip(boxes, grid))
    return sudoko_dict


def eliminate(values, peers):

    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    for box in values:   # same output as: values.keys():
        if len(values.get(box)) == 1:
            for peer in peers.get(box):   # work on dictionary values
                values[peer] = values.get(peer).replace(values.get(box), '')

    return values


def only_choice(values, unitlist):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.

"""
    for unit in unitlist:
        for digit in cols:
            only_one = [box for box in unit if digit in values[box]]
            only_values = [values[box] for box in only_one]
            #print(only_one, only_values)
            if len(only_one) == 1:
                values[only_one[0]] = digit

    return values


def naked_twins(values, peers):
    for box in values:
        if len(values[box]) > 1:
            for peer in peers[box]:
                #print(values[peer])
                if len(values[box]) != len(values[peer]):
                    #if values[box] != values[peer]:
                    values[peer] = values[peer].replace(values[box], '')
    return values


def reduce_puzzle(values, peers, unitlist):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box 
        with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.

        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values, peers)
        #values = naked_twins(values)
        # Use the Only Choice Strategy
        values = only_choice(values, unitlist)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(boxes, values, peers, unitlist):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values, peers, unitlist)
    # Choose one of the unfilled squares with the fewest possibilities
    if values is False:
        return False  ## Failed earlier
    if all(len(values[box])==1 for box in values):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    # The all() function is an inbuilt function in Python which returns true
    # if all the elements of a given iterable( List, Dictionary, Tuple, set, etc) are True
    # else it returns False. It also returns True if the iterable object is empty.
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    #print(n, s)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoko = values.copy()
        new_sudoko[s] = value
        attempt = search(boxes, new_sudoko, peers, unitlist)

        if attempt:
            return attempt



def main(grid):
    boxes = cross(rows, cols)
    unitlist = get_unitlist()
    peers = get_peers(boxes, unitlist)
    sudoko_dict = grid_values(grid, boxes)

    print("Normal Sudoko")
    display(sudoko_dict, boxes)
    print('\n\n')

    solution = search(boxes, sudoko_dict, peers, unitlist)
    print("Solved Sudoko")
    display(solution, boxes)
    print('\n\n\n')


if __name__ == "__main__":
    grid1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    grid3 = '1.4.9..68956.18.34..84.695151.....868..6...1264..8..97781923645495.6.823.6.854179'
    grids = [grid1, grid2, grid3]

    for grid in grids:
        main(grid)