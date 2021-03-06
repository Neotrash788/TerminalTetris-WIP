import pygame
import time
import random
from colorama import Fore
FPS = 30

lib = {
    0: (Fore.WHITE,'\u25A1'),
    1: '\u25A7',
    'shadow': (Fore.WHITE,'\u25A6'),
    3: '\u25A9',
    4: (Fore.RED,'\u25A0'),
    'Colz':(Fore.RED,'\u25A0'),
    'Cols':(Fore.GREEN,'\u25A0'),
    'Colt':(Fore.MAGENTA,'\u25A0'),
    'Colo':(Fore.YELLOW,'\u25A0'),
    'Coll':(Fore.WHITE,'\u25A0'),
    'Colj':(Fore.BLUE,'\u25A0'),
    'Coli':(Fore.CYAN,'\u25A0'),
    't': ['r', 'l', 'l', 'r', 'u'],
    'z': ['r', 'l', 'u', 'l'],
    's': ['l', 'r', 'u', 'r'],
    'o': ['u', 'r', 'd'],
    'i': ['l', 'r', 'r', 'r'],
    'l': ['l', 'r', 'r', 'u', ],
    'j': ['r', 'l', 'l', 'u', ],
    'U': 'r',
    'D': 'l',
    'L': 'u',
    'R': 'd',
    'cu': 'l',
    'cd': 'r',
    'cl': 'd',
    'cr': 'u',
    'mu': 'd',
    'md': 'u',
    'ml': 'r',
    'mr': 'l',
    '1': 'SINGLE',
    '2': 'DOUBBLE',
    '3': 'TRIPPLE',
    '4': 'TETRIS',
}

srsLib = {
    # XY
    'UU1': [0, 0],
    'UU2': [-1, 0],
    'UU3': [-1, 1],
    'UU4': [0, -2],
    'UU5': [-1, -2],
    'UR1': [0, 0],
    'UR2': [0, 0],
    'UR3': [1, -1],
    'UR4': [0, 2],
    'UR5': [1, 2],
    'UD1': [0, 0],
    'UD2': [1, 0],
    'UD3': [1, 1],
    'UD4': [0, -2],
    'UD5': [1, -2],
    'UL1': [0, 0],
    'UL2': [0, 0],
    'UL3': [-1, -1],
    'UL4': [0, 2],
    'UL5': [-1, 2],
    'ZU1': [0, 0],
    'ZU2': [1, 0],
    'ZU3': [1, 1],
    'ZU4': [0, -1],
    'ZU5': [1, -2],
    'ZR1': [0, 0],
    'ZR2': [0, 0],
    'ZR3': [1, -1],
    'ZR4': [0, 2],
    'ZR5': [1, 2],
    'ZD1': [0, 0],
    'ZD2': [-1, 0],
    'ZD3': [-1, 1],
    'ZD4': [0, -1],
    'ZD5': [-1, -2],
    'ZL1': [0, 0],
    'ZL2': [-1, 0],
    'ZL3': [-1, -1],
    'ZL4': [0, 2],
    'ZL5': [-1, 2]
}


iSpecials = {
    # xy
    'u': [0, 0],
    'r': [1, 0],
    'd': [1, -1],
    'l': [0, -1]
}

vh = 23
vw = 10
prevShape = []
prevOffset = [0, 0]


