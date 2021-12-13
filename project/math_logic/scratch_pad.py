from project.math_logic.equation_builder import MathExpression
from random import randrange


eq = MathExpression('x * y')
# print(eq.expression_string)
eq.replace_variables([2, 6])
# print(eq.expression_string)
answer = eq.resolve()
# print(answer)


# eq = MathExpression('x + v * t + a * t^2 / 2')
# print(eq.expression_string)
# eq.replace_variables([2, None, 1])
# print(eq.expression_string)
# answer = eq.resolve()
# print(answer)
