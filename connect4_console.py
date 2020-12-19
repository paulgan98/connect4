#!/usr/bin/env python3

import os
import random

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
red = "R"           # human player, minimizer
yellow = "Y"        # AI player, maximizer
placeholder = "."

# initialize the board to dots
def createBoard(board):
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
            s += str(board[col][maxR - row - 1]) + "   "
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
    li_shuffled = li[:]
    random.shuffle(li_shuffled)
    return li_shuffled

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
    maxScore = 1000000
    numCenters = 0
    score = 0
    # [3, 4, 5,  7,  5,  4, 3], 
    # [4, 6, 8,  10, 8,  6, 4],
    # [5, 8, 11, 13, 11, 8, 5], 
    # [5, 8, 11, 13, 11, 8, 5],
    # [4, 6, 8,  10, 8,  6, 4],
    # [3, 4, 5,  7,  5,  4, 3]

    #                 R  0 1 2 3 4 5
    evaluationTable =  [[3,4,5,5,4,3],      # C0
                        [4,6,8,8,6,4],      # C1
                        [5,8,11,11,8,5],    # C2
                        [7,10,13,13,10,7],  # C3
                        [5,8,11,11,8,5],    # C4
                        [4,6,8,8,6,4],      # C5
                        [3,4,5,5,4,3]]      # C6

    # check vertical
    for col in board:
        count = 0
        for row in col:
            if row == player:
                count += 1
            else:
                if row == placeholder and (count == 2 or count == 3):
                    score += count**2
                elif row == placeholder and count >= 4:
                    score += maxScore
                count = 0
    
    # check horizonal
    for rown in range(maxR):
        count = 0
        c = -1
        for coln in range(len(board)):
            if board[coln][rown] == player:
                count += 1  
                if c == -1: # if leftmost chip in streak, set to column number 
                    c = coln
            else:
                if count == 2 or count == 3:
                    if c == 0 and board[c + count][rown] == placeholder:
                        score += count**2
                    elif 1 <= c < maxC-count and (board[c-1][rown] == placeholder) or (board[c+count][rown] == placeholder):
                        score += count**2
                    elif c == maxC-count and board[c-1][rown] == placeholder:
                        score += count**2
                elif count >= 4:
                    score += maxScore
                count = 0
                c = -1

    # check diagonal: top left -> bottom right
    for r in range(maxR):
        coln = 0
        rown = r+3
        count = 0
        c = -1
        while rown > maxR-1: # if too high, keep moving down and right
            rown -= 1
            coln += 1
        while rown >= 0 and coln <= maxC-1:
            if board[coln][rown] == player:
                count += 1
                if c == -1: # if leftmost chip in streak, set to column number 
                    c = coln
            else:
                if count == 2 or count == 3:
                    if c == 0 and board[c + count][rown] == placeholder:
                        score += count**2
                    elif 1 <= c < maxC-count and (board[c-1][rown] == placeholder) or (board[c+count][rown] == placeholder):
                        score += count**2
                    elif c == maxC-count and board[c-1][rown] == placeholder:
                        score += count**2
                elif count >= 4:
                    score += maxScore
                count = 0
                c = -1
            rown -= 1
            coln += 1

    # check diagonal: bottom left -> top right
    for r in range(maxR):
        coln = 0
        rown = maxR - r - 4
        count = 0
        c = -1
        while rown < 0: # if too low, keep moving up and right
            rown += 1
            coln += 1
        while rown < maxR and coln <= maxC-1:
            if board[coln][rown] == player:
                count += 1
                if c == -1: # if leftmost chip in streak, set to column number 
                    c = coln
            else:
                if count == 2 or count == 3:
                    if c == 0 and board[c + count][rown] == placeholder:
                        score += count**2
                    elif 1 <= c < maxC-count and (board[c-1][rown] == placeholder) or (board[c+count][rown] == placeholder):
                        score += count**2
                    elif c == maxC-count and board[c-1][rown] == placeholder:
                        score += count**2
                elif count >= 4:
                    score += maxScore
                count = 0
                c = -1
            rown += 1
            coln += 1

    # loop through center column chips and count number of chips player has in center column
    for chip in board[int(maxC/2)]: 
        if chip == player:
            numCenters += 1

    evalScore = 0
    for coln in range(len(board)):
        for rown in range(coln):
            if board[coln][rown] == player:
                evalScore += evaluationTable[coln][rown]

    # return score based on board state
    score += evalScore + 5*numCenters
    if player == red:
        return (-1 * score)
    return score

def otherPlayer(player):
    if player == red:
        return yellow
    else:
        return red