class Logic():
    def __init__(self):
        self.minos = ['z', 's', 'j', 'l', 't', 'o', 'i']
        self.bag = []
        for i in range(3):
            random.shuffle(self.minos)
            self.bag.append(''.join(self.minos))
            print(self.minos)
        random.shuffle(self.minos)

        self.bagPos = 0
        self.heldPiece = None
        self.groundTime = 0
        self.prevShadow = []
        self.heldGrid = [[lib[0] for i in range(4)]for i in range(4)]

    def xyToyx(self, pos):
        return [pos[1], pos[0]]

    def shapeToCords(self, origin, shape, ofset=(0, 0),rotate = False):
        global currentShape
        # xy
        origin = [origin[0] + ofset[0], origin[1] + ofset[1]]
        origin = tuple(origin)

        try:
            if currentShape.shapeId == 'i':
                if rotate == False:
                    origin = [origin[0] + iSpecials[currentShape.rotation][0],origin[1] + iSpecials[currentShape.rotation][1]]
                else:
                    if rotate == 'u':
                        rot = lib[currentShape.rotation.upper()]
                    if rotate == 'z':
                        rot = lib[f'c{currentShape.rotation}']
                    if rotate == 'a':
                        rot = lib[f'm{currentShape.rotation}']
                    origin = [origin[0] + iSpecials[rot][0],origin[1] + iSpecials[rot][1]]
        except NameError:
            pass

        cord = origin
        cords = [cord]

        for i in shape:
            if i == 'r':
                cord = (cord[0] + 1, cord[1])
            if i == 'l':
                cord = (cord[0] - 1, cord[1])
            if i == 'u':
                cord = (cord[0], cord[1]+1)
            if i == 'd':
                cord = (cord[0], cord[1]-1)
            cords.append(cord)
        cords = [list(i) for i in cords]
        return cords

    def onGround(self, cords):
        cords = [self.xyToyx(i) for i in cords]
        # below here cords is y,x
        for i in cords:
            if i[0] == 0:
                return True

        newCords = [[i[0]-1, i[1]] for i in cords]

        for i in range(len(newCords)-1, -1, -1):
            if newCords[i] in cords:
                newCords.pop(i)

        for i in newCords:
            if board.board[i[0]][i[1]] != lib[0] and board.board[i[0]][i[1]] != lib['shadow']:
                return True
        else:
            return False

    def validRotation(self, origin, shape, Dir, offset=(0, 0)):
        if Dir == 'z':
            shape = [lib[f'c{i}'] for i in shape]
        if Dir == 'u':
            shape = [lib[i.upper()] for i in shape]
        if Dir == 'a':
            shape = [lib[f'm{i}'] for i in shape]

        origin = [origin[0]+offset[0], origin[1]+offset[1]]
        cords = self.shapeToCords(origin, shape,(0,0),Dir)

        for i in range(len(cords)-1, -1, -1):
            if cords[i] in currentShape.cords:
                cords.pop(i)

        cords = [logic.xyToyx(i) for i in cords]

        try:
            for i in cords:
                if logic.touchingPiece(i) or i[0] <= -1:
                    return False
            else:
                return True
        except IndexError:
            return False

    def canMove(self, dir):
        if dir == 'r':
            cords = [[currentShape.cords[i][0]+1, currentShape.cords[i][1]]
                     for i in range(len(currentShape.cords))]
        if dir == 'l':
            cords = [[currentShape.cords[i][0]-1, currentShape.cords[i][1]]
                     for i in range(len(currentShape.cords))]

        for i in range(len(cords)-1, -1, -1):
            if cords[i] in currentShape.cords:
                cords.pop(i)

        cords = [logic.xyToyx(i) for i in cords]

        for i in cords:
            if i[1] < 0 or i[1] > vw - 1 or logic.touchingPiece(i):
                print('INVALID MOVEMENT')
                return False
        else:
            return True

    def lineClears(self):
        clearLines = []
        for i in range(len(board.board)):
            if not lib[0] in board.board[i]:
                clearLines.append(i)
        return clearLines if not clearLines == [] else False

    def newShape(self):
        global currentShape,pieceQue
        currentShape = shape([4, 21], self.bag[0][self.bagPos])
        self.bagPos += 1
        if self.bagPos == 7:
            self.bag.pop(0)
            random.shuffle(self.minos)
            self.bag.append(''.join(self.minos))
            self.bagPos = 0
        pieceQue = logic.nextQue()

    def topedOut(self):
        return True if self.onGround(currentShape.cords) else False

    def srs(self, origin, shape, Dir):
        if Dir == 'a':
            if self.validRotation(origin, shape, 'a'):
                currentShape.rotate('a', [0, 0])
                return True
            else:
                return False

        for i in range(1, 6):
            if self.validRotation(origin, shape, Dir, srsLib[f'{Dir.upper()}{currentShape.rotation.upper()}{i}']):
                ofset = srsLib[f'{Dir.upper()}{currentShape.rotation.upper()}{i}']
                currentShape.rotate(Dir, ofset)
                if ofset != [0, 0]:
                    self.spin = True
                return True
        else:
            return False

    def hold(self):
        global currentShape
        if self.heldPiece == None:
            self.heldPiece = currentShape.shapeId
            self.newShape()
        else:
            currentShape, self.heldPiece = shape(
                [4, 21], self.heldPiece), currentShape.shapeId

        currentShape.printShape(4)
        board.printGrid()

    def shapeDisplay(self, shape):
        self.resetHoldDisplay()
        cords = self.shapeToCords([1, 0], lib[shape]) if shape != None else []
        cords = [self.xyToyx(cord) for cord in cords]

        for cord in cords:
            self.heldGrid[cord[0]][cord[1]] = lib[f'Col{shape}']    
        return [cord for cord in self.heldGrid[::-1]]

    def resetHoldDisplay(self):
        self.heldGrid = [[lib[0] for i in range(4)]for i in range(4)]

    def nextQue(self):
        que = []
        for i in range(5):
            if self.bagPos+i < 6:
                for row in self.shapeDisplay(self.bag[0][self.bagPos+i]):
                    que.append([row[-1], row[0:3]])
            else:
                for row in self.shapeDisplay(self.bag[1][self.bagPos+i-6]):
                    que.append([row[-1], row[0:3]])
        return que

    def isTspin(self, cords):
        higestH = 0
        highestC = []
        for cord in cords:
            # yx
            if cord[0] > higestH:
                higestH = cord[0]
        for cord in cords:
            if cord[0] >= higestH:
                highestC.append(cord)

        if len(highestC) < 2:
            if board.board[highestC[0][0]][highestC[0][1]+1] != lib[0] and board.board[highestC[0][0]][highestC[0][1]+1] != lib['shadow'] or board.board[highestC[0][0]][highestC[0][1]-1] != lib[0] and board.board[highestC[0][0]][highestC[0][1]-1] != lib['shadow']:#CHECK#CHECK
                return True
        else:
            for cord in highestC:
                if board.board[cord[0]+1][cord[1]] != lib[0] and board.board[cord[0]+1][cord[1]] != lib['shadow']:
                    return True

        return False

    def handleSpin(self):
        pass

    def grav(self):
        global prevShape
        checkTop = False
        move = True
        if logic.onGround(currentShape.cords):
            self.groundTime += 1
            if self.groundTime == 2:
                prevShape = []
                board.printGrid()
                lineCs = logic.lineClears()
                if lineCs != False:
                    if currentShape.shapeId == 't' and self.isTspin(currentShape.cords):
                        self.spin = 2
                    board.removeLines(lineCs)
                logic.newShape()
                checkTop = True
                self.groundTime = 0
            move = False

        if move:
            currentShape.origin = [
                currentShape.origin[0], currentShape.origin[1] - 1]
            currentShape.cords = logic.shapeToCords(
                currentShape.origin, currentShape.shape)
        currentShape.printShape(4)
        self.handleSpin()

        board.printGrid()

        if logic.topedOut() and checkTop:
            print('Topped Out')
            exit()
        checkTop = False
    
    def touchingPiece(self,i):
        #CHECK
        if board.board[i[0]][i[1]] != lib[0] and board.board[i[0]][i[1]] != lib['shadow']:
            return True

    def displayShadow(self):
        for i in self.prevShadow:
            i = logic.xyToyx(i)
            if board.board[i[0]][i[1]] == lib['shadow']:
                board.board[i[0]][i[1]] = lib[0]

        id = currentShape.shapeId
        origin = currentShape.origin
        cords = currentShape.cords

        while not self.onGround(cords):
            origin = [origin[0], origin[1] - 1]
            cords = logic.shapeToCords(origin, currentShape.shape)
        for i in cords:
            i = logic.xyToyx(i)
            print(i)
            if board.board[i[0]][i[1]] == lib[0]:
                board.board[i[0]][i[1]] = lib['shadow']
        self.prevShadow = cords

