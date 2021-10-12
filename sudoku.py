############################################################
# CIS 521: Sudoku Homework 
############################################################

student_name = "Xiaoyi Wu"

############################################################
import collections
from copy import deepcopy
############################################################

# Include your imports here, if any are used.



############################################################
# Section 1: Sudoku Solver
############################################################

def sudoku_cells():
    ls=[]
    for i in range(9):
        for j in range(9):
            ls.append((i,j))
    return ls
# return list of all arcs which need to follow constraints
# row, col, subgrid
def sudoku_arcs():
    ls=[]
    for i in range(9):
        for j in range(9):
            p=(i,j)
            for m in range(9):
                if m !=i:
                    ls.append((p,(m,j)))
                if m!=j:
                    ls.append((p,(i,m)))
            for sub1 in range(int(i/3)*3,int(i/3)*3+3):
                for sub2 in range(int(j/3)*3,int(j/3)*3+3):
                    if sub1 != i or sub2 !=j:
                        ls.append((p,(sub1,sub2)))

    ls =list(set(ls))
    # set 会过滤掉重复的值
    return ls

def read_board(path):
    dic={}
    i=0
    j=0
    l=set(list((1,2,3,4,5,6,7,8,9)))
    with open(path) as f:
        lines=f.read().split()
        for line in lines:
            for word in line:
                if word=='*':
                    dic[(i,j)]=l
                else:
                    dic[(i,j)]=set([int(word)])
                j=(j+1)%9
            i=(i+1)%9
    return dic

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board=board


    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        ## 这里的constraint是同一行、同一列、同一个subgrid不能有相同值
        inconsistent_values=set()
        ls1=list(self.board[cell1])
        ls2=list(self.board[cell2])
        # todo: check cell2
        # 如果 y中没有一个值满足contraint，就不是arc-consistent
        if len(ls2)>1:
            return False
        else:
            for i in ls1:
                for j in ls2:
                    if i == j:
                        inconsistent_values.add(i)
                        ls1.pop(ls1.index(i))
        self.board[cell1]=set(ls1)
        return len(inconsistent_values)>0

    def infer_ac3(self):
        queue=collections.deque(Sudoku.ARCS)
        while queue:
           c1,c2=queue.pop()
           if self.remove_inconsistent_values(c1,c2):
               if self.board[c1] ==():
                   return False
               # if x_i is removed/revised, add (X_k,X_i)
               # into agenda/queue
               for arc in Sudoku.ARCS:
                   if arc[1]==c1 and arc[0]!=c2:
                       queue.append(arc)
        return self.board

    def check_unique(self,cell,val):

        for i in range(9):
            if i!=cell[1]:
                if val in self.board[(cell[0],i)]:
                    return False
            if i!=cell[0]:
                if val in self.board[(i,cell[1])]:
                    return False
        for sub1 in range(int(cell[0] / 3) * 3, int(cell[0] / 3) * 3 + 3):
            for sub2 in range(int(cell[1]/ 3) * 3, int(cell[1] / 3) * 3 + 3):
                if sub1 != cell[0] or sub2 != cell[1]:
                    if val in self.board[(sub1,sub2)]:
                        return False
        return True



      #cell is position
        #i is the position value
    def infer_improved(self):
        made_additional_inference=True
        while made_additional_inference:
            #todo: check the status of self.infer_ac3
            # if it is empty, the process fails

            self.infer_ac3()
            made_additional_inference = False
            for cell in Sudoku.CELLS:
                a=list(self.board[cell])
                if len(a)>1:
                    # todo: the standard of uniqueness: how to check the value of cell
                    for i in a:
                        if self.check_unique(cell,i):
                            self.board[cell]=set([i])
                            made_additional_inference = True
                            break
        return self.board

    def is_solved(self):
        for cell in self.CELLS:
            a=list(self.board[cell])
            if len(a)!=1:
                return False
            else:
                if not self.check_unique(cell,a[0]):
                    return False
        return True

    def infer_with_guessing(self):
        self.infer_improved()
        for cell in Sudoku.CELLS:
            a = list(self.board[cell])
            if len(a)>1:
                for i in a:
                    p=deepcopy(self)
                    p.board[cell]=set([i])
                    p.infer_improved()
                    if p.is_solved():
                        self.board=p.board
                        return self.board
                        break
                    else:
                        p.infer_with_guessing()
                break
        return self.board

sudoku = Sudoku(read_board("sudoku/hard1.txt"))
# See below for a picture.
for i in range(9):
    for j in range(9):
        if i !=0:
            removed = sudoku.remove_inconsistent_values((0, 4), (i, 4))
            print(sudoku.board[(i,4)], sudoku.get_values((0, 4)))

        if i!=4:
            removed = sudoku.remove_inconsistent_values((0, 4), (0, i))

            print(sudoku.board[(0,i)], sudoku.get_values((0, 4)))
        for sub1 in range(int(0 / 3) * 3, int(0/ 3) * 3 + 3):
            for sub2 in range(int(4 / 3) * 3, int(4/ 3) * 3 + 3):
                if sub1 != 0 or sub2 != 4:
                    removed = sudoku.remove_inconsistent_values((0, 4), (sub1,sub2))
                    print(sudoku.board[(sub1,sub2)], sudoku.get_values((0, 4)))

# b=sudoku.is_solved()
# print(a)
# print(b)

############################################################
# Section 2: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 10

feedback_question_2 = """
the second question
"""

feedback_question_3 = """
It introduces how to solve Sudoku
"""
