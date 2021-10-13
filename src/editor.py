# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 22:02:35 2020

@author: rohan
"""
import tkinter as tk


class Editor:
    def __init__(self, program_state):
        self.program_state = program_state
        self.light_mode = {'bg': 'white', 'fg': 'black',
                           'operators': 'orange', 'insert': 'black',
                           'keywords': 'orange', 'string': 'lime green'}
        self.dark_mode = {'bg': 'black', 'fg': 'white',
                          'operators': 'yellow', 'insert': 'white',
                          'keywords': 'cyan', 'string': 'lime green'}
        self.mode = self.dark_mode

        root = tk.Tk()
        root.title('Beaver')
        root.attributes('-topmost', True)
        root.geometry('1700x1600+0+0')
        self.text = tk.Text(root, width=80, height=35,
                            font=('Consolas', 14, 'normal'),
                            bg=self.mode['bg'],
                            fg=self.mode['fg'],
                            insertbackground=self.mode['insert'],
                            tabs=('1c'))
        b = tk.Button(root, text='Run',
                      command=lambda event: self.execute())
        b.grid(column=2, row=0)
        self.text.grid(column=0, row=0)

        scrollb = tk.Scrollbar(root, orient="vertical",
                               command=self.text.yview)
        scrollb.grid(column=1, row=0)

        self.text.configure(yscrollcommand=scrollb.set)
        self.text.tag_config('bracket', foreground='red')
        root.bind('<Return>', lambda event: self.enter())
        root.bind('<BackSpace>', lambda event: self.backspace())
        root.bind('<KeyPress>', lambda event: self.analyse(event))
        root.bind('<Control-s>', lambda event: self.save_code())
        root.bind('<F5>', lambda event: self.execute())
        root.mainloop()

    def backspace(self):
        while self.text.get('insert-1c') in ' \n':
            char = self.text.get('insert-1c')
            self.text.delete('insert-1c', 'insert')
            if char == '\n': break

    def save_code(self):
        file = open('code.txt', 'w')
        file.write(self.text.get(1.0, tk.END))

    def enter(self):
        prev_char = self.text.get('insert-2c')
        next_char = self.text.get('insert')
        tabs = self.tabs_on_current_line()

        self.text.mark_set('insert', 'insert lineend+1c')
        self.text.insert(tk.INSERT, tabs * '\t')
        if prev_char in '({':
            self.text.insert(tk.INSERT, '\t')
            if next_char in ')}':
                self.text.insert(tk.INSERT, '\n' + tabs * '\t')
                self.text.mark_set('insert', 'insert-' + str(tabs + 1) + 'c')

    def tabs_on_current_line(self):
        self.text.mark_set('insert', 'insert-1lines')
        pos = 'insert'
        tabs = 0
        while self.text.get(pos) == '\t':
            tabs += 1
            pos += '+1c'
        return tabs

    def analyse(self, event):
        self.auto_complete_pair(event)
        self.highlight_operators()
        self.highlight_keywords()
        self.highlight_functions()
        self.highlight_comments()
        self.highlight_strings()

    def highlight_strings(self):
        self.text.tag_remove('string', '1.0', tk.END)
        start = 1.0
        while 1:
            pos1 = self.text.search('"', start, stopindex=tk.END)

            if not pos1:
                break
            start = pos1 + '+1c'
            pos2 = self.text.search('"', start, stopindex=tk.END)

            if not pos2:
                break
            pos2 += '+1c'
            self.text.tag_add("string", pos1, pos2)
            start = pos2
        start = 1.0
        while 1:
            pos1 = self.text.search("'", start, stopindex=tk.END)
            if not pos1:
                break

            if self.text.get(pos1 + '+1c') == "'":
                start = pos1 + '+2c'
                continue
            if not self.text.get(pos1 + '+2c'):
                break

            elif self.text.get(pos1 + '+2c') == "'":
                self.text.tag_add("string", pos1, pos1 + '+3c')
                start = pos1 + '+3c'
            else:
                start = pos1 + '+1c'
        self.text.tag_config("string", foreground=self.mode['string'])

    def highlight_comments(self):
        self.text.tag_remove('comment', '1.0', tk.END)
        start = 1.0
        while 1:
            pos1 = self.text.search('#', start, stopindex=tk.END)

            if not pos1:
                break
            start = pos1 + '+1c'
            pos2 = self.text.search('#', start, stopindex=tk.END)

            if not pos2:
                break
            pos2 += '+1c'
            self.text.tag_add("comment", pos1, pos2)
            start = pos2 + '+1c'
        self.text.tag_config("comment", foreground='red')

    def highlight_functions(self):
        self.text.tag_remove('function', '1.0', tk.END)
        for name in self.program_state.function_names:
            start = 1.0
            while 1:
                pos = self.text.search(name, start, stopindex=tk.END)
                if not pos:
                    break
                end = pos + '+' + str(len(name)) + 'c'

                if (self.text.get(end) in self.program_state.operators and
                        (pos == '1.0' or
                         self.text.get(pos + '-1c') in self.program_state.operators)):
                    self.text.tag_add("function", pos, end)
                start = end
        self.text.tag_config("function", foreground='magenta')

    def highlight_keywords(self):
        self.text.tag_remove('keyword', '1.0', tk.END)
        for keyword in self.program_state.keywords:
            start = 1.0
            while 1:
                pos = self.text.search(keyword, start, stopindex=tk.END)
                if not pos:
                    break
                end = pos + '+' + str(len(keyword)) + 'c'
                if (self.text.get(end) in self.program_state.operators and
                        (pos == '1.0' or
                         self.text.get(pos + '-1c') in self.program_state.operators)):
                    self.text.tag_add("keyword", pos, end)
                start = end
        self.text.tag_config("keyword", foreground=self.mode['keywords'])

    def highlight_operators(self):
        self.text.tag_remove('operator', '1.0', tk.END)
        for operator in self.program_state.operators:
            if operator in '(){}[] in':
                continue
            start = 1.0
            while 1:
                pos = self.text.search(operator, start, stopindex=tk.END)
                if not pos:
                    break
                end = pos + '+' + str(len(operator)) + 'c'
                self.text.tag_add("operator", pos, end)
                start = end
        self.text.tag_config("operator", foreground=self.mode['operators'])

    def auto_complete_pair(self, event):
        if len(event.char) == 1 and event.keysym != 'BackSpace':
            if self.text.get('insert-1c') == '{':
                self.text.insert(tk.INSERT, '}')
                self.text.mark_set("insert", "insert-1c")
            elif self.text.get('insert-1c') == '(':
                self.text.insert(tk.INSERT, ')')
                self.text.mark_set("insert", "insert-1c")
            elif self.text.get('insert-1c') == '[':
                self.text.insert(tk.INSERT, ']')
                self.text.mark_set("insert", "insert-1c")
            elif self.text.get('insert-1c') == '"':
                self.text.insert(tk.INSERT, '"')
                self.text.mark_set("insert", "insert-1c")

    def execute(self):
        code = self.text.get(1.0, tk.END)
        self.program_state.evaluate(code, reset_state=True)
