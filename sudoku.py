import time
from os import system
from timeit import default_timer as timer

import numpy as np


def create_cover(sudoku, grid_width=9, block_width=3):
    """
    Creates the relationship matrix used by algorithm-x
    :param sudoku: the sudoku matrix (2-d numpy array)
    :param grid_width: number of elements in a row
    :param block_width: number of blocks in a row
    :return: the relationship matrix (called a cover)
    """
    g_len = sudoku.shape[0]  # grid side length
    n_non_zeros = np.count_nonzero(sudoku)
    # N_possibilities = #_of_zeros * numbers_per_row + #_of_non_zeros
    n_possibilities = (g_len * g_len - n_non_zeros) * g_len + n_non_zeros
    # There are 4 types of constraints and each type has g_len * g_len constraints
    n_constrains = 4 * g_len * g_len
    # cover stores the 0-1 relationships that Algorithm-X uses
    cover = np.zeros((n_possibilities, n_constrains))
    # possibilities stores the 'name' of a possibility (row, col, number) such that
    # possibilities[i] is the name for row i in cover. This is used to fill in the
    # sudoku at the end
    possibilities = []
    # iterate over each sudoku element, add possibilities and fill in its corresponding
    # relationship with each constraint
    for row in range(g_len):
        for col in range(g_len):
            # if (is a starting number in the sudoku grid)
            if sudoku[row, col] != 0:
                possibility = (row, col, sudoku[row, col])
                add_possibility(
                    possibility,
                    cover,
                    len(possibilities),
                    grid_width=grid_width,
                    block_width=block_width,
                )
                possibilities.append(possibility)
                continue
            for n in range(1, grid_width + 1):
                possibility = (row, col, n)
                add_possibility(
                    possibility,
                    cover,
                    len(possibilities),
                    grid_width=grid_width,
                    block_width=block_width,
                )
                possibilities.append(possibility)
    return cover, possibilities


