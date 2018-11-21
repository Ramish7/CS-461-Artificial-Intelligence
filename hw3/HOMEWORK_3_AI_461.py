'''
We have used Sum of Euclidian distances of the tiles from their goal positions (h2 is an admissible
heuristic, since in every move, one tile can only move closer to its goal by one step and
the Euclidian distance is never greater than the number of steps required to move a tile
to its goal position)
'''

import random
import numpy as np

finalBoard=[0,2,3,4,5,6,7,8,9]

#checks whether the puzzle generated is solvable or not
def IsSolvable(List):
    inversion = 0
    for i in range (0, len(List)-1):
        for j in range (i+1, len(List)):
            if(List[j] != 0 & List[i] != 0 & List[i] > List [j]):
                inversion = inversion + 1
            
    return (inversion % 2 == 0)

#generates a random puzzle
def generatePuzzle():
    solvable = False
    list_1 = [0,2,3,4,5,6,7,8,9]
    list_2 = [2,3,4,5,6,7,8,9]
    
    arr = np.arange(2)
    np.random.shuffle(arr)
    
    list_begin = arr
    if(list_begin[0] == 1):
        List = list_1
        add = 1
    else:
        List = list_2
        add = 2
    
    while(solvable != True ):
        random.shuffle(List)
        if(IsSolvable(List)):
            solvable = True
    if add == 1 :
        List = [1]+List
    if add == 2 :
        List = [0,1]+List
        
    return List

#converts a 9-puzzle into 8
def puzzle_9_8(List): 
    if List[0]==1:
        return List[1:len(List)]
    else:
        return [0]+List[2:len(List)]
    
#converts a 8 puzzle into 9
def puzzle_8_9(List): 
    return [1]+List

#checks whether the final solution has reached the goal state or not
def goalTest(state):
    for x in range (0,9):
        if state[x]!=finalBoard[x]:
            return False
    return True

#finds the actions that are needed to reach to the children state
def findActionsToChildren(state):
    position = state.index(0)
    if position==0:
        return[2,4]
    elif position==1:
        return[2,3,4]
    elif position==2:
        return[2,3]
    elif position==3:
        return[1,2,4]
    elif position==4:
        return[1,2,3,4]
    elif position==5:
        return[1,2,3]
    elif position==6:
        return[1,4]
    elif position==7:
        return[1,3,4]
    else:
        return[1,3]

#after each move, children are appended to the parent and total distance till that [point is calculated
def getChildrenStates(initialState,actions):
    childrenStates=[]
    zeroPlace=initialState[0].index(0)
    for x in actions:
        first=list(initialState[0])
        second=list(initialState[1])
        state=[first,second]
        if x==1:
            state[0][zeroPlace] = state[0][zeroPlace-3]
            state[0][zeroPlace-3] = 0
            state[1][0]=state[1][0]+1
            state[1][1]=1
            childrenStates.append(state)
        elif x==2:
            state[0][zeroPlace] = state[0][zeroPlace+3]
            state[0][zeroPlace+3] = 0
            state[1][0]=state[1][0]+1
            state[1][1]=2
            childrenStates.append(state)
        elif x==3:
            state[0][zeroPlace] = state[0][zeroPlace-1]
            state[0][zeroPlace-1] = 0
            state[1][0]=state[1][0]+1
            state[1][1]=3
            childrenStates.append(state)
        else:
            state[0][zeroPlace] = state[0][zeroPlace+1]
            state[0][zeroPlace+1] = 0
            state[1][0]=state[1][0]+1
            state[1][1]=4
            childrenStates.append(state) 
    return childrenStates

#checks whether the states are already visited or not
def checkAlreadyIn(state,visitedStates,queue):
    for y in visitedStates:
        if state[0]==y[0]:
            return True
    for y in queue:
        if state[0]==y[0]:
            return True
    return False

#adds children to the queue
def addChildrenToQueue(children,queue,visitedStates):
    for x in children:
        if not checkAlreadyIn(x,visitedStates,queue):
            queue.append(x)