logic = Logic()


class Board():

    def fill(self, col):
        [self.board.append([lib[col] for i in range(0, vw)])
         for ii in range(0, vh)]

    def __init__(self):
        self.board = []
        self.fill(0)

    def setblock(self, pos, id):
        pos = logic.xyToyx(pos)
        if id != 0:
            self.board[pos[0]][pos[1]] = lib[f'Col{id}']
        else:
            self.board[pos[0]][pos[1]] = lib[0]

    def removePrevShape(self, prevShape):
        if len(prevShape) > 0:
            prevShape = prevShape[0]
        [self.setblock(i, 0) for i in prevShape]

    def removeLines(self, lines):
        clearType = lib[str(len(lines))]
        print(clearType)
        for i in lines:
            self.board[i] = [lib[0] for ii in range(vw)]

        i = 0
        while i < len(self.board)-1:
            if self.board[i+1] != [lib[0] for ii in range(vw)] and self.board[i] == [lib[0] for ii in range(vw)]:
                self.board[i+1], self.board[i] = self.board[i], self.board[i+1]
                while self.board[i-1] == [lib[0] for ii in range(vw)] and i > 0:
                    i -= 1
                    self.board[i+1], self.board[i] = self.board[i], self.board[i+1]
            i += 1

        count = 0
        for ii in self.board:
            for i in ii:
                if i == lib[0]:
                    count += 1

        if count == vw*vh:
            print('ALL CLEAR')

    def printGrid(self):
        global pieceQue
        print(f"Current shape's orentation ->{currentShape.rotation}")
        print('--------------------------')
        print(f'BAG POS ->{logic.bagPos}')
        print(f'CURRENT BAG->{logic.bag}')

        logic.displayShadow() # CHECK

        held = [i for i in logic.shapeDisplay(logic.heldPiece)]
        currentBoard = [i for i in self.board[::-1]]
        length = len(pieceQue ) if len(pieceQue) > len(
            currentBoard) else len(currentBoard)

        while len(held) != length:
            held.append([lib[0] for i in range(4)])

        while len(currentBoard) != length:
            currentBoard.append([lib[0] for i in range(10)])

        while len(pieceQue) != length:
            pieceQue.append([lib[0] for i in range(4)])

        for i in range(length):
            bRow = ''
            for ii in currentBoard[i]:
                bRow += ii[0]+ii[1] + ' '
            hRow = ''
            for iii in held[i]:
                hRow += iii[0]+iii[1] + ' '
            pRow = ''
            pRow += pieceQue[i][0][0] + pieceQue[i][0][1] + ' '
            for iiii in pieceQue[i][1]:
                try:
                    pRow += iiii[0]+iiii[1] + ' '
                except IndexError:
                    pRow += '\u25A1'
                    for i in range(0,3): pRow += '\u25A1' + ' '

            print(hRow + Fore.WHITE + '||' + bRow + Fore.WHITE + '||' + pRow + Fore.WHITE)

