from py_expression_eval import Parser


class MathExpression:

    def __init__(self, equation_arg):
        self.define(equation_arg)  # The define function is used to instantiate and redefine the equation if needed

    def define(self, equation_arg):
        """
        The define function is used to construct the MathExpression object. No field is private or protected.

        Field structure:
        expression_string, String
        equation_parser, Parser Object
        variables_list, List of Strings
        """
        self.expression_string = equation_arg  # expression_string contains the equation in string form
        self.equation_parser = Parser().parse(equation_arg)  # equation_parser contains the parser object
        self.variables_list = self.equation_parser.variables()  # variables_list contains the list of string variables

    def replace_variables(self, replacements_list):
        """
        The replace_variables function only accepts a list of integers argument. The list should be ordered
        in the same order as the variables appear in the equation, lef to right. If a variables needs to
        remain as a variable and not replaced with a number, use None in place of an integer/float. The list
        argument must be the same length or shorter than the field variables_list.
        """
        assert len(replacements_list) <= len(
            self.variables_list)  # Confirms that the argument is shorter than variables_list

        for i in range(len(replacements_list)):

            if replacements_list[i]:  # Only replace variable if replacement is not None

                # Replaces string value in field expression_string, replacement is converted from int/float to string
                self.expression_string = self.expression_string.replace(self.variables_list[i],
                                                                        str(replacements_list[i]))

        self.define(self.expression_string)  # MathExpression object is reconstructed from new string

    def simplify(self):
        """
        The simplify function used in the original API of the Parser object to 'simplify' the expression.
        The simplification is to remove any ambiguity in the expression with the inclusion of verbose
        parenthesis. If this is not needed in the use of MathExpression, feel free to delete this.
        """
        simplified_string = self.equation_parser.simplify(
            {}).toString()  # Rewrites Parser object to include verbose parenthesis, returns string

        self.define(
            simplified_string)  # Reconstructs MathExpression object using verbose parenthesis form from string equation

    def resolve(self, values=None):
        """
        The resolve function returns the result of the equation, int/float. If the equation requires values for
        any of the remaining variables, they should be passed in the argument values as a list of
        int/floats.
        """

        if values:  # Assert that values is not None

            prev_expression_string = self.expression_string  # Retain current expression_string with variable as string

            self.replace_variables(values)  # Replace variables in MathExpression object with int/float values

            result = self.equation_parser.evaluate({})  # Evaluate Parser object, returns int/float

            self.define(prev_expression_string)  # Redefine MathExpression object with previous expression_string

            return result  # Return int/float result of Parser object

        else:
            return self.equation_parser.evaluate({})  # Return int/float result of Parser object

    # Various print functions for ease in design/implementation, no field is private/protected
    def print_variables(self):
        print(self.variables_list)

    def print_num_variables(self):
        print(len(self.variables_list))

    def print_expression(self):
        print(self.expression_string)

    def print_resolve(self, values=None):
        print(self.resolve(values))
