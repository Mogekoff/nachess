from nachess import *
import pygame


def main():
    mv = [(1,7,2,5),(4,1,4,3)]
    field = Field(None, mv)
    field.print()
    while True:
        x, y, X, Y = int(input()), int(input()), int(input()), int(input())
        field.move(x, y, X, Y)
        field.print()


if __name__ == '__main__':
    main()
