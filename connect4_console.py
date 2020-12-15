#!/usr/bin/env python3

import os

# (C,R)
# (7,6)

#     C0 C1 C2 C3 C4 C5 C6
# R5  05 15 25 35 45 55 65
# R4  04 14 24 34 44 54 64 
# R3  03 13 23 33 43 53 63
# R2  02 12 22 32 42 52 62
# R1  01 11 21 31 41 51 61 
# R0  00 10 20 30 40 50 60

originalBoard = []  # [ [C0 rows], [C1 rows], ... , [C6 rows] ]
maxC = 7   
maxR = 6
red = "X"           # human player, minimizer
yellow = "O"        # AI player, maximizer
placeholder = "."

# initialize the board to dots
for col in range(maxC):
    rows = []
    for row in range(maxR):
        if placeholder:
            rows.append(placeholder)
        else:
            rows.append(row)
    originalBoard.append(rows)

# Move object stores score and column values of a move
class Move():
    def __init__(self, score):
        self.score = score
        self.col = -1

# prints game board to console
def printBoard(board):
    s = ""
    for row in range(maxR):
        for col in range(len(board)):
            s += str(board[col][maxR - row - 1]) + "    "
        if row < maxR-1:
            s += "\n"
        print(s)
        s = ""

# returns list of indices of columns that are not full
def availableCols(board):
    li = []
    for col_num in range(len(board)):
        count = 0
        for item in board[col_num]:
            if item == red or item == yellow:
                count += 1
        if count < maxR:
            li.append(col_num)
    return li

# drop player's chip in col of board
def dropChip(col, player, board):
    if col >= maxC or col < 0:
        return

    nextR = 0
    for item in board[col]: 
        if item != placeholder:
            nextR += 1
    if nextR < maxR:
        board[col][nextR] = player
        return nextR

def winning(board, player):
    # check vertical
    for col in board:
        count = 0
        for row in col:
            if row == player:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
    
    # check horizonal
    for rown in range(maxR):
        count = 0
        for coln in range(len(board)):
            if board[coln][rown] == player:
                count += 1
                if count >= 4:
                    return True     
            else:
                count = 0

    # check diagonal: top left -> bottom right
    for r in range(maxR):
        coln = 0
        rown = r+3
        count = 0
        while rown > maxR-1: # if too high, keep moving down and right
            rown -= 1
            coln += 1
        while rown >= 0 and coln <= maxC-1:
            if board[coln][rown] == player:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
            rown -= 1
            coln += 1

    # check diagonal: bottom left -> top right
    for r in range(maxR):
        coln = 0
        rown = maxR - r - 4
        count = 0
        while rown < 0: # if too low, keep moving up and right
            rown += 1
            coln += 1
        while rown < maxR and coln <= maxC-1:
            if board[coln][rown] == player:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0
            rown += 1
            coln += 1

    # 4 in a row not found, so return false
    return False

# returns score based on state of the board
def boardState(board, player):
    numTwos = 0
    numThrees = 0
    numFours = 0
    numCenters = 0

    # check vertical
    for col in board:
        count = 0
        for row in col:
            if row == player:
                count += 1
            else:
                if count == 2:
                    numTwos += 1
                elif count == 3:
                    numThrees += 1
                elif count == 4:
                    numFours += 1
                count = 0
    
    # check horizonal
    for rown in range(maxR):
        count = 0
        for coln in range(len(board)):
            if board[coln][rown] == player:
                count += 1    
            else:
                if count == 2:
                    numTwos += 1
                elif count == 3:
                    numThrees += 1
                elif count == 4:
                    numFours += 1
                count = 0

    # check diagonal: top left -> bottom right
    for r in range(maxR):
        coln = 0
        rown = r+3
        count = 0
        while rown > maxR-1: # if too high, keep moving down and right
            rown -= 1
            coln += 1
        while rown >= 0 and coln <= maxC-1:
            if board[coln][rown] == player:
                count += 1
            else:
                if count == 2:
                    numTwos += 1
                elif count == 3:
                    numThrees += 1
                elif count == 4:
                    numFours += 1
                count = 0
            rown -= 1
            coln += 1

    # check diagonal: bottom left -> top right
    for r in range(maxR):
        coln = 0
        rown = maxR - r - 4
        count = 0
        while rown < 0: # if too low, keep moving up and right
            rown += 1
            coln += 1
        while rown < maxR and coln <= maxC-1:
            if board[coln][rown] == player:
                count += 1
            else:
                if count == 2:
                    numTwos += 1
                elif count == 3:
                    numThrees += 1
                elif count == 4:
                    numFours += 1
                count = 0
            rown += 1
            coln += 1
    # loop through center column chips and count number of chips player has in center column
    for chip in board[int(maxC/2)]: 
        if chip == player:
            numCenters += 1

    # 4 in a row not found, so return score based on board state
    # 2-in-row < center col < 3-in-row < 4-in-row
    score = 50*numCenters + 10*numTwos + 100*numThrees + 500*numFours
    if player == red:
        return (-1 * score)
    return score