def add_possibility(possibility, cover, cover_row, grid_width=9, block_width=3):
    """
    Adds the possibility and its constraint relationships to the cover matrix.
    :param possibility: The possibility to add
    :param cover: The cover matrix
    :param cover_row: The row in the cover matrix to add the relationships
    :param grid_width: number of elements in a row
    :param block_width: number of blocks in a row
    """
    row, col, n = possibility
    # Row-Column constraint
    cover[cover_row, row * grid_width + col] = 1
    # Row-Number constraint
    cover[cover_row, grid_width * grid_width + row * grid_width + n - 1] = 1
    # Col-Number constraint
    cover[cover_row, 2 * grid_width * grid_width + col * grid_width + n - 1] = 1
    # Block-Number constraint
    # block_idx is the nth block, counting from left to right, top-down
    block_idx = (row // block_width) * grid_width // block_width + (col // block_width)
    cover[cover_row, 3 * grid_width * grid_width + block_idx * grid_width + n - 1] = 1


def solve(cover, active_rows, active_cols, solution: list):
    """
    solves the exact cover problem with algorithm-x.
    See https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X for the high level algorithm
    :param cover: the cover.
    :param active_rows: a vector representing which rows haven't and have been removed.
    # this is used for efficiency's sake. Rather than creating a whole new matrix
    # at each iteration when we remove row i, we simply set a active_rows[i] = 0.
    :param active_cols: same as active_rows but for columns.
    :param solution: a list provided which will hold the final solution.
    :return: True if the algorithm successfully found a solution.
    """
    # no active columns means the solution is found.
    if np.sum(active_cols) == 0:
        return True
    # pick the column with the lest number of 1s. This is a heuristic to speed up the
    # algorithm (and is extremely effective for sudoku).
    col, count = min_col(cover, active_rows, active_cols)
    # a column that doesn't contains 1s means no solution can be found and we backtrack.
    if count == 0:
        print("backtrack!")
        return False
    for row in np.nonzero(active_rows * cover[:, col])[0]:
        solution.append(row)
        # track removed rows and columns so we can easily add them back if we need
        # to backtrack
        removed_rows, removed_cols = select(row, cover, active_rows, active_cols)
        solved = solve(cover, active_rows, active_cols, solution)
        if solved:
            return True
        # not solved: backtrack
        solution.pop()
        deselect(removed_rows, removed_cols, active_rows, active_cols)


def select(row, cover, active_rows, active_cols):
    """
    selects a row (possibility) by removing columns and rows that conflict with it.
    :param row: the row representing the selected possibility
    :param cover: the cover matrix
    :param active_rows: active rows in the cover matrix
    :param active_cols: active columns in the cover matrix
    :return: a tuple (removed_rows, removed_cols) which are numpy arrays containing a
    1 if the row/column was removed or 0 otherwise.
    """
    removed_rows = np.zeros(active_rows.shape[0])
    removed_cols = np.zeros(active_cols.shape[0])
    for col in np.nonzero(active_cols * cover[row, :])[0]:
        # if active_cols[col] == 0 or cover[row, col] == 0:
        #     continue
        # at this point: cover[row, col] is 1. Remove other rows that have a 1 in this
        # column.
        for row2 in np.nonzero(active_rows * cover[:, col])[0]:
            # if active_rows[row2] == 1 and cover[row2, col] == 1:
            active_rows[row2] = 0
            removed_rows[row2] = 1
        # now remove the column because we just covered `row` just covered it.
        active_cols[col] = 0
        removed_cols[col] = 1
    return removed_rows, removed_cols


def deselect(removed_rows, removed_cols, active_rows, active_cols):
    """
    restore rows and columns that were removed with select()
    """
    active_rows += removed_rows
    active_cols += removed_cols

    # for i in range(removed_rows.shape[0]):
    #     if removed_rows[i] == 1:
    #         active_rows[i] = 1
    # for i in range(removed_cols.shape[0]):
    #     if removed_cols[i] == 1:
    #         active_cols[i] = 1


def min_col(cover, active_rows, active_cols):
    """
    :return: (column, count) tuple such that column contains the least number of 1s
    compared to other columns.
    """
    counts = col_counts(cover, active_rows, active_cols)
    argmin = -1
    for i in range(counts.shape[0]):
        if active_cols[i] == 0:
            continue
        if argmin == -1 or counts[i] < counts[argmin]:
            argmin = i
    return argmin, counts[argmin]


def col_counts(r, active_rows, active_cols):
    return np.sum(r[active_rows == 1, :], axis=0)


def print_grid(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            print(grid[i, j] if grid[i, j] != 0 else "_", end=" ")
        print()


def main():
    # sudoku = np.array(
    #     [
    #         [0,18,15,9,0,21,0,0,0,0,0,0,22,1,0,0,5,0,14,0,12,0,0,13,7],
    #         [23,0,0,4,0,0,0,11,0,0,0,25,24,0,0,18,0,0,20,0,6,0,0,0,0],
    #         [],
    #         [8, 3, 0, 6, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 9, 0, 0, 1, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [5, 0, 7, 0, 0, 0, 3, 0, 0],
    #         [0, 0, 0, 3, 0, 2, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0],
    #     ]
    # )
    size = 5
    sudoku = np.zeros((size * size, size * size), dtype=np.uint8)

    cover, possibilities = create_cover(sudoku, grid_width=size*size, block_width=size)
    solution = []
    start = timer()
    solved = solve(
        cover, np.ones(cover.shape[0]), np.ones(cover.shape[1]), solution=solution
    )
    end = timer()
    print(f"Solved in {end - start} seconds")
    if solved:
        for sol in solution:
            row, col, n = possibilities[sol]
            sudoku[row, col] = n
        print_grid(sudoku)
    else:
        print("No solution exists :(")


if __name__ == "__main__":
    main()
