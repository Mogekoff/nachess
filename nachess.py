from config import figures


class Figure:  # базовый класс "фигура"
    x = 0
    y = 0
    color = None  # цвет фигуры
    icon = None  # икнока фигуры
    field = None  # ссылка на игровое поле

    def __init__(self, x, y, color, field):  # конструктор
        self.x = x
        self.y = y
        self.color = color
        self.field = field

    def can_move(self, x, y):  # функция проверки возможности хода
        if (x < 0 or x > 7 or y < 0 or y > 7 or  # выход за края доски
                self.x == x and self.y == y or  # ход на клетку, на которой стоит ходящая фигура
                self.field[x][y] is not None and self.color == self.field[x][y].color):  # ход на свою фигуру
            return False
        return True


class Field:  # класс игрового поля
    field = None
    moves = []

    def __init__(self, field=None, moves=None):  # конструктор принимает массив игрового поля
        if field is None:  # если массив не предоставлен
            self.field = [0] * 8  # создаем двумерный массив
            for i in range(7, -1, -1):  # 8х8 ячеек
                self.field[i] = [0] * 8  #
                for j in range(8):  #
                    self.field[i][j] = None  # и заполняем его 'None'
            self.draw_classic()
        else:
            self.field = field
        if moves is not None:
            for i in range(len(moves)):
                self.move(moves[i][0], moves[i][1], moves[i][2], moves[i][3])
            self.moves = moves

    def print(self):  # функция вывода игрового поля
        cell = False  # итератор для чередования цвета клеток поля
        for i in range(7, -1, -1):
            # print(i + 1, end=' ')
            print(i, end=' ')  # выводит номер клетки
            for j in range(8):
                if self.field[j][i] is not None:  # если на клетке есть фигура
                    print(self.field[j][i].icon, end=' ')  # вывести икноку фигуры
                elif cell:  # если фигуры нет и клетка черная (True)
                    print(figures['black']['cell'], end=' ')  # вывести символ из массива figures из config.py
                else:
                    print(figures['white']['cell'], end=' ')
                cell = not cell  # чередовать цвет клетки
            cell = not cell  # повтор цвета в конце строки
            print()
        print('  ' + figures['coordinates'])  # вывод нижних координат

    def move(self, from_x, from_y, to_x, to_y):  # функция, делающая ходы на доске
        if self.field[from_x][from_y] is not None and self.field[from_x][from_y].can_move(to_x, to_y):
            self.field[to_x][to_y] = self.field[from_x][from_y]  # если да, ходим
            self.field[from_x][from_y] = None  # удаляем фигуру из прошлой клетки
            self.field[to_x][to_y].x = to_x  # меняем координаты фигуры
            self.field[to_x][to_y].y = to_y  # на новые
            self.moves.append((from_x, from_y, to_x, to_y))  # сохраняем ход
            return True
        return False

    def draw_classic(self):  # устанавливает фигуры в стандартное шахматное расположение
        for i in range(8):
            self.field[i][1] = Pawn(i, 1, False, self.field)    # пешки белых
            self.field[i][6] = Pawn(i, 6, True, self.field)     # пешки черных
        self.field[1][0], self.field[6][0] = Knight(1, 0, False, self.field), Knight(6, 0, False, self.field)  # кони
        self.field[1][7], self.field[6][7] = Knight(1, 7, True, self.field), Knight(6, 7, True, self.field)    #
        self.field[0][0], self.field[7][0] = Rook(0, 0, False, self.field), Rook(7, 0, False, self.field)      # ладьи
        self.field[0][7], self.field[7][7] = Rook(0, 7, True, self.field), Rook(7, 7, True, self.field)        #
        self.field[2][0], self.field[5][0] = Bishop(2, 0, False, self.field), Bishop(5, 0, False, self.field)  # слоны
        self.field[2][7], self.field[5][7] = Bishop(2, 7, True, self.field), Bishop(5, 7, True, self.field)    #
        self.field[3][0], self.field[3][7] = Queen(3, 0, False, self.field), Queen(3, 7, True, self.field)
        self.field[4][0], self.field[4][7] = King(4, 0, False, self.field), King(4, 7, True, self.field)


class Pawn(Figure):  # класс пешки
    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            self.icon = figures['black']['pawn']
        else:
            self.icon = figures['white']['pawn']

    def can_move(self, x, y):
        if super().can_move(x, y):  # вызов базовой проверки хода родительского класса "фигура"
            if ((self.x == x and  # ход пешки вперед на 1 или 2 клетки...
                 (not self.color and (self.y - y == -2 or self.y - y == -1)) or  # для белой пешки
                 (self.color and (self.y - y == 2 or self.y - y == 1))) or  # для черной пешки
                    ((self.x - 1 == x or self.x - 1) and  # ход вбок при рубке
                     self.field[x][y] is not None and not self.color == self.field[x][y].color)):  # только при рубке
                return True
        return False


class Knight(Figure):  # класс фигуры "конь"
    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            self.icon = figures['black']['knight']
        else:
            self.icon = figures['white']['knight']

    def can_move(self, x, y):
        if super().can_move(x, y):
            if (self.x - x) ** 2 + (self.y - y) ** 2 == 5:
                return True
        return False


class Rook(Figure):  # класс ладьи
    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            self.icon = figures['black']['rook']
        else:
            self.icon = figures['white']['rook']

    def can_move(self, x, y):
        if super().can_move(x, y):
            inc = 1  # инкремент, решающий куда двигаться, вперед или назад
            if self.y > y or self.x > x:  #
                inc = -1  #
            if self.x == x:  # если двигаемся по вертикали
                for i in range(self.y + inc, y, inc):  # проверка на препятствия по пути
                    if self.field[x][i] is not None:  #
                        return False
            elif self.y == y:  # если ходим по горизонтали
                for i in range(self.x + inc, x, inc):
                    if self.field[i][y] is not None:
                        return False  # если встретили препятствие по пути
            else:
                return False  # если ходим не по горизонтали и не вертикали
            return True  # если прошли прошлые две проверки
        return False  # если не прошли базовую проверку


class Bishop(Figure):  # класс слона
    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            self.icon = figures['black']['bishop']
        else:
            self.icon = figures['white']['bishop']

    def can_move(self, x, y):
        if super().can_move(x, y):
            if abs(self.x - x) == abs(self.y - y):  # проверка на возможность хода на эту клетку
                return True
        return False


class Queen(Bishop, Rook):  # класс фигуры "ферзь", наследуется от слона и ладьи
    def __init__(self, x, y, color, field):
        Figure.__init__(self, x, y, color, field)
        if color:
            self.icon = figures['black']['queen']
        else:
            self.icon = figures['white']['queen']

    def can_move(self, x, y):
        if Bishop.can_move(self, x, y) or Rook.can_move(self, x, y):
            return True
        return False


class King(Figure):  # класс фигуры "конь"
    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            self.icon = figures['black']['king']
        else:
            self.icon = figures['white']['king']

    def can_move(self, x, y):
        if super().can_move(x, y):
            if (-1 <= self.x - x <= 1) and (-1 <= self.y - y <= 1):
                return True
        return False
