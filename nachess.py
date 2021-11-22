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
    king_white = None
    king_black = None
    figures = [[], []]

    def __init__(self, field=None, moves=None):  # конструктор принимает массив игрового поля
        if field is None:  # если массив не предоставлен
            self.field = [0] * 8  # создаем двумерный массив
            for i in range(7, -1, -1):  # 8х8 ячеек
                self.field[i] = [0] * 8  #
                for j in range(8):  #
                    self.field[i][j] = None  # и заполняем его 'None'
            self.draw_classic()
            self.king_white = self.field[4][0]
            self.king_black = self.field[4][7]
        else:
            self.field = field
        if moves is not None:
            print(range(len(moves)))
            for i in range(len(moves)):
                self.move(moves[i][0], moves[i][1], moves[i][2], moves[i][3])
        for i in range(8):
            for j in range(8):
                figure = self.field[i][j]
                if not (figure is None):
                    if figure.color:
                        self.figures[1].append(figure)
                    else:
                        self.figures[0].append(figure)
                if figure is King:
                    if figure.color:
                        self.king_white = figure
                    else:
                        self.king_black = figure

    def print(self, x=None, y=None):  # функция вывода игрового поля
        cell = False  # итератор для чередования цвета клеток поля
        for i in range(7, -1, -1):
            # print(i + 1, end=' ')
            print(i, end=' ')  # выводит номер клетки
            for j in range(8):
                if (x is not None and y is not None and self.field[x][y] is not None and
                    (((self.field[x][y].can_move(j, i) or self.el_passant(x, y, j, i)) and
                        not self.check_check(x, y, j, i, self.field[x][y].color)) or
                        self.castling(x, y, j, i))):
                    add_color = '\033[32m'
                else:
                    add_color = ''
                if self.field[j][i] is not None:  # если на клетке есть фигура
                    if isinstance(self.field[j][i], King) and self.field[j][i].check:
                        add_color = '\033[31m' + add_color
                    print(add_color + self.field[j][i].icon, end='')  # вывести икноку фигуры
                elif cell:  # если фигуры нет и клетка черная (True)
                    print(add_color + figures['black']['cell'],
                          end='')  # вывести символ из массива figures из config.py
                else:
                    print(add_color + figures['white']['cell'], end='')
                cell = not cell  # чередовать цвет клетки
                print('\033[0m', end=' ')
            cell = not cell  # повтор цвета в конце строки
            print()
        print('  ' + figures['coordinates'])  # вывод нижних координат

    def move(self, from_x, from_y, to_x, to_y):  # функция, делающая ходы на доске
        need_to_move = False
        if self.field[from_x][from_y] is None:
            return False
        if self.field[from_x][from_y].can_move(to_x, to_y):
            need_to_move = True
            if (isinstance(self.field[from_x][from_y], King) or isinstance(self.field[from_x][from_y], Rook) and
                    self.field[from_x][from_y].first_move):
                        self.moves.append((from_x, from_y, to_x, to_y, self.field[to_x][to_y], True))
            else:
                self.moves.append((from_x, from_y, to_x, to_y, self.field[to_x][to_y]))  # сохраняем ход
        elif self.el_passant(from_x, from_y, to_x, to_y):
            need_to_move = True
            bad_pawn = self.field[self.moves[-1][2]][self.moves[-1][3]]
            self.moves.append((bad_pawn.x, bad_pawn.y, bad_pawn.x, bad_pawn.y, bad_pawn))  # запись рубки на прох.
            self.moves.append((from_x, from_y, to_x, to_y, None))
            self.field[bad_pawn.x][bad_pawn.y] = None
        elif self.castling(from_x, from_y, to_x, to_y):
            need_to_move = True
            rook = None
            inc = (to_x - from_x) // 2
            if inc == -1:
                rook = self.field[0][from_y]
            elif inc == 1:
                rook = self.field[7][from_y]
            self.moves.append((from_x, from_y, to_x, to_y, None))
            self.move(rook.x, rook.y, self.field[from_x][from_y].x + inc, rook.y)
        if need_to_move:
            if self.field[to_x][to_y] is not None and self.figures != [[], []]:
                self.figures[int(self.field[to_x][to_y].color)].remove(self.field[to_x][to_y])
            self.field[to_x][to_y] = self.field[from_x][from_y]
            self.field[from_x][from_y] = None
            self.field[to_x][to_y].x = to_x  # меняем координаты фигуры
            self.field[to_x][to_y].y = to_y  # на новые
            return True
        return False

    def go(self, from_x, from_y, to_x, to_y):
        if self.move(from_x, from_y, to_x, to_y):
            if self.check(not self.field[to_x][to_y].color, True):
                self.backtrack()
                return False
            else:
                if self.field[to_x][to_y].color:
                    if self.king_black is not None:
                        self.king_black.check = False
                else:
                    if self.king_white is not None:
                        self.king_white.check = False
                if self.check(self.field[to_x][to_y].color, False):
                    self.checkmate(self.field[to_x][to_y].color)
        if isinstance(self.field[to_x][to_y], King) or isinstance(self.field[to_x][to_y], Rook):
            self.field[to_x][to_y].first_move = False
        return True

    def el_passant(self, from_x, from_y, to_x, to_y):
        if len(self.moves) <= 0:
            return False
        last_move = self.moves[-1]
        bad_pawn = self.field[last_move[2]][last_move[3]]  # фигура из последнего хода
        my_pawn = self.field[from_x][from_y]
        if not (isinstance(bad_pawn, Pawn) and abs(bad_pawn.y - last_move[1]) == 2):  # пешка противника сходила на 2
            return False
        if not (isinstance(my_pawn, Pawn) and bad_pawn.color != my_pawn.color):  # моя пешка это пешка и другого цвета
            return False
        if not (to_x == bad_pawn.x):
            return False
        sign = 1
        if my_pawn.color:
            sign = -1
        if self.field[to_x][from_y] == bad_pawn:
            if to_y == bad_pawn.y + sign:
                return True
        return False

    def castling(self, from_x, from_y, to_x, to_y):
        king = self.field[from_x][from_y]
        if not isinstance(king, King):
            return False

        if king.first_move and to_y == king.y and not king.check:
            rook_left = self.field[0][king.y]
            rook_right = self.field[7][king.y]

            if not (to_x in (2, 6)):
                return False
            inc = (to_x - king.x)//2

            if inc == -1:
                if not(isinstance(rook_left, Rook) and rook_left.first_move and rook_left.can_move(king.x - 1, king.y)):
                    return False
            elif inc == 1:
                if not(isinstance(rook_right, Rook) and rook_right.first_move and rook_right.can_move(king.x + 1, king.y)):
                    return False

            if self.move(king.x, king.y, king.x + inc, king.y):
                if not self.check(not king.color, True):
                    if self.move(king.x, king.y, king.x + inc, king.y):
                        if not self.check(not king.color, True):
                            self.backtrack()
                            self.backtrack()
                            return True
                        self.backtrack()
                self.backtrack()
        return False

    def check_check(self, from_x, from_y, to_x, to_y, color):   # color - цвет того, кто делает шах
        if self.move(from_x, from_y, to_x, to_y):
            if self.check(color, True):
                self.backtrack()
                return True
            self.backtrack()
        return False

    def check(self, color, fake):   # color - цвет того, кто делает шах
        if color:
            for i in self.figures[1]:
                if i is None:
                    continue
                if self.king_white is None:
                    return False
                if i.can_move(self.king_white.x, self.king_white.y):
                    if not fake:
                        self.king_white.check = True
                    return True
            if not fake:
                self.king_white.check = False
        else:
            for i in self.figures[0]:
                if i is None:
                    continue
                if self.king_black is None:
                    return False
                if i.can_move(self.king_black.x, self.king_black.y):
                    if not fake:
                        self.king_black.check = True
                    return True
            if not fake:
                self.king_black.check = False
        return False

    def checkmate(self, color):  # color - цвет того, кто ставит мат
        for i in self.figures[int(not color)]:
            if i is None:
                continue
            for j in range(8):
                for k in range(8):
                    if ((i.can_move(j, k) or self.el_passant(i.x, i.y, j, k)) and
                            not self.check_check(i.x, i.y, j, k, color)):
                        return False
        print(f"{('White', 'Black')[int(color)]} won!!!")
        return True

    def backtrack(self):
        if len(self.moves) > 0:
            last_move = self.moves[-1]
            back_figure = self.field[last_move[2]][last_move[3]]
            back_figure.x = last_move[0]
            back_figure.y = last_move[1]
            self.field[last_move[0]][last_move[1]] = back_figure
            self.field[last_move[2]][last_move[3]] = last_move[4]
            if len(last_move)==6:
                back_figure.first_move = True
        else:
            return
        if (isinstance(self.field[last_move[0]][last_move[1]], Pawn) and  # возврат рубки на проходе
                last_move[4] is None and last_move[0] != last_move[2]):
            last_move = self.moves[-1]
            self.field[last_move[0]][last_move[1]] = last_move[4]
        if last_move[4] is not None:
            self.figures[int(last_move[4].color)].append(last_move[4])
        self.moves.pop()
        if len(self.moves) > 0:
            new_last_move = self.moves[-1]
            inc = new_last_move[0] - new_last_move[2]
            if abs(inc) == 2:
                self.field[new_last_move[2]][new_last_move[3]].first_move = True
                if inc > 0:
                    self.field[0][new_last_move[1]].first_move = True
                else:
                    self.field[7][new_last_move[1]].first_move = True
                self.backtrack()

    def draw_classic(self):  # устанавливает фигуры в стандартное шахматное расположение
        for i in range(8):
            self.field[i][1] = Pawn(i, 1, False, self.field)  # пешки белых
            self.field[i][6] = Pawn(i, 6, True, self.field)  # пешки черных
        self.field[1][0], self.field[6][0] = Knight(1, 0, False, self.field), Knight(6, 0, False, self.field)  # кони
        self.field[1][7], self.field[6][7] = Knight(1, 7, True, self.field), Knight(6, 7, True, self.field)  #
        self.field[0][0], self.field[7][0] = Rook(0, 0, False, self.field), Rook(7, 0, False, self.field)  # ладьи
        self.field[0][7], self.field[7][7] = Rook(0, 7, True, self.field), Rook(7, 7, True, self.field)  #
        self.field[2][0], self.field[5][0] = Bishop(2, 0, False, self.field), Bishop(5, 0, False, self.field)  # слоны
        self.field[2][7], self.field[5][7] = Bishop(2, 7, True, self.field), Bishop(5, 7, True, self.field)  #
        self.field[3][0], self.field[3][7] = Queen(3, 0, False, self.field), Queen(3, 7, True, self.field)  # ферзи
        self.field[4][0], self.field[4][7] = King(4, 0, False, self.field), King(4, 7, True, self.field)  # короли


