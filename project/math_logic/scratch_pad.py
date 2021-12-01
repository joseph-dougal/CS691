from project.math_logic.equation_builder import MathExpression
from random import randrange


# eq = MathExpression('x + v * t + a * t^2 / 2')
eq = MathExpression('x * y')
print(eq.expression_string)
# print(eq.variables_list)

# eq.replace_variables([2, 7, 6])
eq.replace_variables([2, 6])
print(eq.expression_string)

# eq.simplify()
# print(eq.variables_list)

answer = eq.resolve()
print(answer)