# minimax function with alpha-beta pruning
def minimax(board, player, time, depth, alpha, beta):
    # list of available cols
    availCols = availableCols(board)
    
    # check wins
    if winning(board, red):
        score = boardState(board, red)
        return Move(score * time)
    elif winning(board, yellow):
        score = boardState(board, yellow)
        return Move(score * time)

    # else if depth == 0, evaluate board state at that time
    elif depth == 0 or len(availCols) == 0:
        score = boardState(board, player) + boardState(board, otherPlayer(player))
        return Move(score * time)
    
    # create a move object
    m = Move(0)

    if player == yellow: # if ai, maximize
        bestScore = -1000000000000
        for i in range(len(availCols)):
            # drop player's chip in the column number of board
            r = dropChip(availCols[i], player, board)
            result = minimax(board, red, time*0.98, depth-1, alpha, beta)
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
        bestScore = 1000000000000
        for i in range(len(availCols)):
            # drop player's chip in the column number of board
            r = dropChip(availCols[i], player, board)
            result = minimax(board, yellow, time*0.98, depth-1, alpha, beta)
            board[availCols[i]][r] = placeholder
            if result.score < bestScore:
                bestScore = result.score
                m.col = availCols[i]
            beta = min(beta, result.score)
            if beta <= alpha:
                break
        m.score = bestScore
        return m


# -------------------- Variables and functions for the main game loop --------------------

def initBoard(moveHistory, board):
    for item in moveHistory:
        dropChip(item[1]-1,item[0], board)

# print move history after game
def printMoveHistory(moveHistory):
    s = ""
    for i in range(len(moveHistory)):
        s += "(\"" + str(moveHistory[i][0]) + "\"," + str(moveHistory[i][1]) + ")"
        if i < len(moveHistory)-1:
            s += ","
    print("Moves Made: " + s)

# print column numbers and last move made
def printLast(ind):
    s1 = ""
    for i in range(maxC):
        s1 += str(i+1) + "   "
    if ind == -1:
        print("\n" + s1)
        return
    li = []
    for c in range(maxC):
        if c == ind:
            li.append("@   ")
        else:
            li.append("    ")
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
def checkGameOver():
    valid = availableCols(originalBoard)
    if winning(originalBoard, yellow):
        return "lose"
    elif winning(originalBoard, red):
        return "win"
    elif (len(valid) == 0):
        return "tie"
    else:
        return ""

running = True
moves = 1
t = 1
d = 7
ind = -1

# function to help get input without having to press enter
def getch():
    import termios
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

def takeTurn(player):
    global running
    global moves
    global d
    global t
    global ind
    global moveHistory

    clear()
    print("\nEnter column number to drop a chip, q to quit game")
    print(placeholder + " empty space")
    print("@" + " last move made")
    print(yellow + " \"Paul\" the a.i.")
    print(red + " You\n")
    print("Move: ", moves) 
    printLast(ind)
    print("\n") 
    printBoard(originalBoard)
    inp = ""

    # player's turn
    if player == red:
        print("Your turn (" + red + ")")
        valid = availableCols(originalBoard)
        for i in range(len(valid)):
            valid[i] = str(valid[i] + 1)
        inp = getch()
        while (inp not in valid):
            if inp == "q":
                printMoveHistory(moveHistory)
                running = False
                break
            else:
                inp = getch()
        if inp != "q":
            ind = int(inp)-1

    # ai's turn
    else:  # yellow
        print("Paul is thinking...")
        m = minimax(originalBoard, player, t, d, -999999999, 999999999)
        ind = m.col
    
    if inp != "q":
        dropChip(ind, player, originalBoard)
        moves += 1
        moveHistory.append((player, ind+1))
        c = checkGameOver()
        if c:
            clear()
            print("\nEnter column number to drop a chip, q to quit game")
            print(placeholder + " empty space")
            print("@" + " last move made")
            print(yellow + " \"Paul\" the a.i.")
            print(red + " You\n")
            print("Move: ", moves)
            printLast(ind) 
            printBoard(originalBoard)
            printMoveHistory(moveHistory)
            if c == "win":
                print("You won!")
            elif c == "lose":
                print("You lost!")
            elif c == "tie":
                print("It's a tie!")
            moves = 1
            running = False

# paste move history [(col, player), (col, player), ...] 
# into moveHistory to initialize board to that state. 
# Otherwise, set to empty list
moveHistory = []
running = True

# player vs ai
def main():
    global running
    global moves
    global originalBoard
    global moveHistory
    startingPlayer = yellow
    currPlayer = startingPlayer
    createBoard(originalBoard)
    initBoard(moveHistory, originalBoard)
    if moveHistory:
        startingPlayer = otherPlayer(moveHistory[-1][0])
    newGame = True

    # game loop
    while newGame:
        while running:
            takeTurn(currPlayer)
            if currPlayer != yellow:
                currPlayer = yellow
            else:
                currPlayer = red
        print("Press space to play again. Press q to terminate")
        inp = getch()
        if inp == "q":
            newGame = False
        elif inp == " ":
            running = True
            originalBoard.clear() 
            moveHistory.clear() 
            createBoard(originalBoard)
            moves = 1 

if __name__ == "__main__":
    main()