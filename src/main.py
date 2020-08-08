# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:24:50 2020

@author: rohan
"""
import utils
from utils import builtInState, frameStack, haskellEval, functionNames, operators, keywords
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
    if "#STATIC-MODE#\n" in code:
        utils.static_mode = True
    if "#FUNCTIONAL-MODE#\n" in code:
        utils.functional_mode = True
    parts = code.split('#EVAL#\n')
    for part in parts:
        haskellEval(part)

lightmode = {'bg' : 'white', 'fg' : 'black', 'operators' : 'orange', 'insert' : 'black', 'keywords' : 'orange'}
darkmode = {'bg' : 'black', 'fg' : 'white', 'operators' : 'yellow', 
            'insert' : 'white', 'keywords' : 'cyan', 'string' : 'lime green'}
mode = darkmode
  
def ide():
    root = tk.Tk()
    root.title('Beaver')
    root.attributes('-topmost', True)
    root.geometry('1700x1600+0+0')
    text = tk.Text(root, width = 80, height = 40, font = ('Consolas', 14, 'normal'), bg = mode['bg'],
                   fg = mode['fg'], insertbackground = mode['insert'], tabs = ('1c'))
    tk.Button(root, text = 'Run', command = lambda: execute(text)).grid(column = 2, row = 0)
    text.grid(column = 0, row = 0)
    
    scrollb = tk.Scrollbar(root, orient = "vertical", command = text.yview)
    scrollb.grid(column = 1, row = 0)
    
    text.configure(yscrollcommand = scrollb.set)
    text.tag_config('bracket', foreground = 'red')
    root.bind('<KeyPress>', lambda event: analyse(event, text))
    root.bind('<KeyPress>', lambda event: analyse(event, text))
    root.bind('<Control-s>', lambda event: save_code(text))
    root.bind('<F5>', lambda event: execute(text))
    root.mainloop() 

def save_code(text):
    file = open('code.txt', 'w')
    file.write(text.get(1.0, tk.END))
    
def analyse(event, text):
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

    text.tag_remove('function', '1.0', tk.END)    
    for name in functionNames:
        start = 1.0
        while 1:
            pos = text.search(name, start, stopindex = tk.END)
            if not pos:
                break
            end = pos + '+' + str(len(name)) + 'c'
            if (text.get(end) in ' \n)]}~$;' 
                and (pos == '1.0' or text.get(pos + '-1c') in ' \n\t([{~$;')):
                text.tag_add("function", pos, end) 
            start = end 
    text.tag_config("function", foreground = 'magenta')
            
    
    text.tag_remove('operator', '1.0', tk.END)    
    for operator in operators:
        start = 1.0
        while 1:
            pos = text.search(operator, start, stopindex = tk.END)
            if not pos:
                break
            end = pos + '+' + str(len(operator)) + 'c'
            text.tag_add("operator", pos, end) 
            start = end 
    text.tag_config("operator", foreground = mode['operators'])

    text.tag_remove('keyword', '1.0', tk.END)    
    for keyword in keywords:
        start = 1.0
        while 1:
            pos = text.search(keyword, start, stopindex = tk.END)
            if not pos:
                break
            end = pos + '+' + str(len(keyword)) + 'c'
            if (text.get(end) in ' \n)]}~$;'
                and (pos == '1.0' or text.get(pos + '-1c') in ' \n\t([{~$;')):
                text.tag_add("keyword", pos, end) 
            start = end 
    text.tag_config("keyword", foreground = mode['keywords'])
    
    text.tag_remove('comment', '1.0', tk.END)  
    start = 1.0
    while 1:
        pos1 = text.search('#', start, stopindex = tk.END)
        if not pos1:
            break 
        start = pos1 + '+1c'
        pos2 = text.search('#', start, stopindex = tk.END)
        if not pos2:
            break
        pos2 += '+1c'
        text.tag_add("comment", pos1, pos2)
        start = pos2 + '+1c'
    text.tag_config("comment", foreground = 'red') 
            

    text.tag_remove('string', '1.0', tk.END)    
    start = 1.0
    while 1:
        pos1 = text.search('"', start, stopindex = tk.END)
        if not pos1:
            break 
        start = pos1 + '+1c'
        pos2 = text.search('"', start, stopindex = tk.END)
        if not pos2:
            break 
        pos2 += '+1c'
        text.tag_add("string", pos1, pos2)
        start = pos2
    text.tag_config("string", foreground = mode['string']) 
                
#way = input('Do you want to write on command-line or IDE?: ')
#if way == 'ide':
ide()
#else:
#commandLine()