#
def getReverseActionState(state):
    action = state[1][1]
    zeroPlace=state[0].index(0)
    if action==1:
        state[0][zeroPlace] = state[0][zeroPlace+3]
        state[0][zeroPlace+3] = 0
        return state[0]
    elif action==2:
        state[0][zeroPlace] = state[0][zeroPlace-3]
        state[0][zeroPlace-3] = 0
        return state[0]
    elif action==3:
        state[0][zeroPlace] = state[0][zeroPlace+1]
        state[0][zeroPlace+1] = 0
        return state[0]
    else:
        state[0][zeroPlace] = state[0][zeroPlace-1]
        state[0][zeroPlace-1] = 0
        return state[0]

#appends the states for each level
def findStatesInLevel(visitedStates,level):
    result=[]
    for x in visitedStates:
        if x[1][0]==level:
            result.append(x)
    return result

#gets the solution for each state reached
def getSolutionActions(visitedStates):
    actions=[]
    node = visitedStates[-1]
    solutionLevel = node [1][0]
    actions.insert(0,node[1][1])
    for x in range(solutionLevel-1,0,-1):
        upperLayerStates=findStatesInLevel(visitedStates,x)
        node = getReverseActionState(node)
        lenght = len(upperLayerStates)
        if not lenght==1:
            for y in range(0,lenght):
                if upperLayerStates[y][0]==node:
                    node = upperLayerStates[y]
                    break
        else:
            node=upperLayerStates[0]
        actions.insert(0,node[1][1])
    return actions

def getThirdElement(a):
    return a[2]
#
def reorderQueue(queue):
    queue.sort(key=getThirdElement)

#gets the heuristic distance for each state
def getHeuristic(state):
    sum=0
    for x in range(2,10):
        lineDistance=abs(state.index(x)-finalBoard.index(x))
        k=lineDistance%3
        b=(lineDistance-k)//3
        sum=sum+(k+b)
    return sum

#adds the heurisitc to the children state
def addHeuristicToChildren(children):
    for x in range(0,len(children)):
        heuristic=getHeuristic(children[x][0])
        total=getHeuristic(children[x][0])+children[x][1][0]
        children[x].append([total])

#took the ast algorithm from internet
def ast(board):
    board = [board,[0,0],[getHeuristic(board)]]
    queue = [board]
    visitedStates=[]
    maxSizeOfQueue=0
    maxDepthOfSearch=0
    while not goalTest(queue[0][0]):
        nowWisiting=queue[0]
        del queue[0]
        actions = findActionsToChildren(nowWisiting[0])
        children = getChildrenStates(nowWisiting,actions)
        addHeuristicToChildren(children)
        depthOfChildren=children[0][1][0]
        if maxDepthOfSearch<depthOfChildren:
            maxDepthOfSearch=depthOfChildren
        addChildrenToQueue(children,queue,visitedStates)
        reorderQueue(queue)
        leghtOfQueue = len(queue)
        if maxSizeOfQueue< leghtOfQueue :
            maxSizeOfQueue=leghtOfQueue
        visitedStates.append(nowWisiting)
    
    visitedStates.append(queue[0])
    actions=getSolutionActions(visitedStates)
    return actions

#        MAIN
from tkinter import * 
root = Tk() 

#Graphical Solution part
board = generatePuzzle()

