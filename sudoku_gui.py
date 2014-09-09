# encoding = utf-8
import random
from sys import exit
from copy import deepcopy
import pygame
from pygame.locals import *
import pygame._view #to solve cx_freeze exceptions.
import sys
import string

'''global parameter define
'''
dbg_on = 1
timer='00:00:00'
run=0
board = [[0 for i in range(9)] for i in range(9)]
x_loc = 4
y_loc = 4
check_mode=0

update_value_dict = {K_1:1, K_2:2, K_3:3, K_4:4, K_5:5, K_6:6, K_7:7, K_8:8, K_9:9}
guess_value_dict = {K_KP1:1, K_KP2:2, K_KP3:3, K_KP4:4, K_KP5:5, K_KP6:6, K_KP7:7, K_KP8:8, K_KP9:9}
move_dict = {K_UP   :{'delta_x':0, 'delta_y':8, 'delta_chk':0},
             K_DOWN :{'delta_x':0, 'delta_y':1, 'delta_chk':0},
             K_LEFT :{'delta_x':8, 'delta_y':0, 'delta_chk':0},
             K_RIGHT:{'delta_x':1, 'delta_y':0, 'delta_chk':0},
             K_SLASH:{'delta_x':0, 'delta_y':0, 'delta_chk':1}}

pygame.init()

'''pygame draw box parameters
'''
box_size = 50
box_gap  = 1 #the slimer line gap
box_gap2  = 5 #the thicker line gap
top_of_screen = 100
bottom_of_screen = 30
left_of_screen = 20
screen_width  = box_size * 9 + box_gap * 6 + box_gap2*4  + left_of_screen * 2
screen_height = top_of_screen + box_gap * 6 + box_gap2*4 + box_size * 9 + left_of_screen + bottom_of_screen
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption("Sudoku v1.0")
background = pygame.image.load('background.png').convert()
score = 0
best=595959

OLDLACE    = pygame.color.THECOLORS["oldlace"]
IVORY   = pygame.color.THECOLORS["ivory3"]
BLACK   = pygame.color.THECOLORS["black"]
RED     = pygame.color.THECOLORS["red"]
DARKBLUE     = pygame.color.THECOLORS["darkblue"]
RED2    = pygame.color.THECOLORS["red2"]
DARKGOLD  = pygame.color.THECOLORS["darkgoldenrod1"]
GOLD    =  pygame.color.THECOLORS["gold"]
GRAY    = pygame.color.THECOLORS["gray41"]
CHOCOLATE = pygame.color.THECOLORS["chocolate"]
CHOCOLATE1 = pygame.color.THECOLORS["chocolate1"]
CORAL   = pygame.color.THECOLORS["coral"]
CORAL2  = pygame.color.THECOLORS["coral2"]
ORANGED = pygame.color.THECOLORS["orangered"]
ORANGED2 = pygame.color.THECOLORS["orangered2"]
DARKORANGE = pygame.color.THECOLORS["darkorange"]
DARKORANGE2 = pygame.color.THECOLORS["darkorange2"]
FORESTGREEN = pygame.color.THECOLORS['forestgreen']

