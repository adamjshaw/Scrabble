#!/usr/bin/python

import StringIO
import sys
import re
import time

# Sample interaction:
# > a = ScrabbleBoard(wordScores,letterScores)
# > a.add('hello',5,6,True) - False indicates vertical, True is horizontal
# (a is the board, 'hello' is the word, 5 and 6 are the coordinates)
# > a.add('world',4,10,False)
# > a.add('grillade',7,7,True)
# > a.add('glaired',2,14,False)
# > timeMax(a,'sblivad')
# ('viable', 20, 0, 7, False) -- format: (word, points, xcor, ycor, hor (True is horizontal, False is vertical)
# Running time: 16.750373 seconds -- YMMV

lvals = {'a': 1, 'c': 3, 'b': 3, 'e': 1, 'd': 2, 'g': 2, 'f': 4, 'i': 1, 'h': 4, 'k': 5, 'j': 8, 'm': 3, 'l': 1, 'o': 1, 'n': 1, 'q': 10, 'p': 3, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 4, 'v': 4, 'y': 4, 'x': 8, 'z': 10}

wordScores = {"TW": [(0, 3), (0, 11), (14, 3), (14, 11), (3, 0), (11, 0),
                     (3, 14), (11, 14)],
              "DW": [(1, 5), (1, 9), (3, 7), (5, 1), (5, 13), (7, 3), (7, 11),
                     (9, 1), (9, 13), (11, 7),(13, 5), (13, 9)]
              }

letterScores = {"TL": [(0, 6), (0, 8), (6, 0), (8, 0), (3, 3), (3, 11),
                       (11, 3), (11, 11), (5, 5), (5, 9), (9, 5), (9, 9),
                       (6, 14), (14, 6), (8, 14), (14, 8)],
                "DL": [(1, 2), (2, 1), (1, 12), (12, 1), (2, 4), (4, 2),
                       (2, 13), (13, 2), (2, 10), (10, 2), (4, 12), (12, 4),
                       (4, 6), (4, 8), (6, 4), (8, 4), (10, 12), (12, 10),
                       (12, 13), (13, 12), (6, 10), (10, 6), (8, 10), (10, 8)]
                }
gfile = open('sd').read()
class ScrabbleBoard(object):

    class boardSquare(object):
            def __init__(self, wordScore, letterScore, letter):
                    self.wordScore = wordScore
                    self.letterScore = letterScore
                    self.letter = letter

            def __repr__(self):
                    if (self.letter != None):
                            return str(self.letter)
                    elif (self.wordScore != None):
                            return str(self.wordScore)
                    elif (self.letterScore != None):
                            return str(self.letterScore)
                    else:
                            return '[]'

    def __init__(self, wordScoreDict, letterScoreDict):
            blankBoard = createBlankBoard()
            updatedBoard = updateWS(blankBoard, wordScoreDict)
            updatedBoard = updateLS(updatedBoard, letterScoreDict)
            self.board = updatedBoard

    def __repr__(self):
            boardRows = len(self.board)
            boardColumns = len(self.board[0])

            for r in range(0, boardRows):
                for c in range(0, boardColumns):
                    print repr(self.board[r][c]).rjust(2),

                print
            return ""
    def add(self, word, x, y, hor):
        print posPoints(word, self, x, y, hor)
        if hor:
            for i in word:
                self.board[x][y].letter = i
                self.board[x][y].letterScore = None
                self.board[x][y].wordScore = None
                y += 1
        else:
            for i in word:
                self.board[x][y].letter = i
                self.board[x][y].letterScore = None
                self.board[x][y].wordScore = None
                x += 1

def createBlankBoard():
    board = []
    for a in range(0, 15):
        row = []
        for b in range(0, 15):
            row.append(ScrabbleBoard.boardSquare(None, None, None))
        board.append(row)
    return board

def updateWS(board, wordScoreDict):
    for score in wordScoreDict.keys():
        indices = wordScoreDict[score]
        for tile in indices:
            r = tile[0]
            c = tile[1]
            board[r][c].wordScore = score
    return board

def updateLS(board, letterScoreDict):
    for score in letterScoreDict.keys():
        indices = letterScoreDict[score]
        for tile in indices:
            r = tile[0]
            c = tile[1]
            board[r][c].letterScore = score
    return board

def anagram(word, letters):
    letters2 = list(letters)
    diff = 0
    for i in word:
        if i in letters2:
            letters2.remove(i)
        else:
            diff+= 1
    return diff
def anagram2(word, letters, l):
    letters2 = list(letters)
    if l in word:
        diff = 0
        letters2.append(l)
        for i in word:
            if i in letters2:
                letters2.remove(i)
            else:
                diff+= 1
        return diff
    else:
        return -1
