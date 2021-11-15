from config import figures

field = None


class Figure:
    x = 0
    y = 0
    color = None
    icon = None

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, x, y):
        if self.can_move(x, y):
            field.field[x][y] = self
            field.field[self.x][self.y] = None
            self.x = x
            self.y = y

    def can_move(self, x, y):
        if (x < 0 or x > 7 or y < 0 or y > 7 or
                self.x == x and self.y == y or
                field.field[x][y] is not None and self.color == field.field[x][y].color):
            return False
        return True


class Field:
    field = None

    def __init__(self, field=None):
        if field == None:
            self.field = [0] * 8
            for i in range(7, -1, -1):
                self.field[i] = [0] * 8
                for j in range(8):
                    self.field[i][j] = None
        else:
            self.field = field

    def print(self):
        cell = False
        for i in range(7, -1, -1):
            #print(i + 1, end=' ')
            print(i, end=' ')
            for j in range(8):
                if self.field[j][i] != None:
                    print(self.field[j][i].icon, end=' ')
                elif cell:
                    print(figures['black']['cell'], end=' ')
                else:
                    print(figures['white']['cell'], end=' ')
                cell = not cell
            cell = not cell
            print()
        #print('  A B C D E F G H')
        print('  0 1 2 3 4 5 6 7')

    def draw_classic(self):
        for i in range(8):
            self.field[i][1] = Pawn(i, 1, False)
            self.field[i][6] = Pawn(i, 6, True)
        self.field[1][0], self.field[6][0] = Knight(1, 0, False), Knight(6, 0, False)
        self.field[1][7], self.field[6][7] = Knight(1, 7, True), Knight(6, 7, True)


field = Field()


class Pawn(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if color:
            self.icon = figures['black']['pawn']
        else:
            self.icon = figures['white']['pawn']

    def can_move(self, x, y):
        if super().can_move(x, y):
            if ((self.x == x and
                 (not self.color and (self.y - y == -2 or self.y - y == -1)) or
                 (self.color and (self.y - y == 2 or self.y - y == 1))) or
                    ((self.x - 1 == x or self.x - 1) and
                     field.field[x][y] is not None and not self.color == field.field[x][y].color)):
                return True
        return False

    def move(self, x, y):
        if self.can_move(x, y):
            super().move(x, y)


class Knight(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if color:
            self.icon = figures['black']['knight']
        else:
            self.icon = figures['white']['knight']

    def can_move(self, x, y):
        if super().can_move(x, y):
            if (self.x - 1 == x and self.y - 2 == y or
                    self.x - 2 == x and self.y - 1 == y or
                    self.x - 2 == x and self.y + 1 == y or
                    self.x - 1 == x and self.y + 2 == y or
                    self.x + 2 == x and self.y + 1 == y or
                    self.x + 1 == x and self.y + 2 == y or
                    self.x + 2 == x and self.y - 1 == y or
                    self.x + 1 == x and self.y - 2 == y):
                return True
        return False

    def move(self, x, y):
        if self.can_move(x, y):
                super().move(x, y)





field.draw_classic()
field.field[1][1].move(1, 2)
field.field[2][1].move(2, 3)
field.field[3][1].move(3, 4)
field.field[4][1].move(4, 1)
field.field[4][1].move(5, 0)

field.field[1][7].move(0, 7)
field.field[1][7].move(0, 6)
field.field[1][7].move(0, 5)
field.print()
