from flask import Flask, after_this_request, request

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST'])
def aiMove():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    payload = request.get_json(force=True)
    print(payload['isGameOver'], payload['board'])
    aiMove = makeMove(payload['board'])
    return str(aiMove)

# This function returns true if there are moves remaining on the board
# It returns false if there are no moves left to play
def isMovesLeft(board):
    for idx, value in enumerate(board):
        if value is None:
            return True

    return False

# Evaluate current board state
# if x wins => return 10
# else if o wins => return -10
# otherwise => return 0
def evaluate(b):
    # Check for Rows for X or O Victory    
    for row in range(3):
        if b[row * 3] == b[row * 3 + 1] and b[row * 3 + 1] == b[row * 3 + 2]:
            if b[row * 3] == 'x':
                return 10
            elif b[row * 3] == 'o':
                return -10

    # Check For columns for X or O Victory
    for col in range(3):        
        if b[col] == b[3 + col] and b[3 + col] == b[6 + col]:
            if b[col] == 'x':
                return 10
            elif b[col] == 'o':
                return -10

    # Check For Diagonals for X or O Victory
    if b[0] == b[4] and b[4] == b[8]:
        if b[0] == 'x':
            return 10
        elif b[0] == 'o':
            return -10

    if b[2] == b[4] and b[4] == b[6]:
        if b[2] == 'x':
            return 10
        elif b[2] == 'o':
            return -10

    # Else if none of them have won then return 0
    return 0

# this function consider all the possible ways the game can go and returns the value of the board
def minmax(board, depth, isMax):
    score = evaluate(board)
    print('evaluate', score, board)

    # If Maximizer has won the game return his evaluated score
    if score == 10:
        return score

    # If Minimizer has won the game return evaluated score
    if score == -10:
        return score

    # If there are no more moves and no winner then 
    # It is a tie
    if isMovesLeft(board) == False:
        return 0

    # If this is maximizer's move
    if isMax:
        best = -1000
        # Traverse all cells
        for idx, value in enumerate(board):
            # Check if cell is empty
            if value is None:
                # Make the Move
                board[idx] = 'x'

                # Call minimax recursively and chose the maximun values
                best = max(best, minmax(board, depth + 1, not isMax))

                # Undo then Move
                board[idx] = None

        return best

    # If this is minimizer move
    else:
        best = 1000
        for idx, value in enumerate(board):
            # Check if cell is empty
            if value is None:
                # Make the move
                board[idx] = 'o'

                # Call minimax recursively and choose the minimum value
                best = min(best, minmax(board, depth + 1, not isMax))

                # Undo the move
                board[idx] = None

        return best


def makeMove(board):
    bestVal = 1000
    bestMove = -1

    # Traverse all cells, evaluate minmax function 
    # for all empty cells, And return the cell with optimal value
    for idx, value in enumerate(board):
        # Check if cell is empty
        if value is None:
            # Make the Move
            board[idx] = 'o'

            # Compute evaluate function for this move
            moveVal = minmax(board, 0, True)
            print(idx, moveVal)

            # Undo the move
            board[idx] = None

            # If the value of the current move is less than the best value
            # Then update best
            if moveVal < bestVal:
                bestMove = idx
                bestVal = moveVal

    return bestMove


