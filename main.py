from nachess import *
import pygame

def main():
    field = Field()
    field.draw_classic()
    field.print()
    while True:
        x, y, X, Y = int(input()), int(input()), int(input()), int(input())
        field.field[x][y].move(X, Y)
        field.print()


if __name__ == '__main__':
    main()
