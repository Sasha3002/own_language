from interpreter.context import ContextManager
import interpreter.classes as c
import parser.nodes as nodes
from parser.nodes import MainVisitor
import errors.errors as e
from parser.parser import Operators


class Visitor(MainVisitor):
    def __init__(self):
        self.context_manager = ContextManager()
        self.last_result = None

    def is_variable(self, identifier: str):
        return self.context_manager.is_variable_exists(identifier)
    
    def visit_identifier(self, identifier: nodes.Identifier):
        if self.is_variable(identifier.name) or identifier.name == 'print' or self.context_manager.is_function_exists(identifier.name) or any(identifier.name in values for values in self.context_manager.BUILT_IN.values()):
            self.last_result = identifier.name
        else: 
            raise e.UndeclaredVariableError(identifier.name, identifier.column, identifier.line)

    def visit_bool_value(self, bool_value: nodes.BoolValue):
        self.last_result = bool_value.value

    def visit_int_value(self, int_value: nodes.IntValue):
        self.last_result = int_value.value

    def visit_float_value(self, float_value: nodes.FloatValue):
        self.last_result = float_value.value

    def visit_string_value(self, string_value: nodes.StringValue):
        self.last_result = string_value.value

    def visit_function_type(self, function_type: nodes.FunctionType):
        self.last_result = function_type.type

    def visit_variable_type(self, variable_type: nodes.VariableType):
        self.last_result = variable_type.type

    def visit_parameter(self, parameter: nodes.Parameter):
        parameter.type.accept(self)
        param_type = self.last_result
        param_name = parameter.identifier
        self.last_result = (param_type, param_name)

  

    def visit_negation_expression(self, negation_expression: nodes.NegationExpression):
        negation_expression.expression.accept(self)
        expression = self.last_result

        if self.is_variable(expression):
            expression = self.context_manager.get_variable_value(expression)

        operator = negation_expression.operator
        if operator == Operators.MINUS:
            if not isinstance(expression, (int, float)):
                    raise e.InvalidTypeError("Negation requires numeric types", negation_expression.column, negation_expression.line)
            self.last_result = -expression
        elif operator == Operators.NOT:
            if not isinstance(expression, bool):
                    raise e.InvalidTypeError("Logical NOT requires a boolean type", negation_expression.column, negation_expression.line)
            self.last_result = not expression

    def visit_method_call_expression(self, method_call_expression: nodes.MethodCallExpression):
        method_call_expression.caller.accept(self)
        caller = self.last_result
        if not self.is_variable(caller):
            raise e.UndeclaredVariableError(caller, method_call_expression.column, method_call_expression.line)
        for method in method_call_expression.methods:
            method.accept(self, caller)
            caller = self.last_result
        self.last_result = caller

    def visit_method_call(self, method_call: nodes.MethodCall, caller):
        accepted_arguments = []
        for argument in method_call.arguments:
            argument.accept(self)
            accepted_arguments.append(self.last_result)
        method_call.name.accept(self)
        method_name = self.last_result
        self.execute_method(caller, method_name, accepted_arguments)

    def visit_binary_expression(self, binary_expression: nodes.BinaryExpression):
        binary_expression.left.accept(self)
        left = self.last_result
        binary_expression.right.accept(self)
        right = self.last_result

        if self.is_variable(left):
            left = self.context_manager.get_variable_value(left)
        if self.is_variable(right):
            right = self.context_manager.get_variable_value(right)

        operator = binary_expression.operator
        if operator == Operators.PLUS:
            self.last_result = self.binary_plus(left, right)
        elif operator == Operators.MINUS:
            self.last_result = self.binary_minus(left, right, binary_expression.column, binary_expression.line)
        elif operator == Operators.MUL:
            self.last_result = self.binary_mult(left, right, binary_expression.column, binary_expression.line)
        elif operator == Operators.DIV:
            self.last_result = self.binary_div(left, right, binary_expression.column, binary_expression.line)
        elif operator in (Operators.GREATER, Operators.LE, Operators.GE, Operators.EQ, Operators.NEQ, Operators.LESS):
            self.last_result = self.comparison(operator, left, right, binary_expression.column, binary_expression.line)
        elif operator == Operators.AND:
            self.last_result = self.logical_and(left, right, binary_expression.column, binary_expression.line)
        elif operator == Operators.OR:
            self.last_result = self.logical_or(left, right, binary_expression.column, binary_expression.line)

    def binary_plus(self, left, right):
        if isinstance(left, str) or isinstance(right, str):
            return str(left) + str(right)
        else:
            return left + right
        
    def binary_minus(self, left, right, column, line):
        if isinstance(left, str) or isinstance(right, str):
            raise e.InvalidTypeError("Subtraction requires numeric types", column, line)
        return left - right

    def binary_mult(self, left, right, column, line):
        if isinstance(left, str) and isinstance(right, int):
            return left * right
        if isinstance(right, str) and isinstance(left, int):
            return right * left
        if isinstance(left, str) or isinstance(right, str):
            raise e.InvalidTypeError('Multiplication requires numeric types', column, line)
        return left * right
    
    def binary_div(self, left, right, column, line):
        if right == 0:
            raise e.DivisionByZeroError(column, line, 'Division by zero is undefined')
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise e.InvalidTypeError('Division requires numeric types', column, line)
        return left / right

    def comparison(self, operator, left, right, column, line):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            pass
        elif isinstance(left, str) and isinstance(right, str):
            if operator == Operators.EQ:
                return left == right
            elif operator == Operators.NEQ:
                return left != right
            raise e.InvalidTypeError('Type str dont know how to work with comparison operators', column, line)
        else:
            raise e.InvalidTypeError(f'Dont know how to comparise this types {type(left)} and {type(right)}', column, line)
        match operator:
            case Operators.EQ:
                return left == right
            case Operators.NEQ:
                return left != right
            case Operators.LESS:
                return left < right
            case Operators.GREATER:
                return left > right
            case Operators.LE:
                return left <= right
            case Operators.GE:
                return left >= right

    def logical_and(self, left, right, column, line):
        if not isinstance(left, bool) or not isinstance(right, bool):
            raise e.InvalidTypeError("Logical AND requires boolean types", column, line)
        return left and right

    def logical_or(self, left, right, column, line):
        if not isinstance(left, bool) or not isinstance(right, bool):
            raise e.InvalidTypeError("Logical OR requires boolean types", column, line)
        return left or right



    def visit_assignment_expression(self, assignment_expression: nodes.AssignmentExpression):
        assignment_expression.identifier.accept(self)
        identifier = self.last_result
        if not self.is_variable(identifier):
            raise e.UndeclaredVariableError(identifier, assignment_expression.column, assignment_expression.line)
        assignment_expression.expression.accept(self)
        new_value = self.last_result
        if eval(self.context_manager.get_variable_type(identifier)) == type(new_value):
            self.context_manager.set_variable_value(identifier, new_value)
        else:
            raise e.TypeMismatchError(identifier, assignment_expression.column, assignment_expression.line)

    def visit_function_call(self, function_call_statement: nodes.FunctionCallStatement):
        if (function_call_statement.identifier in self.context_manager.BUILT_IN or 
            function_call_statement.identifier == 'print'):
            identifier = function_call_statement.identifier
        else:
            if not self.context_manager.is_function_exists(function_call_statement.identifier.name):
                raise e.UndeclaredFunctionError(function_call_statement.identifier, function_call_statement.column, function_call_statement.line)
            function_call_statement.identifier.accept(self)
            identifier = self.last_result
        accepted_arguments = []
        for argument in function_call_statement.arguments:
            argument.accept(self)
            accepted_arguments.append(self.last_result)
        self.execute_function(identifier, accepted_arguments)

    def visit_if_statement(self, if_statement: nodes.IfStatement): 
        if_statement.condition.accept(self)
        condition = self.last_result
        if not isinstance(condition, bool):
            raise e.InvalidConditionError(if_statement.column, if_statement.line, condition)
        if condition:
            if_statement.block.accept(self)
        elif if_statement.else_block:
            if_statement.else_block.accept(self)
        else:
            self.last_result = None

    def visit_while_statement(self, while_statement: nodes.WhileStatement):
        while_statement.condition.accept(self)
        condition = self.last_result
        if not isinstance(condition, bool):
            raise e.InvalidConditionError(while_statement.column, while_statement.line, condition)
        if condition:
            while condition:
                while_statement.block.accept(self)
                while_statement.condition.accept(self)
                condition = self.last_result
        else:  
            self.last_result = None

    def visit_declaration_statement(self, declaration: nodes.DeclarationStatement):
        declaration.variable_type.accept(self)
        variable_type = self.last_result
        identifier = declaration.identifier
        if declaration.expression:
            declaration.expression.accept(self)
            value = self.last_result
        else:
            if variable_type == 'int':
                value = 0
            elif variable_type == 'float':
                value = 0.0
            elif variable_type == 'string':
                value = ''
            elif variable_type == 'bool':
                value = False
        if self.context_manager.is_variable_exists_in_current_context(identifier):
            raise e.RedefinitionError(identifier, declaration.column, declaration.line)
        self.context_manager.add_variable(identifier, value, variable_type)

    def visit_return_statement(self, return_statement: nodes.ReturnStatement):
        return_statement.expression.accept(self)


    def visit_block(self, block: nodes.Block):
        for statement in block.statements:
            if isinstance(statement, nodes.ReturnStatement):
                statement.accept(self)
                self.context_manager.set_return_value(self.last_result)
            if self.context_manager.get_return_value() is not None:
                self.last_result = self.context_manager.get_return_value()
                return
            else:
                statement.accept(self)
        if self.context_manager.get_return_value() is not None:
            self.last_result = self.context_manager.get_return_value()

    def visit_function(self, function: nodes.Function):
        if function.block.statements:
            function.block.accept(self)

    def visit_program(self, program: nodes.Program):
        main_function = None
        for function in program.functions:
            if (function.identifier == 'main' and function.function_type.type == 'int' and
               function.parameters == []):
                if main_function:
                    raise e.RedefinitionError(function.identifier)
                main_function = function
            elif function.identifier == 'print':
                raise e.RedefinitionError(function.identifier)
            elif not self.context_manager.is_function_exists(function.identifier):
                self.context_manager.add_function(function)
            else:
                raise e.RedefinitionError(function.identifier)
        if not main_function:
            raise e.MainFunctionNotFoundError()
        else:
            self.context_manager.add_function(main_function)
            self.context_manager.enter_context(main_function.identifier)
            self.execute_function(main_function.identifier, [])

    def execute_print(self, arguments):
        if len(arguments) != 1:
            raise e.InvalidNumberOfArgumentsError('print')
        if self.is_variable(arguments[0]):
            print(self.context_manager.get_variable_value(arguments[0]))
        else:
            print(arguments[0])

    def create_list(self, arguments):
        if arguments:
            self.last_result = c.List(arguments)
        else:
            self.last_result = c.List()

    def create_collection(self, arguments):
        if arguments:
            new_arguments = []
            for argument in arguments:
                if self.context_manager.is_variable_exists_in_current_context(argument):
                    argument = self.context_manager.get_variable_value(argument)
                if not isinstance(argument, c.Polyhedron):
                    raise e.InvalidTypeError("Collection can only contains Polyhedrons")
                new_arguments.append(argument)
            self.last_result = c.Collection(new_arguments)
        else:
            self.last_result = c.Collection()

    def create_polyhedron(self, arguments):
        if arguments:
            new_arguments = []
            for argument in arguments:
                if self.context_manager.is_variable_exists_in_current_context(argument):
                    argument = self.context_manager.get_variable_value(argument)
                    if not isinstance(argument, c.Line):
                        raise e.InvalidTypeError("Polyhedron can only be created from Lines")
                    new_arguments.append(argument)
                elif not isinstance(argument, c.Line):
                    raise e.InvalidTypeError("Polyhedron can only be created from Lines")
                else:
                    new_arguments.append(argument)
            polyhedron = c.Polyhedron(new_arguments)
            points = polyhedron.points()
            for point in points:
                occurence = 0
                for line in polyhedron.lines():
                    if point.x == line.start.x and point.y == line.start.y and point.z == line.start.z:
                        occurence += 1
                    if point.x == line.end.x and point.y == line.end.y and point.z == line.end.z:
                        occurence += 1
                if occurence < 3:
                    message = "In order to create polyhedron, each point must "
                    raise e.InvalidTypeError(message + "connected to at least 3 lines")
            self.last_result = polyhedron
        else:
            raise e.InvalidNumberOfArgumentsError('Polyhedron')

    def create_line(self, arguments):
        if len(arguments) != 2:
            raise e.InvalidNumberOfArgumentsError('Line')
        new_arguments = []
        for argument in arguments:
            if self.is_variable(argument):
                argument = self.context_manager.get_variable_value(argument)
            if not isinstance(argument, c.Point):
                raise e.InvalidTypeError("Line can only be created from Points")
            new_arguments.append(argument)
        self.last_result = c.Line(new_arguments[0], new_arguments[1])

    def create_point(self, arguments):
        if len(arguments) != 3:
            raise e.InvalidNumberOfArgumentsError('Point')
        new_arguments = []
        for argument in arguments:
            if self.is_variable(argument):
                argument_type = self.context_manager.get_variable_type(argument)
                argument = self.context_manager.get_variable_value(argument)
                if argument_type not in ['int', 'float']:
                    raise e.InvalidTypeError("Point arguments must be 'int' or 'float'")
            elif not isinstance(argument, (int, float)):
                raise e.InvalidTypeError("Point arguments must be 'int' or 'float'")
            new_arguments.append(argument)
        self.last_result = c.Point(new_arguments[0], new_arguments[1], new_arguments[2])
                   

    def execute_builtin_function(self, function_name: str, arguments: list):
        if function_name == 'print':
            self.execute_print(arguments)
            self.last_result = None
        elif function_name == 'List':
            self.create_list(arguments)
        elif function_name == 'Collection':
            self.create_collection(arguments)
        elif function_name == 'Polyhedron':
            self.create_polyhedron(arguments)
        elif function_name == 'Line':
            self.create_line(arguments)
        elif function_name == 'Point':
            self.create_point(arguments)
        else:
            raise e.UndeclaredFunctionError(function_name)

    def execute_user_function(self, function_name: str, arguments: list):
        self.context_manager.enter_context(function_name)
        function = self.context_manager.get_function(function_name)
        if len(function.parameters) != len(arguments):
            raise e.InvalidNumberOfArgumentsError(function_name)
        for parameter, argument in zip(function.parameters, arguments):
            name = parameter.identifier
            parameter.type.accept(self)
            parameter_type = self.last_result
            if self.is_variable(argument):
                value = self.context_manager.get_variable_value(argument)
            else:
                value = argument
            if eval(parameter_type) != type(value):
                raise e.TypeMismatchError(parameter.identifier, function.column, function.line)
            self.context_manager.add_variable(name, value, parameter_type)
        function.block.accept(self)
        return_value = self.last_result
        if self.is_variable(return_value):
            return_value = self.context_manager.get_variable_value(return_value)
        if function.function_type.type == 'void':
            if return_value is not None:
                raise e.InvalidReturnTypeError(function.function_type.type, type(return_value), function.function_type.column, function.function_type.line)
        elif function.function_type.type in self.context_manager.BUILT_IN.keys():
            if not return_value.__class__.__name__ == function.function_type.type:
                raise e.InvalidReturnTypeError(function.function_type.type, type(return_value), function.function_type.column, function.function_type.line)
        elif eval(function.function_type.type) != type(return_value):
            raise e.InvalidReturnTypeError(function.function_type.type, type(return_value), function.function_type.column, function.function_type.line)
        self.context_manager.exit_context()
        self.last_result = return_value

    def execute_main_function(self, function_name: str):
        function = self.context_manager.get_function(function_name)
        function.block.accept(self)
        return_value = self.last_result
        if self.is_variable(return_value):
            return_value = self.context_manager.get_variable_value(return_value)
        if function.function_type.type == 'void' and return_value is not None:
            raise e.InvalidReturnTypeError(function.function_type.type, type(return_value), function.function_type.column, function.function_type.line)
        elif eval(function.function_type.type) != type(return_value):
            raise e.InvalidReturnTypeError(function.function_type.type, type(return_value), function.function_type.column, function.function_type.line)
        self.context_manager.exit_context()
        self.last_result = return_value

    def execute_function(self, function_name: str, arguments: list):
        if function_name in self.context_manager.BUILT_IN.keys() or function_name == 'print':
            self.execute_builtin_function(function_name, arguments)
        elif function_name == 'main':
            self.execute_main_function(function_name)
        else:
            self.execute_user_function(function_name, arguments)


    def execute_method(self, name, method_name: str, arguments: list):
        argument_values = []
        for argument in arguments:
            if self.is_variable(argument):
                argument_values.append(self.context_manager.get_variable_value(argument))
            else:
                argument_values.append(argument)
        if self.context_manager.is_variable_exists(name):
            value = self.context_manager.get_variable_value(name)
            var_type = self.context_manager.get_variable_type(name)
            if var_type in self.context_manager.BUILT_IN:
                for method in self.context_manager.BUILT_IN[var_type]:
                    if method_name == method:
                        if method_name in ['lines', 'points']:
                            self.last_result = c.List(getattr(value, method_name)(*argument_values))
                        else:
                            self.last_result = getattr(value, method_name)(*argument_values)
                        return
                raise e.InvalidMethodCallError(var_type, method_name)
        elif name.__class__.__name__ in self.context_manager.BUILT_IN:
            for method in self.context_manager.BUILT_IN[name.__class__.__name__]:
                if method_name == method:
                    if method_name in ['lines', 'points']:
                        self.last_result = c.List(getattr(name, method_name)(*argument_values))
                    else:
                        self.last_result = getattr(name, method_name)(*argument_values)
                    return
            raise e.InvalidMethodCallError(name.__class__.__name__, method_name)
        else:
            raise e.UndeclaredVariableError(name)

