class GameState():
    def __init__(self):
        #Board is an 8x8 2d list, each element of the list has two characters.
        #The first character represents the color of the piece, 'b', or 'w'.
        #The second character represents the type of the piece. 'K', 'Q', etc.
        #"--" represents an unoccupied space on the board.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN","bR"],
            ["bp","bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp","wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN","wR"]]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
    #takes a move as a parameter and executes it(This will not work for castling, pawn promotion, and en-passant)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo the move later
        self.whiteToMove = not self.whiteToMove #swap players
        #update King's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
    #undo the last move    
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #update King's position if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
    #All moves considering checks
    def getValidMoves(self):
        # 1.) Generate all possible moves
        moves = self.getAllPossibleMoves()
        # 2.) For each move, make the move
        for i in range(len(moves)-1, -1, -1): #When removing from a list, go backwards through the list
            self.makeMove(moves[i])
            # 3.) Generate all opponent's moves
            # 4.) For each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        # 5.) If they do attack your king, it's not a valid move
        if len(moves) == 0: #Either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves
    #All moves without considering checks
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #Switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #Switch turn back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #calls move function based on piece type
        return moves
    def getPawnMoves(self, r, c, moves): #Get all the pawn moves for pawn located at row, col and add these moves to the list
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #One square pawn advance
                moves.append(Move((r, c),(r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c),(r-2,c), self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c),(r-1,c-1), self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c),(r-1,c+1), self.board))
        else: #black pawn moves
            if self.board[r+1][c] == "--": #One square pawn advance
                moves.append(Move((r, c),(r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c),(r+2,c), self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c),(r+1,c-1), self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c),(r+1,c+1), self.board))
        #add pawn promotions later
            
    def getRookMoves(self, r, c, moves): #Get all the rook moves for rook located at row, col and add these moves to the list
        directions = ((-1,0), (0,-1), (1,0), (0,1)) #up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: # off board
                    break
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece != allyColor: # not an ally piece(empty or enemy piece)
                    moves.append(Move((r,c), (endRow, endCol), self.board))
    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))
class Move():
    # Maps keys to values
    # Key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    #Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]