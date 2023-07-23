from SETTING import *
import numpy as np
from copy import deepcopy
import random 

class HBoard:
    def __init__(self, board, numberreadyToBulb = [], numberOfNumberCell = [],numberBulb =[]):
        self.board = deepcopy(board)
        self.DIMENTION = len(board)
        self.numberreadyToBulb = numberreadyToBulb      
        self.numberOfNumberCell = numberOfNumberCell 
        self.numberBulb = numberBulb                
        self.numberCross = self.setCross()             
        self.numberExplode= -1                     
        self.numberOfNumberExplode = -1            
        self.numberLighted = 0
        self.score = -1000               
        self.isSolution = self.checkEnd()
    
    def reset(self):
        self.__init__(self.board)

    # count number of cell in board that can put bulb in  this 
    # return a list of bulb's location
    def readyToBulb(self):
        res = []
        for i in range(self.DIMENTION):
            for j in range(self.DIMENTION):
                if 0<= self.board[i][j] <=5 or self.board[i][j] == BULB  or (self.board[i][j] + 2)%8 ==0: continue
                res += [(i, j)]
        self.numberreadyToBulb = res
        return res
    
    # count number of cell that have number
    # return a list of cell's location
    def countNumberCell(self):
        count = []
        for i in range(self.DIMENTION):
            for j in range(self.DIMENTION):
                if 0<=self.board[i][j]<=5:
                    count += [(i,j)]
        self.numberOfNumberCell = count
        return count 
    
    #---- count number of bulb in board
    #---- return a list of bulb's location
    def countBulb(self):
        bulbLocal = []
        for i in range(self.DIMENTION):
            for j in range(self.DIMENTION):
                if self.board[i][j]==8:
                    bulbLocal += [(i,j)]
        self.numberBulb = bulbLocal
        return bulbLocal
    
    #---- count number of cross in board (that can't put bulb)
    #---- return number of cross
    def setCross(self):
        count = 0
        for i in range(self.DIMENTION):
            for j in range(self.DIMENTION):
                if self.board[i][j]==0:
                    if i < self.DIMENTION-1 and self.board[i+1][j] == -1:
                        self.board[i+1][j] = -2
                        count +=1
                    if i > 0 and self.board[i-1][j] ==-1:
                        self.board[i-1][j]=-2
                        count +=1
                    if j< self.DIMENTION - 1 and self.board[i][j+1] == -1:
                        self.board[i][j+1]=-2
                        count +=1
                    if j>0 and self.board[i][j-1] == -1:
                        self.board[i][j-1] = -2
                        count +=1
        return count
    
    #---- count number of bulb that explode (when it light up another bulb)
    #---- return number of explore
    def countExplode(self):
        explode = 0
        
        
        #---- check row
        for i in range(self.DIMENTION):
            start = 0
            j = 0
            while j < self.DIMENTION:
                if self.board[i][j] == BULB:
                    start = j
                    k = start + 1
                    while k < self.DIMENTION:
                        if 0 <= self.board[i][k] <= 5:
                            j = k
                            break

                    
                        if self.board[i][k] == 8:
                            explode += 1
                        k += 1
                j += 1
                
        #---- check col
        for i in range(self.DIMENTION):
            start = 0
            j = 0  # Introduce a separate variable to track the current row
            while j < self.DIMENTION:
                if self.board[j][i] == BULB:
                    start = j
                    k = start + 1
                    while k < self.DIMENTION:
                        if 0 <= self.board[k][i] <= 5:
                            j = k
                            break
                        if self.board[k][i] == 8:
                            explode += 1
                        k += 1
                j += 1
        self.numberExplode = explode
        return explode
    
    #---- count number of bulb that not match with number in cell
    #---- return number of numberExplode
    def countNumberExplode(self):
        explode = 0
        numberCell = self.numberOfNumberCell
        for i in range(len(numberCell)):
            x = numberCell[i][0]
            y = numberCell[i][1]
            number = self.board[x][y]
            bulb = 0
            if self.board[x][y] == NONUMBER: continue
            if x+1 < self.DIMENTION:
                bulb +=1 if self.board[x+1][y] == BULB else 0
            if x-1 >= 0:
                bulb +=1 if self.board[x-1][y] == BULB else 0
            if y+1 < self.DIMENTION:
                bulb +=1 if self.board[x][y+1] == BULB else 0
            if y-1 >= 0:
                bulb +=1 if self.board[x][y-1] == BULB else 0
            if bulb != number :
                explode += abs(number - bulb)
        self.numberOfNumberExplode = explode
        return explode
    
    #---- count the number of cell that light up
    #---- return number of lighted
    def countLighted(self):
        light = 0
        for i in range(self.DIMENTION):
            for j in range(self.DIMENTION):
                if self.board[i][j] > 5:
                    light += 1
        self.numberLighted = light
        return light
    
    #---- calculate score of a state (board)
    #---- return score
    def heuristic(self):
        
        countNumberCell = len(self.numberOfNumberCell)
        countNumberBulb = len(self.countBulb())
        countExplore = self.numberExplode
        countNumberExplode = self.numberOfNumberExplode    
        countLight = self.numberLighted
        #score = countLight // (self.DIMENTION*self.DIMENTION -countNumberCell) - countExplore*3 - countNumberExplode*2
        score = countLight - countExplore - countNumberExplode
        #score = self.DIMENTION*countLight/(self.DIMENTION*self.DIMENTION -countNumberCell) - countExplore/countNumberBulb - (self.DIMENTION - 1)*countNumberExplode/countNumberCell
        self.score = score
        return score
    
    #---- change the value of cells when bulb is put
    def lightUp(self, bulbLocal):
        for i in range(len(bulbLocal)):
            x = bulbLocal[i][0]
            y = bulbLocal[i][1]
            nextrow = bulbLocal[i][0]+1
            nextcol = bulbLocal[i][1]+1
            prerow = bulbLocal[i][0]-1
            precol = bulbLocal[i][1]-1
            if nextcol < self.DIMENTION:
                for i in range(nextcol, self.DIMENTION):
                    if 0 <= self.board[x][i]<=5: break
                    if self.board[x][i] == 8: continue
                    self.board[x][i] +=8
            if nextrow < self.DIMENTION:
                for i in range(nextrow, self.DIMENTION):
                    if 0 <= self.board[i][y]<=5: break
                    if self.board[i][y] == 8: continue
                    self.board[i][y] +=8    
            if prerow >= 0:
                for i in range(prerow, -1, -1):
                    if 0 <= self.board[i][y]<=5: break
                    if self.board[i][y] == 8: continue
                    self.board[i][y] +=8
            if precol >= 0:
                for i in range(precol, -1, -1):
                    if 0 <= self.board[x][i]<=5: break
                    if self.board[x][i] == 8: continue
                    self.board[x][i] +=8
        return self.board
    
    #---- change the value of cells when bulb is removed
    def lightOff(self, bulbLocal):
        for i in range(len(bulbLocal)):
            x = bulbLocal[i][0]
            y = bulbLocal[i][1]
            nextrow = bulbLocal[i][0]+1
            nextcol = bulbLocal[i][1]+1
            prerow = bulbLocal[i][0]-1
            precol = bulbLocal[i][1]-1
            c = 0
            if nextcol < self.DIMENTION:
                for i in range(nextcol, self.DIMENTION):
                    if 0 <= self.board[x][i]<=5: break
                    if self.board[x][i] == 8: 
                        c +=1
                        continue
                    self.board[x][i] -=8
                    
            if nextrow < self.DIMENTION:
                for i in range(nextrow, self.DIMENTION):
                    if 0 <= self.board[i][y]<=5: break
                    if self.board[i][y] == 8: 
                        c +=1
                        continue
                    self.board[i][y] -=8    
            if prerow >= 0:
                for i in range(prerow, -1, -1):
                    if 0 <= self.board[i][y]<=5: break
                    if self.board[i][y] == 8: 
                        c +=1
                        continue
                    self.board[i][y] -=8
            if precol >= 0:
                for i in range(precol, -1, -1):
                    if 0 <= self.board[x][i]<=5: break
                    if self.board[x][i] == 8: 
                        c += 1
                        continue
                    self.board[x][i] -=8
            self.board[x][y] = c * 8 -1
        return self.board

    #---- check if the board is a solution
    def checkEnd(self):
        
        for i in range(self.DIMENTION):
            for j in range(self.DIMENTION):
                if self.board[i][j] == EMPTY or self.board[i][j] == CROSS:
                    self.isSolution = False
                    return False
        
        if self.countNumberExplode() > 0 or self.countExplode() > 0:
            self.isSolution = False
            return False
        
        self.isSolution = True
        return True