if (board[1]==1):
    L = Label(text="0",width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
    L.grid(row=0,column=0)
    board = puzzle_9_8(board)
    actions = ast(board) 
    Initial_State = board 
    for i in range(3): 
        L = Label(text=Initial_State[i],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
        L.grid(row=1,column=i)
    for i in range(3): 
        L = Label(text=Initial_State[i+3],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
        L.grid(row=2,column=i)
    for i in range(3): 
        L = Label(text=Initial_State[i+6],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
        L.grid(row=3,column=i)
        
    L = Label(text="1",width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
    L.grid(row=1,column=0)
    
    tempBoard=[board,[0,0]]  
    x=-1
    def show_position(event): 
                global x
                if x==-1: 
                    L = Label(text="1",width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                    L.grid(row=0,column=0)
                    Initial_State = board 
                    for i in range(3): 
                        L = Label(text=Initial_State[i],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                        L.grid(row=1,column=i)
                    for i in range(3): 
                        L = Label(text=Initial_State[i+3],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                        L.grid(row=2,column=i)
                    for i in range(3): 
                        L = Label(text=Initial_State[i+6],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                        L.grid(row=3,column=i)
                    L = Label(text="DOWN",width=5,font='Helvetica 10 bold',highlightthickness=1)
                    L.grid(row=2,column=6)
                    
                
                
                x = x+1 
                if x<len(actions): 
                    global tempBoard 
                    action=[actions[x]]
                    tempBoard = getChildrenStates(tempBoard,action)
                    tempBoard = tempBoard[0] 
                    State = tempBoard[0] 
                    for i in range(3): 
                        L = Label(text=State[i],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                        L.grid(row=1,column=i)
                    for i in range(3): 
                        L = Label(text=State[i+3],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                        L.grid(row=2,column=i)
                    for i in range(3): 
                        L = Label(text=State[i+6],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                        L.grid(row=3,column=i) 
                    if actions[x]==1:
                            L = Label(text="UP",width=5,font='Helvetica 10 bold',highlightthickness=1)
                            L.grid(row=2,column=6)
                    elif actions[x]==2:
                             L = Label(text="DOWN",width=5,font='Helvetica 10 bold',highlightthickness=1)
                             L.grid(row=2,column=6)
                    elif actions[x]==3:
                             L = Label(text="LEFT",width=5,font='Helvetica 10 bold',highlightthickness=1)
                             L.grid(row=2,column=6)
                    elif actions[x]==4:
                             L = Label(text="RIGHT",width=5,font='Helvetica 10 bold',highlightthickness=1)
                             L.grid(row=2,column=6)


                else: 
                    L = Label(text="DONE !",width=5,font='Helvetica 12 bold',highlightthickness=1)
                    L.grid(row=4,column=1)
                    L = Label(text="0",width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1)
                    L.grid(row=0,column=0)
                    L = Label(text="1",width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1)
                    L.grid(row=1,column=0)
     
else:     

    L = Label(text="1",width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
    L.grid(row=0,column=0)
    board = puzzle_9_8(board)
    Initial_State = board 
    for i in range(3): 
        L = Label(text=Initial_State[i],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
        L.grid(row=1,column=i)
    for i in range(3): 
        L = Label(text=Initial_State[i+3],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
        L.grid(row=2,column=i)
    for i in range(3): 
        L = Label(text=Initial_State[i+6],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
        L.grid(row=3,column=i)

    actions = ast(board)
    x=-1 
    tempBoard=[board,[0,0]]  
    def show_position(event): 
            global x 
            x = x+1 
            if x<len(actions): 
                global tempBoard 
                action=[actions[x]]
                tempBoard = getChildrenStates(tempBoard,action)
                tempBoard = tempBoard[0] 
                State = tempBoard[0] 
                for i in range(3): 
                    L = Label(text=State[i],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                    L.grid(row=1,column=i)
                for i in range(3): 
                    L = Label(text=State[i+3],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                    L.grid(row=2,column=i)
                for i in range(3): 
                    L = Label(text=State[i+6],width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1) 
                    L.grid(row=3,column=i) 
                if actions[x]==1:
                        L = Label(text="UP",width=5,font='Helvetica 10 bold',highlightthickness=1)
                        L.grid(row=2,column=6)
                elif actions[x]==2:
                         L = Label(text="DOWN",width=5,font='Helvetica 10 bold',highlightthickness=1)
                         L.grid(row=2,column=6)
                elif actions[x]==3:
                         L = Label(text="LEFT",width=5,font='Helvetica 10 bold',highlightthickness=1)
                         L.grid(row=2,column=6)
                elif actions[x]==4:
                         L = Label(text="RIGHT",width=5,font='Helvetica 10 bold',highlightthickness=1)
                         L.grid(row=2,column=6)

                 
            else: 
                L = Label(text="DONE !",width=5,font='Helvetica 12 bold',highlightthickness=1)
                L.grid(row=4,column=1) 
                L = Label(text="0",width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1)
                L.grid(row=0,column=0)
                L = Label(text="1",width=5,font='Helvetica 12 bold',bg="SkyBlue",highlightthickness=1)
                L.grid(row=1,column=0)

B = Button(root, text='Solve', bg="Green", fg="Black",width=4,height=1,font=('Helvetica','12'))
B.grid(row=4, column=2)
B.bind('<Button-1>', show_position) 

root.geometry("700x700") 
root.mainloop()  
    
    