class sudoku():
    global dbg_on
    '''Sudoku main
    '''
    #init function
    def __init__(self,dbg_on):
        '''parameter initial
        '''
        self.level = 0 #level: 2-hard:24, 1-middle:32, 0-easy:40
        self.MatrixSize = 9
        self.HintNumList = [40, 35, 30]
        self.HintNum = self.HintNumList[self.level]
        if dbg_on ==1:
            print(self.HintNum)
        self.MatrixNum = self.MatrixSize * self.MatrixSize
        self.Done = 0 #sudoku finish flag
        self.Score = 0 #sudoku correct number
        #initial a 9*9 matrix for MatrixSize
        self.MATRIX = [[0 for i in range(self.MatrixSize)] for i in range(self.MatrixSize)]
        #initial array 1-9
        self.CUBIC = [(i+1) for i in range(self.MatrixSize)]
        self.ALLNUM = [i for i in range(self.MatrixNum)]
        self.RandMatrix = self.MATRIX
        self.HintMatrix = self.MATRIX
        self.CurrMatrix = [['*' for i in range(self.MatrixSize)] for i in range(self.MatrixSize)]
        #print(self.CurrMatrix[0][0])
        self.RandPool = []
        self.RandHintPool = []
        self.RowList = [[] for i in range(9)]
        self.ColList = [[] for i in range(9)]
        self.CubList = [[[] for i in range(3)] for i in range(3)]
        self.HintList = []
        self.HintMatrixList = [[[] for i in range(9)] for j in range(9)]
        self.HintMatrixListPre = self.HintMatrixList
        #self.HintMatrixListPre = [[[] for i in range(9)] for j in range(9)]
        self.RowMinList = [[] for i in range(9)]
        self.ColMinList = [[] for i in range(9)]
        self.CubMinList = [[[] for i in range(3)] for i in range(3)]
        self.RowMaxList=[]
        self.ColMaxList=[]
        self.CubMaxList=[]
        self.ValInputList=[]
        self.LocInputList=[]

    #utils function: get input value
    def GetInputVal(self, valname, minrange, maxrange):
        '''get input value
           @return: input value
           @type: int
        '''
        sys.stdout.write('>>>>>>>>>> %s = '%valname)
        inputVal = input()
        illegal_type = (self.InputIllegalChk(inputVal, minrange, maxrange))
        while illegal_type != 0 : #0: no illegal find. others: illegal input.
            print('Wrong %s!(please enter number within %d-%d)'%(valname, minrange, maxrange))
            if dbg_on == 1:
                print("illegal type is: %d(1, null input; 2, not numbers; 3, numbers out of range)"%int(illegal_type))
            sys.stdout.write('>>>>>>>>>> %s = '%valname)
            inputVal = input()
            illegal_type = (self.InputIllegalChk(inputVal, minrange, maxrange))
        return(int(inputVal))

    #utils function: check if input value is illegal or not
    def InputIllegalChk(self, strVal, minrange, maxrange):
        #illegal 1: null input
        if strVal == "":
            return 1
        #illegal 2: input not numbers
        nums = string.digits
        for i in strVal:
            if i not in nums:
                return 2
        #illegal 3: input out of specified range
        if int(strVal) not in range(minrange, (maxrange+1)):
            return 3
        #all check pass
        return 0


    #Step1, initialize a Sudoku
    def iniMatrix(self):
        '''initial random matrix
           choose random hints
        '''
        #clear all to 0 at beginning
        self.Done = 0 #sudoku finish flag
        #initial hints number based on game level
        #self.MatrixDisplay(0)
        #print(self.level)
        self.HintNum = self.HintNumList[self.level]
        self.Score = self.HintNum #sudoku correct number
        if dbg_on ==1:
            print(self.HintNum)

        #generate final matrix
        self.MatrixGen()

        #generate random hint matrix
        self.HintGen()

        #generate curr matrix
        for i in range(9):
            for j in range(9):
                if self.HintMatrix[i][j] != 0:
                    self.CurrMatrix[i][j] = str(self.HintMatrix[i][j])


    def MatrixGen(self):
        retry_cnt=0
        while(self.MatrixRandGen() != 1):
            retry_cnt=retry_cnt+1
            pass
        print('>>>>>>>>>> matrix gen retry cnt is %d'%retry_cnt)

    def MatrixRandGen(self):
        '''random generate a MATRIX
                1: ROW 1-9
                2: COLUMN 1-9
                3: CUBIC 1-9
           @return: gen OK or not
           @type: int
        '''
        #clear MATRIX to all 0
        self.RandMatrix = [[0 for i in range(self.MatrixSize)] for i in range(self.MatrixSize)]
        self.RowList = [[] for i in range(9)]
        self.ColList = [[] for i in range(9)]
        self.CubList = [[[] for i in range(3)] for i in range(3)]

        for i in range(9): #ROW i
            for j in range(9): #COLUMN j
                self.RandPool = self.CUBIC
                if dbg_on == 2:
                    print('i=%d, j=%d'%(i,j))

                self.RandPool = list(set(self.RandPool) - set(self.ColList[j]) - set(self.RowList[i]) - set(self.CubList[int(i/3)][int(j/3)]))

                if dbg_on == 2:
                    print(self.RandPool)
                if self.RandPool != []:
                    self.RandMatrix[i][j] = random.choice(self.RandPool) #random select 1 in pool
                else:
                    if dbg_on == 2:
                        print("Gen fail! return 1!")
                    return 0 #Gen fail

                self.RowList[i].append(self.RandMatrix[i][j])
                self.ColList[j].append(self.RandMatrix[i][j])
                self.CubList[int(i/3)][int(j/3)].append(self.RandMatrix[i][j])

        if dbg_on == 1:
            print(self.RandMatrix)
            print("Gen OK! return 0!")
        return 1 #Gen OK


    def HintGen(self):

        try_cnt=0
        self.RandHintGen()
        try_cnt=try_cnt+1
        while(self.MatrixNotSingle()):
            self.RandHintGen()
            try_cnt=try_cnt+1
        print(">>>>>>>>>> hint_gen try cnt is %d"%try_cnt)


    def RandHintGen(self):
        '''generate random Hint loccation
        '''
        self.HintMatrix = self.MATRIX
        self.RandHintPool = self.ALLNUM
        self.HintList = []

        for i in range(self.HintNum):
            self.RandHintPool = list(set(self.RandHintPool) - set(self.HintList))
            hint = random.choice(self.RandHintPool)
            self.HintList.append(hint)

        if dbg_on == 2:
            print(self.HintList)
            print(self.RandHintPool)

        for i in range(9):
            for j in range(9):
                if self.HintList.count(i*9+j)>0:
                    self.HintMatrix[i][j] = self.RandMatrix[i][j]
                else:
                    self.HintMatrix[i][j] = 0

        if dbg_on == 1:
            print(self.HintMatrix)


    #here need a submodule for hint matrix check, to confirm that it still have single result.
    def MatrixNotSingle(self):
        '''for i in range(9):
            for j in range(9):
                self.HintMatrixList[i][j].append(self.RandMatrix[i][j])'''

        self.RowMinList = [[] for i in range(9)]
        self.ColMinList = [[] for i in range(9)]
        self.CubMinList = [[[] for i in range(3)] for i in range(3)]
        self.HintMatrixList = [[[] for i in range(9)] for j in range(9)]
        self.HintMatrixListPre = [[[] for i in range(9)] for j in range(9)]

        if dbg_on == 2:
            print(">>>>>>>>>> 0000000000 print length now!")
            for i in range(9):
                sys.stdout.write("|")
                for j in range(9):
                    sys.stdout.write(" %d "%(len(self.HintMatrixList[i][j])))
                sys.stdout.write("|\n")

        for i in range(9):
            for j in range(9):
                if (i*9+j) in self.HintList:
                    self.HintMatrixList[i][j].append(self.RandMatrix[i][j])
                else:
                    self.HintMatrixList[i][j] = self.CUBIC

        if dbg_on == 2:
            print(">>>>>>>>>> 1111111111 print length now!")
            for i in range(9):
                sys.stdout.write("|")
                for j in range(9):
                    sys.stdout.write(" %d "%(len(self.HintMatrixList[i][j])))
                sys.stdout.write("|\n")

        reloop = 1
        while(reloop):
            reloop = 0
            #self.HintMatrixListPre = self.HintMatrixList
            for i in range(9):
                for j in range(9):
                    self.HintMatrixListPre[i][j] = self.HintMatrixList[i][j]

            if dbg_on == 2:
                print(self.HintMatrixListPre)
                print(self.HintMatrixList)

            for i in range(9):
                for j in range(9):
                    if (len(self.HintMatrixList[i][j])==1):
                        self.RowMinList[i].append(self.HintMatrixList[i][j][0])
                        self.ColMinList[j].append(self.HintMatrixList[i][j][0])
                        self.CubMinList[int(i/3)][int(j/3)].append(self.HintMatrixList[i][j][0])

            for i in range(9):
                for j in range(9):
                    if (len(self.HintMatrixList[i][j])>1):
                        self.HintMatrixList[i][j] = list(set(self.HintMatrixList[i][j]) - set(self.RowMinList[i]) - set(self.ColMinList[j]) -set(self.CubMinList[int(i/3)][int(j/3)]))

            #ROW/Col/Cub
            for i in range(9):
                for j in range(9):
                    self.RowMaxList=[]
                    self.ColMaxList=[]
                    self.CubMaxList=[]
                    for k in range(9):
                        if k != j:
                            self.RowMaxList.extend(self.HintMatrixList[i][k])#list(set(self.RowRoughList) + set(self.HintMatrixList[i][k]))
                        if k != i:
                            self.ColMaxList.extend(self.HintMatrixList[k][j])#list(set(self.ColRoughList) + set(self.HintMatrixList[k][j]))
                        if (int(k/3) != int(i%3)) or (int(k%3) != int(j%3)):
                            self.CubMaxList.extend(self.HintMatrixList[int(i/3)*3+int(k/3)][int(j/3)*3+int(k%3)])#list(set(self.CubRoughList) + set(self.HintMatrixList[int(i/3)*3+int(k/3)][int(j/3)*3+int(k%3)]))

                    for k in self.CUBIC:
                        if k not in self.RowMaxList:
                            self.HintMatrixList[i][j] = []
                            self.HintMatrixList[i][j].append(k)
                        elif k not in self.ColMaxList:
                            self.HintMatrixList[i][j] = []
                            self.HintMatrixList[i][j].append(k)
                        elif k not in self.CubMaxList:
                            self.HintMatrixList[i][j] = []
                            self.HintMatrixList[i][j].append(k)

            if dbg_on == 2:
                print(self.HintMatrixListPre)
                print(self.HintMatrixList)

            for i in range(9):
                for j in range(9):
                    if set(self.HintMatrixListPre[i][j]) > set(self.HintMatrixList[i][j]):
                        reloop = 1

        if dbg_on == 2:
            print(">>>>>>>>>> 2222222222 print length now!")
            for i in range(9):
                sys.stdout.write("|")
                for j in range(9):
                    sys.stdout.write(" %d "%(len(self.HintMatrixList[i][j])))
                sys.stdout.write("|\n")

        for i in range(9):
            for j in range(9):
                if ( len(self.HintMatrixList[i][j]) > 1):
                    return 1

        return 0


    def procMatrix(self):
        self.MatrixDisplay(1)
        self.Score=self.HintNum

        for i in range(9):
            for j in range(9):
                if (i*9+j) in self.LocInputList:
                    if self.ValInputList[self.LocInputList.index((i*9+j))]==0:
                        self.CurrMatrix[i][j] = '*'
                    else:
                        self.CurrMatrix[i][j] = str(self.ValInputList[self.LocInputList.index((i*9+j))])

        for i in range(9):
            for j in range(9):
                if (i*9+j) in self.LocInputList:
                    if int(self.CurrMatrix[i][j]) == int(self.RandMatrix[i][j]):
                        self.Score=self.Score+1

        if (self.Score==81):
            self.Done=1
            self.MatrixDisplay(2)


