from Function import Func, Function
from Types import Variable


class Class(Func):
    def __init__(self, name):
        self.name = 'class ' + name
        self.state = {}
        self.parent_classes = []
        self.interfaces = []
        self.private = []
        self.public = []
        self.hidden = []
        self.is_constructor = False
        self.lazy = True

    def apply(self, expr, program_state=None):
        if not self.is_constructor:
            self.is_constructor = True
            self.name = self.name.split(' ')[1]
            program_state.frame_stack.append(self.state)
            program_state.in_class += 1
            expr.simplify(program_state)
            program_state.in_class -= 1
            program_state.frame_stack.pop(-1)
            program_state.function_names.append(self.name)
            return self
        else:
            values = expr
            obj = Object(self, program_state)
            for name in list(self.state.keys()):
                obj.state[name] = self.state[name]
                if type(self.state[name]).__name__ == 'Function':
                    func = obj.state[name]
                    func = func.clone()
                    obj.state[name] = func
                    for case in func.cases:
                        case.state['this'] = obj

            if 'init' in list(obj.state.keys()):
                # print('init')
                obj.state['init'].apply(values, program_state=program_state)

            return obj

    def __str__(self):
        return self.name

    def simplify(self, program_state):
        return self


class Method(Func):
    def __init__(self, obj, func, program_state):
        self.name = func.name
        self.obj = obj
        self.func = func
        self.lazy = False
        self.program_state = program_state

    def apply(self, arg1=None, arg2=None, program_state=None):
        program_state.frame_stack.append({'this': self.obj})
        value = self.func.apply(arg1, arg2, program_state=program_state)
        program_state.frame_stack.pop(-1)
        if issubclass(type(value), Func) and value.name == self.name:
            return Method(self.obj, value, program_state)
        return value

    def simplify(self, program_state):
        self.program_state.frame_stack.append({'this': self.obj})
        value = self.func.simplify(program_state)
        self.program_state.frame_stack.pop(-1)
        if issubclass(type(value), Func) and value.name == self.name:
            return Method(self.obj, value, program_state)
        return value

    def __str__(self):
        return str(self.obj) + ' ' + str(self.func)


class Object:
    def __init__(self, class_, program_state):
        self.class_ = class_
        self.state = {'this': self}
        self.program_state = program_state

    def simplify(self, program_state):
        return self

    def __str__(self):
        if 'toString' in list(self.state.keys()):
            string = self.state['toString'].simplify(self.program_state).value
            return string
        return self.class_.name + ' object'


class Interface:
    def __init__(self, name, declarationExpr, program_state):
        self.name = name
        state = {}
        program_state.frame_stack = program_state.frame_stack
        program_state.frame_stack.append(state)
        program_state.in_class += 1
        declarationExpr.simplify(program_state)
        program_state.in_class -= 1
        program_state.frame_stack.pop(-1)
        self.methods = state.keys()

    def simplify(self, program_state):
        return self

    def __str__(self):
        return self.name + ' ' + ' '.join(self.methods)
