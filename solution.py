
def cross(A, B):
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'	
assignments = []
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    #dual_values = [box for box in values.keys() if len(values[box]) == 2]
    for column in row_units:
      dual_values= [box for box in column if len(values[box])==2]
      for box in dual_values: 	
        twin_values=[twinbox for twinbox in column if values[twinbox]==values[box]]
        if (len(set(twin_values))>1):
          for indiv_twin_values in twin_values:
            for peer in column:
              if peer not in twin_values:
                for digit in values[indiv_twin_values]:
                  values[peer] = values[peer].replace(digit,'')
    for column in column_units:
      dual_values= [box for box in column if len(values[box])==2]
      for box in dual_values: 	
        twin_values=[twinbox for twinbox in column if values[twinbox]==values[box]]
        if (len(set(twin_values))>1):
          for indiv_twin_values in twin_values:
            for peer in column:
              if peer not in twin_values:
                for digit in values[indiv_twin_values]:
                  values[peer] = values[peer].replace(digit,'')
	
    return values		
def display(values):
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

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))	
	


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values	

def only_choice(values):
    for unit in unitlist:
      for digit in '123456789':
        dplaces = [box for box in unit if digit in values[box]]
        # return the boxes having the criteria ie the digit exists in them
        if len(dplaces) == 1:
          values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    pass

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in grid.keys() if len(grid[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        solved_grid = [box for box in grid.keys() if len(grid[box]) == 1]
        for box in solved_grid:
          digit = grid[box]
          for peer in peers[box]:
            grid[peer] = grid[peer].replace(digit,'')


        # Your code here: Use the Only Choice Strategy
        for unit in unitlist:
          for digit in '123456789':
            dplaces = [box for box in unit if digit in grid[box]]
            # return the boxes having the criteria ie the digit exists in them
            if len(dplaces) == 1:
              grid[dplaces[0]] = digit
        
        # Check how many boxes have a determined value, to compare
        solved_grid_after = len([box for box in grid.keys() if len(grid[box]) == 1])
        # If no new grid were added, stop the loop.
        stalled = solved_grid_before == solved_grid_after
        # Sanity check, return False if there is a box with zero available grid:
        if len([box for box in grid.keys() if len(grid[box]) == 0]):
          return False
    return grid

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
