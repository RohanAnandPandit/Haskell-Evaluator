# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:24:50 2020

@author: rohan
"""
from utils import builtInState, frameStack, haskellEval, functionNames, operators
from Operators import initialiseFunctions
import tkinter as tk
import ctypes
import os
ctypes.windll.shcore.SetProcessDpiAwareness(1)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50) 

initialiseFunctions(builtInState)

def commandLine():
    while (True):
        string = input('Prelude> ')
        if (string == ''):
            continue
        elif (string == '$quit'):
            break
        elif (string == '$stack'):
            print(frameStack)
            continue
        value = haskellEval(string)
        if (value != None):
            print(value)

def execute(text):
    code = text.get(1.0, tk.END)
    parts = code.split('#EVAL#\n')
    for part in parts:
        haskellEval(part)    
    
def ide():
    root = tk.Tk()
    root.title('Caskell')
    root.attributes('-topmost', True)
    root.geometry('2500x1000+0+0')
    text = tk.Text(root, width = 70, height = 25, font = ('Consolas', 20, 'normal'), bg = 'black',
                   fg = 'white', insertbackground = 'white', tabs = ('1c'))
    tk.Button(root, text = 'Run', command = lambda: execute(text)).grid(column = 2, row = 0)
    text.grid(column = 0, row = 0)
    
    scrollb = tk.Scrollbar(root, orient = "vertical", command = text.yview)
    scrollb.grid(column = 1, row = 0)
    
    text.configure(yscrollcommand = scrollb.set)
    text.tag_config('bracket', foreground = 'red')
    root.bind('<KeyPress>', lambda event: analyse(event, text))
    root.bind('<KeyPress>', lambda event: analyse(event, text))
    root.mainloop() 

def analyse(event, text):
    text.tag_remove('keyword', '1.0', tk.END)    
    for keyword in ('class', 'def', 'struct', 'interface', 'extends',
                    'where', 'implements', 'while', 'for', 'switch', 'default'):
        start = 1.0
        while 1:
            pos = text.search(keyword, start, stopindex = tk.END)
            if not pos:
                break
            end = pos + '+' + str(len(keyword)) + 'c'
            if text.get(end) in operators:
                text.tag_add("keyword", pos, end)
            start = end 
    text.tag_config("keyword", foreground = 'cyan')
    
    text.tag_remove('bracket', '1.0', tk.END)    
    for bracket in ('(', ')', '[', ']', '{', '}'):
        start = 1.0
        while 1:
            pos = text.search(bracket, start, stopindex = tk.END)
            if not pos:
                break
            end = pos + '+1c'
            text.tag_add("bracket", pos, end)
            start = end 
    text.tag_config("bracket", foreground = 'yellow')

    text.tag_remove('function', '1.0', tk.END)    
    for name in functionNames:
        start = 1.0
        while 1:
            pos = text.search(name, start, stopindex = tk.END)
            if not pos:
                break
            end = pos + '+' + str(len(name)) + 'c'
            if text.get(end) in operators:
                text.tag_add("function", pos, end) 
            start = end 
    text.tag_config("function", foreground = 'magenta')
    
    if len(event.char) == 1 and event.keysym != 'BackSpace':
        if text.get('insert-1c') == '{':
            text.insert(tk.INSERT, '}')
            text.mark_set("insert", "insert-1c")
        elif text.get('insert-1c') == '(':
            text.insert(tk.INSERT, ')')
            text.mark_set("insert", "insert-1c")
        elif text.get('insert-1c') == '[':
            text.insert(tk.INSERT, ']')
            text.mark_set("insert", "insert-1c")
        elif text.get('insert-1c') == '"':
            text.insert(tk.INSERT, '"')
            text.mark_set("insert", "insert-1c")
            
            
way = input('Do you want to write on command-line or IDE?: ')
if way == 'ide':
    ide()
else:
    commandLine()

