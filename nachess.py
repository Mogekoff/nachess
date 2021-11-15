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
            print(i + 1, end=' ')
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
        print('  A B C D E F G H')


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
                self.move(x, y)


for i in range(8):
    field.field[i][1] = Pawn(i, 1, False)
for i in range(8):
    field.field[i][6] = Pawn(i, 6, True)

field.field[1][1].move(1, 2)
field.field[2][1].move(2, 3)
field.field[3][1].move(3, 4)
field.field[4][1].move(4, 1)
field.field[4][1].move(5, 0)
field.print()
