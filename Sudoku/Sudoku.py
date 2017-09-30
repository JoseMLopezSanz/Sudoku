import sys
from copy import deepcopy
import numpy as np
import cv2

def output(a):
    sys.stdout.write(str(a))

def print_field_cv(field):
    #Don't change the size. If another size is requiered resze the image at the end
    H=500
    W=500
    img=np.zeros((H, W), dtype=np.uint8)
    #create grid
    for i in range(8):
        if (i+1)%3 == 0:
            thick=2
        else:
            thick=1
        cv2.line(img, (0,(i+1)*H/9), (W,(i+1)*H/9), 255, thick)
    for j in range(8):
        if (j+1)%3 == 0:
            thick=2
        else:
            thick=1
        cv2.line(img, ((j+1)*W/9,0), ((j+1)*W/9,H), 255, thick)

    #fill grid
    for i in range(N):
        for j in range(N):
            cell=field[i][j]
            if cell != 0 and not isinstance(cell, set):
                cv2.putText(img, str(cell), (10+(j)*55,50+(i)*55), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            elif isinstance(cell, set):
                for x in range(len(cell)):
                    if 1 in cell:
                        cv2.putText(img, str(1), (10+(j)*55-5,50+(i)*55-33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    if 2 in cell:
                        cv2.putText(img, str(2), (10+(j)*55-5+18,50+(i)*55-33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    if 3 in cell:
                        cv2.putText(img, str(3), (10+(j)*55-5+36,50+(i)*55-33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    if 4 in cell:
                        cv2.putText(img, str(4), (10+(j)*55-5,50+(i)*55-33+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    if 5 in cell:
                        cv2.putText(img, str(5), (10+(j)*55-5+18,50+(i)*55-33+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    if 6 in cell:
                        cv2.putText(img, str(6), (10+(j)*55-5+36,50+(i)*55-33+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    if 7 in cell:
                        cv2.putText(img, str(7), (10+(j)*55-5,50+(i)*55-33+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    if 8 in cell:
                        cv2.putText(img, str(8), (10+(j)*55-5+18,50+(i)*55-33+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    if 9 in cell:
                        cv2.putText(img, str(9), (10+(j)*55-5+36,50+(i)*55-33+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

    cv2.imshow("SUDOKU", img)
    cv2.waitKey()

def print_field(field):
    if not field:
        output("\nNo solution \n \n")
        return
    for i in range(N):
        for j in range(N):
            cell=field[i][j]
            if cell == 0 or isinstance(cell,set):
                output('.')
            else:
                output(cell)
            if(j+1)%3 == 0 and j<8:
                output(' |')

            if j !=8:
                output(' ')
        output('\n')
        if (i+1)%3 == 0 and i <8:
               output("- - - + - - - + - - -\n")

def read(field):
    """Read field into state (replace 0 with set of possible values)"""

    state = deepcopy(field)
    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if cell == 0:
                state[i][j] = set(range(1,10))

    return state


def done(state):
    """Are we done?"""
    for row in state:
        for cell in row:
            if isinstance(cell, set):
                return False
    return True

def propagate_step(state):
    """Propagate one step """

    new_units = False

    for i in range(N):
        row=state[i]
        #gets the values in the row
        values=set([x for x in row if not isinstance(x,set)])
        for j in range(N):
            #if the cell is a set, substract all the values in the row
            if isinstance(state[i][j], set):
                state[i][j] -= values
                #if there's only one value left in the row then is the cell value
                if len(state[i][j]) == 1:
                    #pop() returns the last item in the list
                    state[i][j] = state[i][j].pop()
                    new_units = True
                #if all the values in the set are gone, then promt an error
                elif len(state[i][j]) == 0:
                    return False, None

    #now it checks the columns
    for j in range(N):
        column = [state[x][j] for x in range(N)]
        values = set([x for x in column if not isinstance(x,set)])
        for i in range(N):
            if isinstance(state[i][j], set):
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    state[i][j]=state[i][j].pop()
                    new_units = True
                elif len(state[i][j]) == 0:
                    return False, None

    #check 3x3 squares
    for x in range(3):
        for y in range(3):
            values = set()
            #gets the values in the 3x3 square
            for i in range(3*x, 3*x+3):
                for j in range(3*y, 3*y+3):
                    cell=state[i][j]
                    if not isinstance(cell, set):
                        values.add(cell)
            #checks the empty ones
            for i in range(3*x, 3*x+3):
                for j in range(3*y, 3*y+3):
                    if isinstance(state[i][j], set):
                        state[i][j] -= values
                        if len(state[i][j]) == 1:
                            state[i][j] = state[i][j].pop()
                            new_units = True
                        elif len(state[i][j]) == 0:
                            return False, None

    #now check for unique positions
    for i in range(N):
        for j in range(N):
            if isinstance(state[i][j],set):
                cell=deepcopy(state[i][j])
                for k in range(N):
                    if isinstance(state[i][k],set) and k != j:
                        cell -= state[i][k]
                    elif not isinstance(state[i][k],set) and k != j:
                        cell -= set(range(state[i][k], state[i][k]+1))
                if len(cell) == 1:
                    state[i][j] = cell.pop()
                    new_units = True

    for j in range(N):
        for i in range(N):
            if isinstance(state[i][j],set):
                cell=deepcopy(state[i][j])
                for k in range(N):
                    if isinstance(state[k][j],set) and k != i:
                        cell -= state[k][j]
                    elif not isinstance(state[k][j],set) and k != i:
                        cell -= set(range(state[k][j], state[k][j]+1))
                if len(cell) == 1:
                    state[i][j] = cell.pop()
                    new_units = True

    for x in range(3):
        for y in range(3):
            for i in range(3*x, 3*x+3):
                for j in range(3*y, 3*y+3):
                    if isinstance(state[i][j], set):
                        cell=deepcopy(state[i][j])
                        for ii in range (3*x, 3*x+3):
                            for jj in range(3*y, 3*y+3):
                                if not(ii == i and jj == j):
                                    if isinstance(state[ii][jj],set):
                                        cell -= state[ii][jj]
                                    elif not isinstance(state[ii][jj],set):
                                        cell -= set(range(state[ii][jj], state[ii][jj]+1))
                        if len(cell) == 1:
                            state[i][j] = cell.pop()
                            new_units = True

    print_field_cv(state)
    return True, new_units

def propagate(state):
    """ Propagate until we reach a fixpoint """
    while True:
        solvable, new_unit = propagate_step(state)
        print_field_cv(state)
        print solvable

        if not solvable:
            return False
        if not new_unit:
            return False

def solve(state):
    """ Solve SUDOKU"""

    solvable = propagate(state)
    print(solvable)

    if not solvable:
        return None

    if done(state):
        return state

    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if isinstance(cell, set):
                for value in cell:
                    new_state = deepcopy(state)
                    new_state[i][j] = value
                    solved = solve(new_state)
                    if solved is not None:
                        return solved
                return None

if __name__ == '__main__':
    N=9

    """field=[[5,1,7,6,0,0,0,3,4],
           [2,8,9,0,0,4,0,0,0],
           [3,4,6,2,0,5,0,9,0],
           [6,0,2,0,0,0,0,1,0],
           [0,3,8,0,0,6,0,4,7],
           [0,0,0,0,0,0,0,0,0],
           [0,9,0,0,0,0,0,7,8],
           [7,0,3,4,0,0,5,6,0],
           [0,0,0,0,0,0,0,0,0]]"""
           
    field=[[0,7,0,6,0,8,2,0,0],
          [0,0,0,0,0,5,0,7,4],
          [0,0,5,0,0,0,0,6,0],
          [0,0,3,0,4,0,0,0,0],
          [0,0,0,0,3,0,6,0,1],
          [0,0,2,0,0,6,3,0,0],
          [0,0,0,4,0,9,0,2,0],
          [1,0,0,0,0,0,0,0,8],
          [0,9,0,0,7,0,0,0,0]]


    """field=[[0,2,3,0,0,9,0,0,0],
           [0,0,0,0,0,4,3,0,1],
           [5,0,0,8,0,0,0,0,0],
           [9,0,5,7,0,0,4,0,0],
           [0,3,7,0,0,0,1,6,0],
           [0,0,6,0,0,3,5,0,9],
           [0,0,0,0,0,2,0,0,7],
           [7,0,1,3,0,0,0,0,0],
           [0,0,0,9,0,0,8,5,0]]"""
           
    """field=[[0,2,6,0,0,0,0,4,0],
           [0,8,7,5,0,0,0,0,0],
           [5,9,0,0,4,0,0,0,0],
           [6,0,4,0,9,0,2,0,0],
           [0,0,8,2,0,1,6,0,0],
           [0,0,5,0,6,0,1,0,7],
           [0,0,0,0,8,0,0,7,6],
           [0,0,0,0,0,6,4,1,0],
           [0,6,0,0,0,0,9,3,0]]"""
    
    """field=[[0,2,3,0,0,9,0,0,0],
           [0,0,0,0,0,4,3,0,1],
           [5,0,0,8,0,0,0,0,0],
           [9,0,5,7,0,0,4,0,0],
           [0,3,7,0,0,0,1,6,0],
           [0,0,6,0,0,3,5,0,9],
           [0,0,0,0,0,2,0,0,7],
           [7,0,1,3,0,0,0,0,0],
           [0,0,0,9,0,0,8,5,0]]"""

    print_field_cv(field)
    print_field(field)
    
    state=read(field)

    print_field(solve(state))

