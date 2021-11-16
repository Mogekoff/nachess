from nachess import *
import pygame


def main():
    mv = [(1,7,2,5),(4,1,4,3),(1,6,1,4),(1,4,1,3),(1,3,1,2),(4,6,4,4),(3,7,6,4)]
    field = Field(None, mv)
    field.print()
    while True:
        x, y, X, Y = int(input()), int(input()), int(input()), int(input())
        field.move(x, y, X, Y)
        field.print()


if __name__ == '__main__':
    main()
