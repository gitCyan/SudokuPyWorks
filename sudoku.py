'''@author: Cyan
   @version: 1.0
   @note: Sudoku game(2014-08-07)
          test evironment: python3.4.1
'''
import sys
import random
import string
D:\Program Files\Python\Python325\
class sudoku():
    '''Sudoku main
    '''
    #init function
    def __init__(self,dbg_on):
        '''parameter initial
        '''        
        self.level = 0 #level: 2-hard:24, 1-middle:32, 0-easy:40
        self.MatrixSize = 9
        self.HintNumList = [40, 35, 30]
        #self.HintNum = 40
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

    #####other utils functions###
    def GetCurrMatrix(self, num):
        for i in range(9):
            for j in range(9):
                if i*9+j == num:
                    return self.currMatrix[i][j]
        
        return 'null'

        
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
        self.MatrixDisplay(0)
        print(self.level)
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
                    

    def MatrixDisplay(self, num):
        if num == 0: #game initial pre
            print(">>>>>>>>>> Start Now!")
            print(">>>>>>>>>> Choose Game Level, 0 for easy, 1 for average, 2 for hard")
            self.level=self.GetInputVal('level', 0, 2)
        elif num == 1: #game initial post
            print(">>>>>>>>>> Sudoku  Begin <<<<<<<<<<")
            print("     1  2  3   4  5  6   7  8  9")
            print("   -------------------------------")
            for i in range(9):
                sys.stdout.write(' %d |'%(i+1))
                for j in range(9):
                    sys.stdout.write(' %s '%self.CurrMatrix[i][j])
                    if (int(j%3)==2):
                        sys.stdout.write('|')
                sys.stdout.write('\n')
                if(int(i%3)==2):
                    print("   -------------------------------")
            print(">>>>>>>>>> Sudoku    End <<<<<<<<<<")
            print(">>>>>>>>>> current score is %d"%self.Score)
            print(">>>>>>>>>> Choose input location:")
            get_input_ing=1
            while(get_input_ing):
                tmp1=self.GetInputVal('ROW',1,9)-1
                tmp2=self.GetInputVal('COLUMN',1,9)-1
                if(tmp1*9+tmp2) in self.HintList:
                    get_input_ing=1
                    print(">>>>>>>>>> Wrong location! Crash on the Hint number. Please enter again.")
                else:
                    tmp3=self.GetInputVal('number',0,9)
                    if (tmp1*9+tmp2) not in self.LocInputList:
                        get_input_ing=0
                        self.LocInputList.append((tmp1*9+tmp2))
                        self.ValInputList.append(tmp3)
                    else:
                        if self.ValInputList[self.LocInputList.index((tmp1*9+tmp2))]==tmp3:
                            get_input_ing=1
                            print(">>>>>>>>>> Input same value as before. Please enter again.")
                        else:
                            get_input_ing=0
                            self.ValInputList[self.LocInputList.index((tmp1*9+tmp2))]=tmp3
        elif num == 2: #done!
            print(">>>>>>>>>> Game Win!")
            print(">>>>>>>>>> Sudoku  Begin <<<<<<<<<<")
            print("     1  2  3   4  5  6   7  8  9")
            print("   -------------------------------")
            for i in range(9):
                sys.stdout.write(' %d |'%(i+1))
                for j in range(9):
                    sys.stdout.write(' %s '%self.CurrMatrix[i][j])
                    if (int(j%3)==2):
                        sys.stdout.write('|')
                sys.stdout.write('\n')
                if(int(i%3)==2):
                    print("   -------------------------------")
            print(">>>>>>>>>> Sudoku    End <<<<<<<<<<")


    def play(self):
        self.iniMatrix()
        while(self.Done == 0):
            self.procMatrix()


if __name__ == 'sdktest':
    '''self test
    '''
    dbg_on = 0
    sdk = sudoku(dbg_on)
    work = 1
    while(work):
        sdk.play()
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Press \'q\' to quit, other key to start a new game')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        inputVal=input()
        if(inputVal=='q'):
            work=0
        else:
           print('>>>>>>>>>> TO BE CONTINUE ...')
           print('...')