class Alias:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __str__(self):
        return str(self.var) + '@' + str(self.expr)

    def simplify(self, program_state):
        return self