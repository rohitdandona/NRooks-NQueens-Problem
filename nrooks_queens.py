# nrooks_queens.py : Solve the N-Rooks/N-Queens problem!
#
# The N-rooks/N-Queens problem is: Given an empty NxN chessboard, place N rooks/Queens on the 
# board so that no rooks/queen can take any other.

# This is N, the size of the board.
import time
import sys

N=375

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Count total # of pieces present on each possible diagonal on the board
def count_on_diag(board):
    # Sum of each right diagonal
    check = N - 1
    diagonal_sums = []
    for r in range(0, N):
        diag_sum = 0
        for c in range(0, N):
            if (c <= check):
                diag_sum += board[c][r]
                r += 1
        check -= 1
        if diag_sum <= 1:
            diagonal_sums.append(True)
        else:
            diagonal_sums.append(False)

    check = N - 1
    for r in range(1, N):
        diag_sum = 0
        c = 0
        check -= 1
        temp = r
        while c <= check:
            diag_sum += board[temp][c]
            c += 1
            temp += 1
        if diag_sum <= 1:
            diagonal_sums.append(True)
        else:
            diagonal_sums.append(False)

    # Sum of each left diagonal
    check = N - 1
    for r in reversed(range(N)):
        diag_sum = 0
        for c in range(0, N):
            if (c <= check):
                diag_sum += board[c][r]
                r -= 1
        check -= 1
        if diag_sum <= 1:
            diagonal_sums.append(True)
        else:
            diagonal_sums.append(False)

    check = 0
    for r in range(1, N):
        diag_sum = 0
        c = N - 1
        check += 1
        temp = r
        while c >= check:
            diag_sum += board[temp][c]
            c -= 1
            temp += 1
        if diag_sum <= 1:
            diagonal_sums.append(True)
        else:
            diagonal_sums.append(False)
    return diagonal_sums

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1, ] + board[row][col + 1:]] + board[row + 1:]

# Get list of successors of given board state
def successors(board):
    return [add_piece(board, r, c) for r in range(0, N) for c in range(0, N)]

# Get list of successors of given board state (N+1 and "moves" problem fixed)
def successors2(board):
    succ = []
    for r in range(0, N):
        for c in range(0, N):
            new_b = add_piece(board, r, c)
            if new_b != board:
                total_sum = 0
                for row in new_b:
                    total_sum += sum(row)
                if total_sum <= N:
                    succ.append(new_b)
    return succ

def successors3(board):
    succ = []
    index = 0
    index_list_row = []
    index_list_col = []
    for row in board:
        if any(row):
            index_list_row.append(index)
            index_list_col.append(row.index(1))
        index += 1
    if index_list_col:
        next_col = max(index_list_col) + 1
    else:
        next_col = 0
    for r in range(0, N):
        if r not in index_list_row and next_col < N:
            new_b = add_piece(board, r ,next_col)
            succ.append(new_b)
    return succ


# check if board is a goal state (rook)
def is_goal_rook(board):
    return count_pieces(board) == N and \
           all([count_on_row(board, r) <= 1 for r in range(0, N)]) and \
           all([count_on_col(board, c) <= 1 for c in range(0, N)])

# check if board is a goal state (queen)
def is_goal_queen(board):
    return count_pieces(board) == N and \
        all([count_on_row(board, r) <= 1 for r in range(0, N)]) and \
        all([count_on_col(board, c) <= 1 for c in range(0, N)]) and \
        all(count_on_diag(board))


# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal_rook(s):
                return(s)
            fringe.append(s)
    return False

# Solve n-queens!
def nqueens_solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal_queen(s):
                return(s)
            fringe.append(s)
    return False

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.

ans = raw_input("Would you also like to find the N Queens solution for N = "+str(N)+" (Y or N): ")

# Begin execution of N rooks problem...
initial_board = [[0]*N]*N
print("N Rooks Problem !")
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for a solution with " + str(N) +" rooks...\n")
start_time = time.time()
solution = solve(initial_board)
print (printable_board(solution) if solution else "Sorry, no solution found. :(")
print("\n")

if ans == "N":
    print("--- %s seconds ---\n\n" % (time.time() - start_time))
    sys.exit(0)

# Begin execution of N queens problem...
initial_board = [[0]*N]*N
print("N Queens Problem !")
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for a solution with " + str(N) +" queens...\n")
solution = nqueens_solve(initial_board)
print (printable_board(solution) if solution else "Sorry, no solution found. :(")
print("--- %s seconds ---" % (time.time() - start_time))

