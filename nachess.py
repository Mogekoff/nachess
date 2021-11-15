from config import figures


class Figure:
    x = 0
    y = 0
    color = None
    icon = None
    field = None

    def __init__(self, x, y, color, field):
        self.x = x
        self.y = y
        self.color = color
        self.field = field

    def move(self, x, y):
        if self.can_move(x, y):
            self.field[x][y] = self
            self.field[self.x][self.y] = None
            self.x = x
            self.y = y

    def can_move(self, x, y):
        if (x < 0 or x > 7 or y < 0 or y > 7 or
                self.x == x and self.y == y or
                self.field[x][y] is not None and self.color == self.field[x][y].color):
            return False
        return True


class Field:
    field = None

    def __init__(self, field=None):
        if field is None:
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
                if self.field[j][i] is not None:
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
            self.field[i][1] = Pawn(i, 1, False, self.field)
            self.field[i][6] = Pawn(i, 6, True, self.field)
        self.field[1][0], self.field[6][0] = Knight(1, 0, False, self.field), Knight(6, 0, False, self.field)
        self.field[1][7], self.field[6][7] = Knight(1, 7, True, self.field), Knight(6, 7, True, self.field)
        self.field[0][0], self.field[7][0] = Rook(0, 0, False, self.field), Rook(7, 0, False, self.field)
        self.field[0][7], self.field[7][7] = Rook(0, 7, True, self.field), Rook(7, 7, True, self.field)


class Pawn(Figure):
    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
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
                     self.field[x][y] is not None and not self.color == self.field[x][y].color)):
                return True
        return False

    def move(self, x, y):
        if self.can_move(x, y):
            super().move(x, y)


class Knight(Figure):
    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
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


class Rook(Figure):
    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            self.icon = figures['black']['rook']
        else:
            self.icon = figures['white']['rook']

    def can_move(self, x, y):
        if super().can_move(x, y):
            inc = 1
            if self.y > y or self.x > x:
                inc = -1
            if self.x == x:
                for i in range(self.y+inc, y, inc):
                    if self.field[x][i] is not None:
                        return False
            elif self.y == y:
                for i in range(self.x + inc, x, inc):
                    if self.field[i][y] is not None:
                        return False
            else:
                return False
            return True
        return False

    def move(self, x, y):
        if self.can_move(x, y):
                super().move(x, y)


class Bishop(Figure):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if color:
            self.icon = figures['black']['bishop']
        else:
            self.icon = figures['white']['bishop']

    def can_move(self, x, y):
        if super().can_move(x, y):
            if abs(self.x - x) == abs(self.y - y):
                return True
        return False

    def move(self, x, y):
        if self.can_move(x, y):
                super().move(x, y)
