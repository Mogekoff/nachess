from nachess import *
import pygame


def main():
    mv = [(1,7,2,5),(4,1,4,3),(1,6,1,4),(1,4,1,3),(1,3,1,2),(4,6,4,4),(3,7,6,4),(2,1,1,2),(1,2,1,3),(1,3,1,4),(0,6,0,4)]
    field = Field(None, mv)
    field.print()
    while True:
        cmd_input = input('nachess> ')
        cmd_split = cmd_input.split(' ')
        if cmd_split[0] == 'how':
            field.print(int(cmd_split[1]),int(cmd_split[2]))
        elif cmd_split[0] == 'go':
            x, y, X, Y = int(cmd_split[1]), int(cmd_split[2]), int(cmd_split[3]), int(cmd_split[4])
            field.move(x, y, X, Y)
            field.print()
        elif cmd_split[0] == 'back':
            field.backtrack()
            field.print()


if __name__ == '__main__':
    main()
