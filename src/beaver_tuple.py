# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:19:03 2020

@author: rohan
"""

function_names_tuple = ['fst', 'snd', 'swap']


class Tuple:
    def __init__(self, tup, program_state):
        self.tup = tup
        self.items = tup
        self.program_state = program_state

    def simplify(self, program_state):
        from utils import replace_variables
        tup = Tuple(list(map(lambda expr: replace_variables(expr, program_state),
                             self.tup)), program_state)
        return tup

    def __str__(self):
        tup = []
        for item in self.items:
            value = item
            tup.append(str(value))
        string = ', '.join(tup)

        if len(tup) == 1:
            string += ','
        return '(' + string + ')'