class shape():
    global prevOffset

    def __init__(self, origin, shape):
        self.shapeId = shape
        self.origin = origin
        self.shape = lib[shape]
        self.rotation = 'u'
        self.cords = logic.shapeToCords(self.origin, self.shape)

    def rotate(self, dir, ofset=[0, 0]):
        if self.shapeId == 'o':
            return None

        if dir == 'a':
            self.shape = [lib[f'm{i}'] for i in self.shape]
            self.rotation = lib[f'm{self.rotation}']

        if dir == 'z':
            self.shape = [lib[f'c{i}'] for i in self.shape]
            self.rotation = lib[f'c{self.rotation}']

        if dir == 'u':
            self.shape = [lib[f'{i.upper()}'] for i in self.shape]
            self.rotation = lib[self.rotation.upper()]

        self.origin = [self.origin[0]+ofset[0], self.origin[1]+ofset[1]]

        self.cords = logic.shapeToCords(self.origin, self.shape)
        self.printShape(4)

    def moveUntillGround(self):
        while not logic.onGround(self.cords):
            currentShape.origin = [currentShape.origin[0], currentShape.origin[1] - 1]
            currentShape.cords = logic.shapeToCords(currentShape.origin, currentShape.shape)

    def softDrop(self):
        self.moveUntillGround()
        self.printShape(4)
        board.printGrid()

    def hardDrop(self):
        global prevShape
        self.moveUntillGround()
        board.removePrevShape(prevShape)
        self.printShape(4)
        prevShape = []
        lineCs = logic.lineClears()
        if lineCs != False:
            board.removeLines(lineCs)
        logic.newShape()
        board.printGrid()
        if logic.topedOut():
            print('Topped Out')
            exit()

    def printShape(self, id):
        global prevShape
        # board.removePrevShape(prevShape)
        board.removePrevShape(prevShape)
        [board.setblock(i, self.shapeId) for i in self.cords]
        prevShape = [self.cords]


board = Board()
logic.newShape()
pygame.init()
pygame.display.set_mode(size=(10, 10))


def main():
    frame = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_DOWN:
                    currentShape.softDrop()

                elif event.key == pygame.K_UP:
                    logic.srs(currentShape.origin, currentShape.shape, 'u')
                    board.printGrid()

                elif event.key == pygame.K_z:
                    logic.srs(currentShape.origin, currentShape.shape, 'z')
                    board.printGrid()

                elif event.key == pygame.K_a:
                    logic.srs(currentShape.origin, currentShape.shape, 'a')
                    board.printGrid()

                elif event.key == pygame.K_RIGHT:
                    if logic.canMove('r'):
                        currentShape.origin = [
                            currentShape.origin[0]+1, currentShape.origin[1]]

                    currentShape.cords = logic.shapeToCords(
                        currentShape.origin, currentShape.shape)
                    currentShape.printShape(4)

                    board.printGrid()

                elif event.key == pygame.K_LEFT:
                    if logic.canMove('l'):
                        currentShape.origin = [
                            currentShape.origin[0]-1, currentShape.origin[1]]

                    currentShape.cords = logic.shapeToCords(
                        currentShape.origin, currentShape.shape)
                    currentShape.printShape(4)

                    board.printGrid()

                elif event.key == pygame.K_c:
                    logic.hold()
                    board.printGrid()

                elif event.key == pygame.K_SPACE:
                    currentShape.hardDrop()

                else:
                    frame += 1
                    if frame > 30:
                        logic.grav()
                        frame = 0
        else:
            frame += 1
            if frame > 30:
                logic.grav()
                frame = 0
        time.sleep(1/FPS)


if __name__ == '__main__':
    main()
