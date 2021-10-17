from project.math_logic.equation_builder import Expression
from random import randrange

my_equation = Expression()
x, y = my_equation.set_variables('x y')
my_equation.define(y*y + x*y + 3)

x_var = randrange(10)
y_var = randrange(10)
print(x_var, y_var)

answer = my_equation.resolve([x_var, y_var])
print(answer)

x_var = randrange(10)
y_var = randrange(10)

print("What is", my_equation.get_equation(), "when x is", x_var, "and y is", y_var, "?")
user_answer = int(input("student answer: "))

answer = my_equation.resolve([x_var, y_var])
print(abs(user_answer-answer) < 0.5)
