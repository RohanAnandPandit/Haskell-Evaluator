# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:24:50 2020

@author: rohan
"""

import utils
import ctypes
import os
from Editor import Editor
from State import State

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)


def console():
    state = State()
    while True:
        string = input('Start> ')
        if string == '':
            continue
        elif string == '$quit':
            break
        elif string == '$stack':
            print(state.frame_stack)
            continue
        elif string == '$edit':
            Editor(state)
        # try:
        value = state.evaluate(string)
        print(str(value))
        # except:
        # print("ERROR!")


console()
# wait = input()