def posPoints(word, board, x, y, hor):
    bonus = 1
    wbonus = 1
    val = 0
    if not hor:
        board = transBoard(board)
        x,y = y,x
    for i in range(0, len(word)):
        bonus = 1
        if board.board[x][y+i].letter == None:
            if board.board[x][y+i].letterScore == "DL":
                bonus = 2
            if board.board[x][y+i].letterScore == "TL":
                bonus = 3
            if board.board[x][y+i].wordScore == "DW":
                wbonus = 2
            if board.board[x][y+i].wordScore == "TW":
                wbonus = 3
            val += bonus * lvals[word[i]]

    current = wbonus * val
    for i in range(0,len(word)):
        if board.board[x][y+i].letter == None:
            newX = x-1
            while newX >= 0 and board.board[newX][y+i].letter != None:
                current += lvals[board.board[newX][y+i].letter]
                newX -= 1
            newX = x+1
            while newX < 15 and board.board[newX][y+i].letter != None:
                current += lvals[board.board[newX][y+i].letter]
                newX += 1
    return current

def emptyLine(board, line):
    if line > 13:
        above = 14
    else:
        above = line + 1
    if line == 7:
        return False
    if line == 0:
        below = 0
    else:
        below = line - 1
    for i in range(0, 15):
        if board.board[line][i].letter != None or board.board[above][i].letter != None or board.board[below][i].letter != None:
            return False
    return True        
def transBoard(board):
    newBoard = ScrabbleBoard(wordScores,letterScores)
    for i in range(15):
        for j in range(15):
            newBoard.board[j][i].letter = board.board[i][j].letter
    return newBoard

def findWord(word):
    f = gfile.splitlines()
    found = 0
    for check in f:
        if word == check:
            found += 1
            break
    return found > 0
def validWord(board, word, x, y, hor):
    f = gfile.splitlines()
    l = list(word)
    if not hor:
        board = transBoard(board)
        x,y = y,x
    if emptyLine(board,x) == True:
        return False
    for i in range(y+len(word), 15):
        if board.board[x][i].letter != None:
            l.append(board.board[x][i].letter)
        else:
            break
    for i in range(y):
        letter = board.board[x][y - i - 1].letter
        if letter != None:
            l.reverse()
            l.append(letter)
            l.reverse()
        else:
            break
    word = ''.join(l)
    if not findWord(word):
        return False
    if y + len(word) > 15:
        return False
    countY = y
    for i in word:
        if board.board[x][y].letter != None and board.board[x][y].letter != i:
            return False
        countY += 1
    index = 0
    #newBoard.add(word,x,y,True)
    for i in range(y,y+len(word)):
        newWord = [word[index]]
        #newWord = []
        for j in range(1,x+1):
            letter = board.board[x - j][i].letter
            if letter != None:
                newWord.append(letter)
            else:
                break
        newWord.reverse()
        for j in range(x+1,15):
            letter = board.board[j][i].letter
            if letter != None:
                newWord.append(letter)
            else:
                break
        if len(newWord) > 1:
            newString = ''.join(newWord)
            if not findWord(newString):
                return False
        index += 1


    return True

def maxPoints2(board,letters, hor):
    f = gfile
    letters2 = list(letters)
    max = 0
    max_word = ""
    max_x = 0
    max_y = 0
    for i in range(0,15):
        if not emptyLine(board,i):
            anchors = [0]
            for j in range(0,15):
                if board.board[i][j].letter != None:
                    anchors.append(j)
            anchors.append(15)
            for j in range(1,len(anchors)-1):
                pattern = '\W[%s]{%d,%d}%s[%s]{%d,%d}\W' % (letters, 0, anchors[j]-anchors[j-1], board.board[i][anchors[j]].letter, letters, 0, anchors[j+1]-anchors[j])
                regex = re.compile(pattern)
                for match in regex.findall(f):
                    match = match.strip()
                    if anagram2(match, letters, board.board[i][anchors[j]].letter) == 0:
                        left = anchors[j] - match.find(board.board[i][anchors[j]].letter)
                        if validWord(board,match,i,left,True):
                            p = posPoints(match,board,i,left,True)
                            if p > max:
                                max = p
                                max_word = match
                                max_x = i
                                max_y = left
    if not hor:
        return (max_word, max, max_x, max_y,False)
    tboard = transBoard(board)
    (vword,vmax,vmax_y, vmax_x,hor) = maxPoints2(tboard,letters,False)
    if (vmax > max):
        return (vword,vmax,vmax_x,vmax_y,False)
    return (max_word, max, max_x, max_y,True)


def createBlankBoard():
    board = []
    for a in range(0, 15):
        row = []
        for b in range(0, 15):
            row.append(ScrabbleBoard.boardSquare(None, None, None))
        board.append(row)
    return board

def timeMax(board,letters):
    t0 = time.time()
    print maxPoints2(board,letters,True)
    print "Running time: %f seconds" % (time.time()-t0)