class Pawn(Figure):  # класс пешки

    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            if y == 6:
                self.first_move = True
            self.icon = figures['black']['pawn']
        else:
            if y == 1:
                self.first_move = True
            self.icon = figures['white']['pawn']

    def can_move(self, x, y):
        if super().can_move(x, y):  # вызов базовой проверки хода родительского класса "фигура"
            sign = -1
            if self.color:
                sign = 1
            if self.x == x and self.field[x][y] is None:  # ход пешки вперед
                if ((not self.color and self.y == 1 or self.color and self.y == 6)
                        and self.y - y == 2 * sign and self.field[x][y + sign] is None):
                    return True  # ход на две клетки
                elif self.y - y == 1 * sign:
                    return True  # ход на одну клетку
            elif self.x - 1 == x or self.x + 1 == x:
                if self.y - sign == y:
                    if self.field[x][y] is not None and self.color != self.field[x][y].color:
                        return True  # рубка по диагонали
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
    first_move = False

    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            if x == 0 and y == 7 or x == 7 and y == 7:
                self.first_move = True
            self.icon = figures['black']['rook']
        else:
            if x == 0 and y == 0 or x == 7 and y == 0:
                self.first_move = True
            self.icon = figures['white']['rook']

    def can_move(self, x, y):
        if Figure.can_move(self, x, y):
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
        if Figure.can_move(self, x, y):
            if abs(self.x - x) == abs(self.y - y):  # проверка на возможность хода на эту клетку
                inc_x, inc_y = 1, 1
                if self.x > x:
                    inc_x = -1
                if self.y > y:
                    inc_y = -1
                for i in range(1, abs(self.x - x), 1):
                    if self.field[self.x + i * inc_x][self.y + i * inc_y] is not None:
                        return False
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
    first_move = False
    check = False

    def __init__(self, x, y, color, field):
        super().__init__(x, y, color, field)
        if color:
            if x == 4 and y == 7:
                self.first_move = True
            self.icon = figures['black']['king']
        else:
            if x == 4 and y == 0:
                self.first_move = True
            self.icon = figures['white']['king']

    def can_move(self, x, y):
        if super().can_move(x, y):
            if (-1 <= self.x - x <= 1) and (-1 <= self.y - y <= 1):
                return True
        return False
