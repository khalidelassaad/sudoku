import pdb
import time
from random import randint

class Board:
    def __init__(self):
        self.rows = []
        self.cols = []
        self.squares = []
        self.level = 0
        for x in range(9):
            self.rows.append([" "]*9)
            self.cols.append([" "]*9)
            self.squares.append([" "]*9)
        
    def drawboard(self):
        rs = ""
        for x in range(0,3):
            rs = rs + " ".join(self.rows[x][0:3])
            rs = rs + "|"
            rs = rs + " ".join(self.rows[x][3:6])
            rs = rs + "|"
            rs = rs + " ".join(self.rows[x][6:])
            rs = rs + "\n"
        rs = rs + "-----+-----+-----\n"
        for x in range(3,6):
            rs = rs + " ".join(self.rows[x][0:3])
            rs = rs + "|"
            rs = rs + " ".join(self.rows[x][3:6])
            rs = rs + "|"
            rs = rs + " ".join(self.rows[x][6:])
            rs = rs + "\n"
        rs = rs + "-----+-----+-----\n"
        for x in range(6,9):
            rs = rs + " ".join(self.rows[x][0:3])
            rs = rs + "|"
            rs = rs + " ".join(self.rows[x][3:6])
            rs = rs + "|"
            rs = rs + " ".join(self.rows[x][6:])
            rs = rs + "\n"
        print(rs)

    def setcell(self,row,col,num):
        self.rows[row][col] = str(num)
        self.updatefromrows()
        return

    def clearcell(self,row,col):
        self.rows[row][col] = " "
        return

    def readfromstring(self,s):
        if len(s) != 81:
            raise ValueError
        i = 0
        for row in range(9):
            for col in range(9):
                if s[i] == "0":
                    x = " "
                elif s[i] in "123456789 ":
                    x = s[i]
                else:
                    raise ValueError
                self.rows[row][col] = x
                i+=1
        self.updatefromrows()
        return

    def printtostring(self):
        rs = ""
        for row in self.rows:
            for val in row:
                rs = rs + val
        return rs

    def colsfromrows(self):
        #Populates self.cols depending on what's in rows
        for col in range(9):
            for row in range(9):
                self.cols[col][row] = self.rows[row][col]
        return

    def squaresfromrows(self):
        #Populates self.squares depending on what's in rows
        for x in range(3):
            for y in range(3):
                for row in range(3):
                    for col in range(3):
                        self.squares[x*3+y][row*3+col] = self.rows[row+x*3][col+y*3]
        return

    def updatefromrows(self):
        self.colsfromrows()
        self.squaresfromrows()
        return

    def squarefromrowcol(self,row,col):
        return (row//3)*3+col//3

    def determinepossibilities(self,row,col):
        if self.rows[row][col] != " ":
            raise ValueError
        possibilities = ["1","2","3","4","5","6","7","8","9"]
        for val in self.rows[row] + self.cols[col] + self.squares[self.squarefromrowcol(row,col)]:
            if val in possibilities:
                possibilities.remove(val)
        return possibilities

    def full(self):
        for row in self.rows:
            if " " in row:
                return False
        return True

    def valid(self):
        #returns True if is valid, False if there is an error
        L = self.rows + self.cols + self.squares
        for sublist in L:
            R = ["1","2","3","4","5","6","7","8","9"]
            for val in sublist:
                if val == " ":
                    continue
                try:    
                    R.remove(val)
                except:
                    return False
        return True

    def solve(self):
        while True:
            print(self.printtostring(),"---",slen(self.printtostring()),"---",self.level)
            if not self.valid():
                return False
            if self.full():
                return True
            solves = []
            possibilities = []
            for x in range(9):
                for y in range(9):
                    try:
                        p = self.determinepossibilities(x,y)
                        possibilities.append((x,y,p))
                        if len(p) == 0:
                            return False
                        if len(p) == 1:
                            solves.append((x,y,p[0]))
                    except ValueError:
                        pass
            if solves:
                #for solve in solves:
                solve = solves[0]
                self.setcell(solve[0],solve[1],solve[2])
                continue
            possibilities.sort(key=lambda x: len(x[2]))
            if self.level == 17:
                pass
                #pdb.set_trace()
            for poss in possibilities:
                for val in poss[2]:
                    B = Board()
                    B.level = self.level + 1
                    B.readfromstring(self.printtostring())
                    B.setcell(poss[0],poss[1],val)
                    if B.solve():
                        self.readfromstring(B.printtostring())
                        return True
            return False
                


p0 = "987654321123789456000000000000000000000000000000000000000000000000000000000000000"
p1 = "000000000000000000000000000000000000000000000000000000000000000000006823239841567" #solution with like gaps removed
p2 = "042050000000600020067090380400001806006308700708900003053080670070006000000020150"#Easy
p3 = "400000006300007090260354080000640807000905000602083000020431075040800009700000008"#Medium
p4 = "000100003010000249700009500321000004000060000600000187003900002285000090900008000"#Hard
p5 = "384060000070980300000000700000028009050000030900510000001000000002043080000050674"#Evil
p6 = "100000300000500000000070006000200040008090000000000000000000000000000000000000011"#unbeatable
p7 = "820951000000807000030000008018000007000000000200000540400000070000204005000713026"
p8 = "108520000002300000095160000009870500510200060004015200001080740000002100000001908"
p9 = "2356 9 48 9 23856 86  45239 268539 4 584923 6349  68255 238469 68492  539 356 482"
# solvable if  ^ this number is 5. Make it zero, program gets stuck.

def slen(s):
    x = 0
    for c in s:
        if c not in " 0":
            x += 1
    return x

def randomsudoku(nums):
    board = "123456789456789123789123456231674895875912364694538217317265948542897631968341572"
    l = list(board)
    x = 0
    while x != nums:
        r = randint(0,80)
        if l[r] != "0":
            x+=1
            l[r] = "0"
    return "".join(l)



def printsolve(bs):
    try:
        S = Board()
        S.readfromstring(bs)
        S.drawboard()
        S.solve()
        S.drawboard()
        print(S.printtostring())
    except KeyboardInterrupt:
        print()
        print(bs)

bs = randomsudoku(50)
printsolve(bs)