class Box:
    def __init__(self, topleft, text, color, textcolor, ind):
        self.topleft = topleft
        self.text = text
        self.color = color
        self.textcolor = textcolor
        self.ind = ind
    def render(self, surface):
        x, y = self.topleft
        pygame.draw.rect(surface, self.color, (x, y, box_size, box_size))
        if self.ind == 1:
            text_height  = int(box_size * 0.2)
        else:
            text_height  = int(box_size * 0.35)
        font_obj     = pygame.font.Font("FreeSansBold.ttf", text_height)
        text_surface = font_obj.render(self.text, True, self.textcolor)
        text_rect    = text_surface.get_rect()
        if self.ind == 1:
            text_rect.center = (x + box_size / 2, y + box_size / 10)
        else:
            text_rect.center = (x + box_size / 2, y + box_size / 2)
        surface.blit(text_surface, text_rect)


def draw_box(sdk):
    global board
    x, y = left_of_screen, top_of_screen
    size = box_size * 9 + box_gap * 6 + box_gap2 * 4
    pygame.draw.rect(screen, BLACK, (x, y, size, size))
    x, y = x + box_gap2, y + box_gap2
    ind=0
    for i in range(9):
        for j in range(9):
            '''
            idx=i*j
            text=str(idx)
            textcolor=BLACK
            '''
            idx = board[i][j]
            if idx == 0:
                ind=0
                text = ""
                textcolor = DARKBLUE
            elif idx > 9:
                ind=1
                text = str(idx)
                textcolor = BLACK
            elif idx == board[y_loc][x_loc]:
                ind=0
                text = str(idx)
                if check_mode > 0:
                    textcolor = RED
                else:
                    if(i*9+j) in sdk.HintList:#hint num fixed to black
                        textcolor = BLACK
                    else:
                        textcolor = DARKBLUE
            else:
                ind=0
                text = str(idx)
                if(i*9+j) in sdk.HintList:#hint num fixed to black
                    textcolor = BLACK
                else:
                    textcolor = DARKBLUE

            if(i==y_loc) and (j == x_loc):
                color = (21, 185, 145)
            elif (i==y_loc) or (j == x_loc):
                 color = (92, 237, 201)
            else:
                color =  (192, 192, 192)

            box = Box((x, y), text, color, textcolor, ind)
            box.render(screen)
            if j%3 == 2:
                x += box_size + box_gap2
            else:
                x += box_size + box_gap
        x = left_of_screen + box_gap2
        if i%3 == 2:
            y += box_size + box_gap2
        else:
            y += box_size + box_gap

