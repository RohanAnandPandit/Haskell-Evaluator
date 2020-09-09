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

state = State()
def console():
    while (True):
        string = input('Start> ')
        if (string == ''):
            continue
        elif (string == '$quit'):
            break
        elif (string == '$stack'):
            print(utils.frameStack)
            continue
        elif (string == '$edit'):
            Editor(state)
        value = state.evaluate(string) 
        print(value)

console()








