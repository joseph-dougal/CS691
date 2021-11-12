from project.math_logic.equation_builder import MathExpression
from random import randrange


eq = MathExpression('x + v * t + a * t^2 / 2')
print(eq.expression_string)
# print(eq.variables_list)

eq.replace_variables([2, None, 1])
print(eq.expression_string)

# eq.simplify()
# print(eq.expression_string)
# print(eq.variables_list)

eq.print_resolve([3, 4])


