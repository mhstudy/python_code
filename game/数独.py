def is_valid(board, row, col, num):
    # 检查行是否有重复
    for x in range(9):
        if board[row][x] == num:
            return False

    # 检查列是否有重复
    for x in range(9):
        if board[x][col] == num:
            return False

    # 检查小宫格是否有重复
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return (None, None)


def solve_sudoku(board):
    row, col = find_empty(board)
    if row is None:
        return True  # 数独已解

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0  # 回溯
    return False


def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            print(board[i][j], end=" ")
        print()


sudoku_board = []
with open('数独.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # 把每一行的字符串数字转换成整数列表
        int_row = [int(num) for num in row]
        sudoku_board.append(int_row)


if solve_sudoku(sudoku_board):
    print("数独已解，结果如下:")
    print_board(sudoku_board)
else:
    print("无解")

if solve_sudoku(sudoku_board):
    print("数独已解，结果如下:")
    print_board(sudoku_board)
else:
    print("无解")
