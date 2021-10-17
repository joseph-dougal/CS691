import sympy as sym


class Expression:

    def __init__(self):
        self.count = None
        self.equation = None
        self.variables = None

    def set_variables(self, name_string):
        name_arr = name_string.split(' ')
        variable_list = [None]*len(name_arr)
        for i, name in enumerate(name_arr):
            variable_list[i] = sym.var(name)

        self.variables = variable_list
        self.count = len(variable_list)
        return variable_list

    def define(self, user_equation):
        self.equation = user_equation

    def resolve(self, value_list):
        answer = self.equation
        for i in range(self.count):
            answer = answer.subs(self.variables[i], value_list[i])
        return answer

    def get_equation(self):
        return self.equation

    def get_count(self):
        return self.count

    def get_variables(self):
        return self.variables