# minimax function with alpha-beta pruning
def minimax(board, player, depth, alpha, beta):
    # list of available cols
    availCols = availableCols(board)

    # check wins
    if winning(board, red):
        return Move(-100000)
    elif winning(board, yellow): # ai, yellow, max
        return Move(100000)
    # else if depth == 0, evaluate board state at that time (return score based on how many 2 and 3 in a row)
    elif depth == 0:
        score = boardState(board, player)
        return Move(score)
    
    # create a move object
    m = Move(0)

    if player == yellow: # if ai, maximize
        bestScore = -100000000
        for i in range(len(availCols)):
            # drop player's chip in the column number of board
            r = dropChip(availCols[i], player, board)
            result = minimax(board, red, depth-1, alpha, beta)
            board[availCols[i]][r] = placeholder
            if result.score > bestScore:
                bestScore = result.score
                m.col = availCols[i]
            alpha = max(alpha, result.score)
            if beta <= alpha:
                break
        m.score = bestScore
        return m

    elif player == red: # if human, minimize
        bestScore = 100000000
        for i in range(len(availCols)):
            # drop player's chip in the column number of board
            r = dropChip(availCols[i], player, board)
            result = minimax(board, yellow, depth-1, alpha, beta)
            board[availCols[i]][r] = placeholder
            if result.score < bestScore:
                bestScore = result.score
                m.col = availCols[i]
            beta = min(beta, result.score)
            if beta <= alpha:
                break
        m.score = bestScore
        return m

def printLast(ind):
    s1 = ""
    for i in range(maxC):
        s1 += str(i+1) + "    "
    if ind == -1:
        print("\n" + s1)
        return
    li = []
    for c in range(maxC):
        if c == ind:
            li.append("@    ")
        else:
            li.append("     ")
    s = ""
    for i in range(len(li)):
        s += li[i]
    print(s)
    print(s1)

# function to clear console screen
def clear(): 
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

# return True or False
def checkGameOver(run):
    valid = availableCols(originalBoard)
    if winning(originalBoard, yellow):
        print("You lose!")
        run = False
        return True
    elif winning(originalBoard, red):
        print("You win!")
        run = False
        return True
    elif (len(valid) == 0):
        print("It's a tie!")
        run = False
        return True
    else:
        return False

def main():
    running = True
    ind = -1
    # game loop
    while running:
        clear()
        print("\nEnter column number to drop a chip, q to quit game")
        print(placeholder + " empty space")
        print("@" + " last move made")
        print(yellow + " \"Paul\" the a.i.")
        print(red + " You\n")
        # player's turn 
        printLast(ind)
        printBoard(originalBoard)
        if checkGameOver(running):
            break
        print("Your turn (" + red + ")")
        valid = availableCols(originalBoard)
        for i in range(len(valid)):
            valid[i] = str(valid[i] + 1)
        inp = input()
        if inp == "q":
            running = False
            break
        while (inp not in valid):
            inp = input()
        dropChip(int(inp)-1, red, originalBoard)
        ind = int(inp)-1 

        # computer's turn
        clear()
        print("\nEnter column number to drop a chip, q to quit game")
        print(placeholder + " empty space")
        print("@" + " last move made")
        print(yellow + " \"Paul\" the a.i.")
        print(red + " You\n")
        printLast(ind) 
        printBoard(originalBoard)
        if checkGameOver(running):
            break
        print("Paul is thinking...")
        m = minimax(originalBoard, yellow, 7, -999999999, 999999999)
        dropChip(m.col, yellow, originalBoard)
        ind = m.col

if __name__ == "__main__":
    main()