##############################################################################
##############################################################################            
########################### SIMULATED HEURISTIC ####################################
##############################################################################
##############################################################################
import time
def simulated_annealing(problem, numberiterator):
   
    size = problem.start.DIMENTION
    current = problem.start
    goalState = problem.goal
    path = []
    for t in range(int(numberiterator)):

        T = problem.schedule(t) 
        nextState, nextValue, type = problem.getNeighbors(current)
        if current.checkEnd():
            path += [deepcopy(current)]
            return path
        if nextValue > goalState.score:
            # goalState = nextState
            # path += [goalState]
            goalState = deepcopy(nextState)
            path += [deepcopy(goalState)]
            
        if nextValue > current.score:  
            # current = nextState
            current = deepcopy(nextState)
        else:
            randum = np.random.rand()
            E = -abs(current.score - nextValue)
            p = np.exp(E/T)
            if randum < p:
                # current = nextState
                current = deepcopy(nextState)
        for i in range(size):
            print(current.board[i])
        print(f'### {current.score}******T={T}******i={t} ###')
    return path

class problem:
    def __init__(self, start , Cc, Pp, numIter):
        self.DIMENTION = start.DIMENTION
        self.start = None #start
        self.goal = None #deepcopy(start)
        self.Cc = Cc
        self.Pp = Pp
        self.numIter= numIter
    
    def reset(self):
        self.__init__([], 1, 1, 1)

    def schedule(self, t):
        # return self.Cc/(t + 1)**self.Pp
        # return 100/np.log(t + 1)
        return 100/np.log(t + 1)
    #---- get the candidate state
    #---- return the next state, value of next state 
    def getNeighbors(self, board):
        newBoard = deepcopy(board)
        newBoard.countLighted()
        newBoard.readyToBulb()
        if newBoard.numberLighted < self.DIMENTION/2:
            p = np.random.rand()
            if p > newBoard.numberLighted/(self.DIMENTION*self.DIMENTION - len(newBoard.numberOfNumberCell)):
                add = self.addToNextState(newBoard)
                return (add[0],add[1], "add")
        if len(newBoard.numberreadyToBulb) < self.DIMENTION/2:
            p = np.random.rand()
            if p > len(newBoard.numberreadyToBulb)/(self.DIMENTION*self.DIMENTION - len(newBoard.numberOfNumberCell)):
                dell = self.delToNextState(newBoard)
                return (dell[0],dell[1], "dell")
        add = self.addToNextState(newBoard)
        dell = self.delToNextState(newBoard)
        move = self.moveToNextState(newBoard)
        # m = random.choice([add[1], dell[1], move[1]])
        m = max(add[1], dell[1], move[1])
        
        if m == add[1]:
            return (add[0],add[1], "add")
        if m ==  dell[1]:
            return (dell[0],dell[1],  "del")
        if m == move[1]:
            return (move[0],move[1], "move")

    #---- chose the number of ready cell to bulb          
    def randomeBulb(self, board, num):
        
        CellForBulb = board.readyToBulb()
       
        if len(CellForBulb) < num:
            return CellForBulb
        
        if num <= 0:
            return []
        
        newBulb = random.sample(CellForBulb,num)

        return newBulb
    
    def prepareToSearch(self,old_board: HBoard):

        board = deepcopy(old_board) ########### The bug that made the Play Again button did not work
        # board = old_board
        board.setCross()
        numberBulb = self.setBulb(board)
        board.lightUp(numberBulb)          
        
        numNewBulb = self.DIMENTION*2 - len(numberBulb)
        
        newBulbLocation = self.randomeBulb(board,numNewBulb)
        
        for i in range(len(newBulbLocation)):
            board.board[newBulbLocation[i][0]][newBulbLocation[i][1]] = BULB

        board.numberBulb += newBulbLocation
        board.lightUp(newBulbLocation)
        board.countExplode()
        board.countNumberExplode()
        board.readyToBulb()
        board.heuristic()

        return board
    #---- set the bulb to match with the number in cell (not care about the explode)
    def setBulb(self,board):
        numberCell = board.countNumberCell()
        bulbReal = []
        for i in range(len(numberCell)):
            x = numberCell[i][0]
            y = numberCell[i][1]
            if board.board[x][y] != NONUMBER and board.board[x][y] != NUMBER0:
                bulb = []
                if x+1 < self.DIMENTION:
                    bulb += [(x+1,y)] if board.board[x+1][y] == EMPTY else []
                if x-1 >= 0:
                    bulb += [(x-1,y)] if board.board[x-1][y] == EMPTY else []
                if y+1 < self.DIMENTION:
                    bulb += [(x,y+1)] if board.board[x][y+1] == EMPTY else []
                if y-1 >= 0:
                    bulb+= [(x,y-1)] if board.board[x][y-1] == EMPTY else []
                
                if bulb:
                    if len(bulb) < board.board[x][y]:
                        bulbReal = bulb
                    else:
                        bulbReal = random.sample(bulb, board.board[x][y])
                    board.numberBulb += bulbReal
                    for x in bulbReal:
                        board.board[x[0]][x[1]] = BULB
        return board.numberBulb
        
    #---- move to next state by add a bulb to a current state
    #---- return the new state, the heuristic of new state and the location of new bulb
    def addToNextState(self, board):
        
        newBoard = deepcopy(board)
        res = ([],-1000,(-1,-1))
        score = -1000
        readyToBulb = newBoard.numberreadyToBulb
        
        if len(readyToBulb) > self.DIMENTION:
            
            nextBulb = random.sample(readyToBulb, self.DIMENTION)
            
            for i in range(len(nextBulb)):                
                tmpBoard = deepcopy(newBoard)
                
                
                tmpBoard.numberreadyToBulb.remove(nextBulb[i])
                tmpBoard.numberBulb += [nextBulb[i]]
                
                tmpBoard.board[nextBulb[i][0]][nextBulb[i][1]] = BULB
                tmpBoard.lightUp([nextBulb[i]])
                
                tmpBoard.countExplode()
                tmpBoard.countNumberExplode()
                tmpBoard.countLighted()                
                
                h = tmpBoard.heuristic()

                if h > score:
                    score = h
                    res = (tmpBoard, h, nextBulb[i])   #  nextBulb for what
        elif len(readyToBulb) > 0:
            
            for i in range(len(readyToBulb)):
                tmpBoard = deepcopy(newBoard)
                tmpBoard.numberreadyToBulb.remove(readyToBulb[i])
                tmpBoard.numberBulb += [readyToBulb[i]]
                tmpBoard.board[readyToBulb[i][0]][readyToBulb[i][1]] = BULB
                tmpBoard.lightUp([readyToBulb[i]])
                tmpBoard.countExplode()
                tmpBoard.countNumberExplode()
                tmpBoard.countLighted()                  
                h = tmpBoard.heuristic()
                if h > score:
                    score = h
                    res = (tmpBoard,h,readyToBulb[i])
        return res
    
    #---- move to next state by delete a bulb to a current state
    #---- return the new state, the heuristic of new state and the location of new bulb
    def delToNextState(self, board):
        
        curBoard = deepcopy(board)
        res = ([],-1000,(-1,-1))
        score = -1000
        curBulb = curBoard.numberBulb
        
        if len(curBulb) > self.DIMENTION:
            delBulb = random.sample(curBulb, self.DIMENTION)
            for i in range(len(delBulb)):
                tmpBoard = deepcopy(curBoard)
                
                tmpBoard.numberreadyToBulb += [delBulb[i]]
                tmpBoard.numberBulb.remove(delBulb[i])
                tmpBoard.lightOff( [delBulb[i]])
                tmpBoard.countExplode()
                tmpBoard.countNumberExplode()
                tmpBoard.countLighted()

                h = tmpBoard.heuristic()
                if h > score:
                    score = h
                    res = (tmpBoard,h, delBulb[i])
                    
            # if dell:
            #     curBulb = curBulb.remove(res[2])
        elif len(curBulb) > 0:
            for i in range(len(curBulb)):
                tmpBoard = deepcopy(curBoard)
                tmpBoard.numberreadyToBulb += [curBulb[i]]
                tmpBoard.numberBulb.remove(curBulb[i])
                tmpBoard.lightOff([curBulb[i]])
                tmpBoard.countExplode()
                tmpBoard.countNumberExplode()
                tmpBoard.countLighted()
                
                h=tmpBoard.heuristic()
                
                if h > score:
                    score = h
                    res = (tmpBoard,h,curBulb[i])
        return res
    
    #---- move to next state by move a bulb for a cell to another state
    #---- return the new state, the heuristic of new state and the location of new bulb
    def moveToNextState(self,board):
        curBoard = deepcopy(board)
        score = -1000
        res = ([],-1000)
        
        readyToBulb = curBoard.numberreadyToBulb
        curBulb = curBoard.numberBulb
        
        if len(readyToBulb) > 0 and len(curBulb) > 0:
            for i in range(self.DIMENTION):
                if curBulb:
                    Bulb = random.sample(curBulb,1)
                    if readyToBulb:
                        tmpFree = random.sample(readyToBulb,1)
                        
                        tmpBoard = deepcopy(curBoard)
                        
                        tmpBoard.numberreadyToBulb += Bulb
                        tmpBoard.numberBulb.remove(Bulb[0])
                        tmpBoard.lightOff(Bulb)
                        
                        tmpBoard.numberBulb += tmpFree
                        tmpBoard.numberreadyToBulb.remove(tmpFree[0])
                        tmpBoard.board[tmpFree[0][0]][tmpFree[0][1]] = BULB
                        tmpBoard.lightUp(tmpFree)
                        
                        tmpBoard.countExplode()
                        tmpBoard.countNumberExplode()
                        tmpBoard.countLighted()
                        
                        h = tmpBoard.heuristic()
                        if h > score:
                            score = h
                            res = (tmpBoard,h)
        return res