def draw_title(ttype):
    global timer
    title_dict = {0:{'ttype':'text', 'tname':'SUDOKU', 'theight':40, 'tcolor': (81,205,71),        'tpos':(left_of_screen, left_of_screen//2+15)},
                  1:{'ttype':'text', 'tname':'START',  'theight':14, 'tcolor': FORESTGREEN, 'tpos':(left_of_screen+205, left_of_screen//2+5)},
                  2:{'ttype':'text', 'tname':'DONE',   'theight':14, 'tcolor': FORESTGREEN, 'tpos':(left_of_screen+275, left_of_screen//2+5)},
                  3:{'ttype':'text', 'tname':'TIMER',  'theight':14, 'tcolor': FORESTGREEN, 'tpos':(left_of_screen+355, left_of_screen//2+5)},
                  4:{'ttype':'vars', 'tname':timer,    'theight':14, 'tcolor': GOLD,        'tpos':(), 'tcenter':()},
                  5:{'ttype':'circ', 'tarea':(),       'ttext':'',   'tcolor': RED,         'tpos':(left_of_screen+200, left_of_screen//2 + 35, 60, 30), 'tcenter':(left_of_screen+230, left_of_screen//2 + 50), 'tround':15},
                  6:{'ttype':'circ', 'tarea':(),       'ttext':'',   'tcolor': GRAY,        'tpos':(left_of_screen+265, left_of_screen//2 + 35, 60, 30), 'tcenter':(left_of_screen+295, left_of_screen//2 + 50), 'tround':15},
                  7:{'ttype':'rect', 'varsnum':4, 'tarea':(), 'ttext':'', 'tcolor': FORESTGREEN, 'tpos':(left_of_screen+340, left_of_screen//2 + 35, 80, 30), 'tcenter':(left_of_screen+380, left_of_screen//2 + 50), 'tround':15}}

    for i in range(8):
        if ttype==1:#timer
            if i== 7:
                title_dict[i]['tarea'] = pygame.draw.rect(screen, title_dict[i]['tcolor'], title_dict[i]['tpos'])
                title_dict[i]['ttext'] = write(title_dict[title_dict[i]['varsnum']]['tname'], height=title_dict[title_dict[i]['varsnum']]['theight'], color=title_dict[title_dict[i]['varsnum']]['tcolor'])
                title_dict[title_dict[i]['varsnum']]['tpos'] = title_dict[i]['ttext'].get_rect()
                title_dict[title_dict[i]['varsnum']]['tpos'].center = title_dict[i]['tcenter']
                screen.blit(title_dict[i]['ttext'],title_dict[title_dict[i]['varsnum']]['tpos'])
        else:#ttype==0, draw all title

            if title_dict[i]['ttype']=='text':
                screen.blit(write(title_dict[i]['tname'], height=title_dict[i]['theight'], color=title_dict[i]['tcolor']), title_dict[i]['tpos'])
            elif title_dict[i]['ttype']=='circ':
                title_dict[i]['tarea'] = pygame.draw.circle(screen, title_dict[i]['tcolor'], title_dict[i]['tcenter'], title_dict[i]['tround'])
                #screen.blit()
            elif title_dict[i]['ttype']=='rect':
                title_dict[i]['tarea'] = pygame.draw.rect(screen, title_dict[i]['tcolor'], title_dict[i]['tpos'])
                title_dict[i]['ttext'] = write(title_dict[title_dict[i]['varsnum']]['tname'], height=title_dict[title_dict[i]['varsnum']]['theight'], color=title_dict[title_dict[i]['varsnum']]['tcolor'])
                title_dict[title_dict[i]['varsnum']]['tpos'] = title_dict[i]['ttext'].get_rect()
                title_dict[title_dict[i]['varsnum']]['tpos'].center = title_dict[i]['tcenter']
                screen.blit(title_dict[i]['ttext'],title_dict[title_dict[i]['varsnum']]['tpos'])

    screen.blit(write("Use LEFT, RIGHT, UP, DOWN", height=16, color=GRAY), (left_of_screen, screen_height - bottom_of_screen))

def draw_timer():
    pass

def init_board(sdk):
    sdk.iniMatrix()
    global board
    global x_loc,y_loc,check_mode
    check_mode=check_mode%2
    x_loc = x_loc%9
    y_loc = y_loc%9
    for i in range(9):
        for j in range(9):
            board[i][j] = sdk.HintMatrix[i][j]

def move(value):
    global x_loc
    global y_loc
    global check_mode
    print('MOVE BEFORE,x_loc is %d-----y_loc is %d'%(x_loc, y_loc))
    x_loc+=value['delta_x']
    y_loc+=value['delta_y']
    check_mode+=value['delta_chk']
    x_loc=x_loc%9
    y_loc=y_loc%9
    check_mode=check_mode%2
    print('MOVE AFTER,x_loc is %d-----y_loc is %d'%(x_loc, y_loc))

def update_value(value):
    global board
    if value==board[y_loc][x_loc]:
        board[y_loc][x_loc]=0
    else:
        board[y_loc][x_loc]=value

def guess_value(value):
    global board
    if value==board[y_loc][x_loc]:
        board[y_loc][x_loc]=0
    elif board[y_loc][x_loc]==0:
        board[y_loc][x_loc]=value
    else:
        tmp_str = str(board[y_loc][x_loc])
        tmp_str_list=[]
        for i in tmp_str:
            tmp_str_list.append(int(i))
        if tmp_str_list.count(value)==0:
            tmp_str_list.append(value)
        else:
            while(tmp_str_list.count(value) > 0):
                tmp_str_index = tmp_str_list.index(value)
                del tmp_str_list[tmp_str_index]
        tmp_str_list.sort()
        str_value=''
        for i in tmp_str_list:
            str_value='%s%d'%(str_value, i)
        board[y_loc][x_loc]=int(str_value)


def write(msg="pygame is cool", color= BLACK, height = 14):
    myfont = pygame.font.Font("FreeSansBold.ttf", height)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext

def is_over(sdk):
    global score,best
    '''if board != final matrix
    '''
    for i in range(9):
        for j in range(9):
            if board[i][j] != sdk.RandMatrix[i][j]:
                return False
    tmp_str=''
    for i in str(timer):
        if i != ':' and i != '-':
            tmp_str='%s%s'%(tmp_str, i)
    score=int(tmp_str)
    if score<best:
        best=score
    return True

def read_best():
    try:
        f = open('best.rec', 'r')
        best = int(f.read())
        f.close()
    except:
        best = 0
    return best

def write_best(best):
    try:
        f = open('best.rec', 'w')
        f.write(str(best))
        f.close()
    except IOError:
        pass

def main(sdk):
    global score
    global run
    global timer

    one_ms_cnt=0
    one_sec_cnt=0
    one_min_cnt=0
    one_hour_cnt=0
    timer='%02d:%02d:%02d'%(one_hour_cnt,one_min_cnt,one_sec_cnt)
    #timer='--:--:--'
    screen.blit(background, (0, 0))
    init_board(sdk)
    gameover = is_over(sdk)

    curr_board = deepcopy(board)
    curr_timer = deepcopy(timer)
    curr_status =(x_loc, y_loc, check_mode)

    draw_box(sdk)
    draw_title(0)
    #timer_add()

    while True:

        if one_ms_cnt<999:
            one_ms_cnt+=1
        else:
            one_ms_cnt=0

        if one_sec_cnt<59:
            if one_ms_cnt==999:
                one_sec_cnt+=1
                #print('second add %d'%one_sec_cnt)
        else:
            one_sec_cnt=0

        if one_min_cnt<59:
            if one_sec_cnt==59 and one_ms_cnt==999:
                one_min_cnt+=1
        else:
            one_min_cnt=0

        if one_hour_cnt<59:
            if one_min_cnt==59 and one_sec_cnt==59 and one_ms_cnt==999:
                one_hour_cnt+=1
        else:
            #one_hour_cnt=0
            print("time up! game over!")
            gameover=1

        timer='%02d:%02d:%02d'%(one_hour_cnt,one_min_cnt,one_sec_cnt)

        if curr_timer != timer:
            draw_title(1)
            curr_timer=deepcopy(timer)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                write_best(best)
                #run=0
                pygame.quit()
                exit()
                return 0
            elif not gameover:
                if event.type == KEYUP and event.key in move_dict:
                    move(move_dict[event.key])
                elif event.type == KEYUP and event.key in update_value_dict:
                    if (y_loc*9+x_loc) not in sdk.HintList:
                        update_value(update_value_dict[event.key])
                        print('update value')
                    else:
                        print('hint given! no change!')
                elif event.type == KEYUP and event.key in guess_value_dict:
                    if (y_loc*9+x_loc) not in sdk.HintList:
                        guess_value(guess_value_dict[event.key])
                        print('add guess value')
                    else:
                        print('hint given! no change!')
                elif event.type == KEYUP and event.key == K_DELETE:
                    if (y_loc*9+x_loc) not in sdk.HintList:
                        board[y_loc][x_loc]=0
                    else:
                        print('hint given! no change!')
                elif event.type == KEYUP and event.key == K_F2:
                    for i in range(9):
                        for j in range(9):
                            board[i][j] = sdk.RandMatrix[i][j]

                if curr_board != board or curr_status != (x_loc, y_loc, check_mode):#newx_loc != x_loc or newy_loc != y_loc or check_mode != pre_check_mode:
                    curr_board = deepcopy(board)
                    curr_status = (x_loc, y_loc, check_mode)
                    draw_box(sdk)
                gameover = is_over(sdk)
            else:
                write_best(best)

                screen.blit(write("Game Win!", height = 40, color = FORESTGREEN), (left_of_screen, screen_height // 2))
                screen.blit(write("Press C to Continue,", height = 40, color = FORESTGREEN), (left_of_screen, screen_height // 2+40))
                screen.blit(write("          Q to Quit.", height = 40, color = FORESTGREEN), (left_of_screen, screen_height // 2+80))
                if event.type == KEYUP and event.key == K_c:
                    screen.blit(write("Loading ...", height = 40, color = FORESTGREEN), (left_of_screen, screen_height // 2+120))
                    run=1
                    gameover=0
                    return 1
        pygame.display.update()

if __name__ == "__main__":
    sdk = sudoku(1)
    continue_run=1
    while continue_run:
        continue_run=main(sdk)
        if continue_run==1:
             screen.blit(write("Loading ...", height = 40, color = FORESTGREEN), (left_of_screen, screen_height // 2+120))
             pygame.display.update()