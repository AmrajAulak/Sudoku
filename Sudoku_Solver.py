import numpy as np

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    current_board = sudoku.copy()
    
    domain = get_domain(current_board)
    #print (domain)
    current_board = presolve_board(current_board, domain)

    frontier = []
    frontier.append(current_board)
    global explored
    explored = []
    n = len(current_board)
    
    while True:
        explored.append(current_board)
        
        if is_goal_state(current_board):
            solved_board = current_board.copy()
            #print("Solution found!")
            return solved_board

      
        frontier = (add_nodes(n, current_board, frontier, domain)).copy()

        if len(frontier) == 0:
            #print("No solution found")
            return failed_board(current_board)
        
        new_board = frontier.pop()
        current_board = new_board.copy()
        
        
def add_nodes(n, current_board, frontier, domain):
    #domain = np.arange(1, 10)
    for i in range(n):
        for j in range(n):
            if current_board[i,j] == 0:
                values = domain[(i,j)]
                for value in values:
                    child_board = current_board.copy()
                    if (valid_move(child_board, i, j, value)):
                        child_board[i, j] = value
                        if is_unique(child_board, explored, frontier):
                            frontier.append(child_board)
                return frontier
        
def is_goal_state(current_board):
    n = len(current_board)
    for i in range(n):
        for j in range(n):
            if current_board[i,j] == 0:
                return False
    return True        
        
def failed_board(current_board):
    for i in range(9):
        for j in range(9):
            current_board[i,j] = -1
    return current_board

def is_unique(child_board, explored, frontier):
    def not_in_explored():
        for i in range(len(explored)):
            if ((explored[i] == child_board).all()):
                return False
        return True
        
    def not_in_frontier():
        for i in range(len(frontier)):
            if ((frontier[i] == child_board).all()):
                return False
        return True
        
    return (not_in_explored() and not_in_frontier())

def get_domain(current_board):
    domain = {}
    possible_values = []
    for i in range(9):
        for j in range(9):
            possible_values = []
            if current_board[i, j] == 0:
                for x in range(1, 10):
                    if valid_move(current_board, i, j, x):
                        possible_values.append(x)
                domain.update({(i, j): possible_values})
    
    return domain

def presolve_board(current_board, domain):
    for key in domain:
        if len(domain[key]) == 1:
            i = key[0]
            j = key[1]
            current_board[i][j] = domain[i, j][0]

    return current_board


def valid_move(new_board, row_ind, col_ind, value):

    n = len(new_board)

    def check_columns():
        for j in range(n):
            if new_board[row_ind,j] == value:
                return False
        return True
    
    def check_rows():
        for i in (list(range(0, row_ind)) + list(range(row_ind + 1, n))):
            if new_board[i,col_ind] == value:
                return False
        return True
    
    def check_grid():
        row_start = (row_ind // 3) * 3
        col_start = (col_ind // 3) * 3
        row_end = row_start + 3
        col_end = col_start + 3
        for i in range(row_start, row_end):
            for j in range (col_start, col_end):
                if new_board[i,j] == value:
                    return False
        return True        
                
    return check_rows() and check_columns() and check_grid()
      

def main():
    # Load sudokus
    sudoku = np.load("data/very_easy_puzzle.npy")[1]
    print("very_easy_puzzle.npy has been loaded into the variable sudoku")
    print(sudoku)
    print()
    #print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")
    print(sudoku_solver(sudoku))

#main()