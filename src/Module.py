class Module:
    def __init__(self, name, code, program_state):
        self.name = name
        self.state = {}
        program_state.frame_stack.append(self.state)
        program_state.evaluate(code)
        program_state.frame_stack.pop(-1)
        program_state.frame_stack[-1].update(self.state)

    def simplify(self, program_state):
        return self

    def __str__(self):
        return self.name