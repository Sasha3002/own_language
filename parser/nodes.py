from abc import ABC, abstractmethod


tree_depth = 0


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Identifier(Node):
    def __init__(self, name: str, column, line):
        self.name = name
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_identifier(self)

    def __repr__(self) -> str:
        return f"IdentifierName = {self.name}"


class BoolValue(Node):
    def __init__(self, value: bool, column, line):
        self.value = value
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_bool_value(self)

    def __repr__(self) -> str:
        return f"BoolValue = {self.value}"


class IntValue(Node):
    def __init__(self, value: int, column, line):
        self.value = value
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_int_value(self)

    def __repr__(self) -> str:
        return f"IntValue = {self.value}"


class FloatValue(Node):
    def __init__(self, value: float, column, line):
        self.value = value
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_float_value(self)

    def __repr__(self) -> str:
        return f"FloatValue = {self.value}"


class StringValue(Node):
    def __init__(self, value: str, column, line):
        self.value = value
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_string_value(self)

    def __repr__(self) -> str:
        return f"StringValue = \"{self.value}\""


class FunctionType(Node):
    def __init__(self, type: str, column, line):
        self.type = type
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_function_type(self)

    def __repr__(self) -> str:
        return f"FunctionType = {self.type}"


class VariableType(Node):
    def __init__(self, type: str, column, line):
        self.type = type
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_variable_type(self)

    def __repr__(self) -> str:
        return f"VariableType = {self.type}"


class Parameter(Node):
    def __init__(self, type: VariableType, identifier: str, column, line): #string a nie Identifier
        self.identifier = identifier
        self.type = type
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_parameter(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"Parameter: VariableName = {self.identifier}, {self.type}"
        tree_depth -= 3
        return r


class AssignmentExpression(Node):
    def __init__(self, identifier: Identifier, expression, column, line):
        self.identifier = identifier
        self.expression = expression
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_assignment_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} AssignmentExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Identifier: {self.identifier}"
        r += f"\n{' ' * tree_depth} Expression: {self.expression}"
        tree_depth -= 6
        return r


class BinaryExpression(Node):
    def __init__(self, left, operator: str, right, column, line):
        self.left = left
        self.operator = operator
        self.right = right
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_binary_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} BinaryExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} LeftOperand: {self.left}"
        r += f"\n{' ' * tree_depth} Operator: {self.operator}"
        r += f"\n{' ' * tree_depth} RightOperand: {self.right}"
        tree_depth -= 6
        return r

class NegationExpression(Node):
    def __init__(self, operator, expression, column, line):
        self.operator = operator
        self.expression = expression
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_negation_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} NegationExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Operand: {self.operator}"
        tree_depth -= 6
        return r


class MethodCall(Node):
    #def __init__(self, name: Identifier, arguments: list):
    #    self.name = name
    #    self.arguments = arguments

    def __init__(self, name: Identifier, column, line, arguments = None):
        self.name = name
        self.arguments = arguments
        self.column = column
        self.line = line

    def accept(self, visitor, caller):
        visitor.visit_method_call(self, caller)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} MethodCall:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} MethodName: {self.name}"
        r += f"\n{' ' * tree_depth} Arguments:"
        tree_depth += 3
        if self.arguments != None:
            for argument in self.arguments:
                r += f"\n{' ' * tree_depth} Argument: {argument}"
        else:
            r += f"\n{' ' * tree_depth} Argument: None"
        tree_depth -= 9
        return r



class MethodCallExpression(Node):
    def __init__(self, caller: Identifier, methods: list[MethodCall], column, line):
        self.caller = caller
        self.methods = methods
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_method_call_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} MethodCallExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Caller: {self.caller}"
        r += f"\n{' ' * tree_depth} Methods: {self.methods}"
        tree_depth -= 6
        return r


class FunctionCallStatement(Node):
    def __init__(self, identifier: Identifier, arguments: list, column, line):
        self.identifier = identifier
        self.arguments = arguments
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_function_call(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} FunctionCallStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} FunctionName: {self.identifier}"
        r += f"\n{' ' * tree_depth} Arguments:"
        tree_depth += 3
        for argument in self.arguments:
            r += f"\n{' ' * tree_depth} Argument: {argument}"
        tree_depth -= 9
        return r


class Block(Node):
    def __init__(self, statements: list):
        self.statements = statements

    def accept(self, visitor):
        visitor.visit_block(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} Block:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Statements:"
        tree_depth += 3
        for statement in self.statements:
            r += f"\n{' ' * tree_depth} Statement: {statement}"
        tree_depth -= 9
        return r


class IfStatement(Node):
    def __init__(self, condition, block: Block, column, line, else_block=None):
        self.condition = condition
        self.block = block
        self.else_block = else_block
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_if_statement(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} IfStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Condition: {self.condition}"
        r += f"\n{' ' * tree_depth} IfBlock:"
        r += f"{' ' * tree_depth} {self.block}"
        r += f"\n{' ' * tree_depth} ElseBlock:"
        if self.else_block is None:
            r += f"\n{' ' * (tree_depth + 3)} None"
        else:
            r += f"{' ' * tree_depth} {self.else_block}"
        tree_depth -= 6
        return r


class WhileStatement(Node):
    def __init__(self, condition, block: Block, column, line):
        self.condition = condition
        self.block = block
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_while_statement(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} WhileStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Condition: {self.condition}"
        r += f"\n{' ' * tree_depth} WhileBlock:"
        r += f"{' ' * tree_depth} {self.block}"
        tree_depth -= 6
        return r


class DeclarationStatement(Node):
    def __init__(self, variable_type: VariableType, identifier: str, column, line, expression=None): #################################
        self.variable_type = variable_type
        self.identifier = identifier
        self.expression = expression
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_declaration_statement(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} DeclarationStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} {self.variable_type}"
        r += f"\n{' ' * tree_depth} VariableName = {self.identifier}"
        r += f"\n{' ' * tree_depth} DeclarationExpression: {self.expression}"
        tree_depth -= 6
        return r


class ReturnStatement(Node):
    def __init__(self, expression, column, line):
        self.expression = expression
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_return_statement(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} ReturnStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} ReturnExpression: {self.expression}"
        tree_depth -= 6
        return r


class Function(Node):
    def __init__(self, function_type: FunctionType, identifier: str,#Identifier, #identifier: str
                 parameters: list, block: Block, column, line):
        self.function_type = function_type
        self.identifier = identifier
        self.parameters = parameters
        self.block = block
        self.column = column
        self.line = line

    def accept(self, visitor):
        visitor.visit_function(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} Function:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} FunctionName: {self.identifier}"
        r += f"\n{' ' * tree_depth} FunctionType: {self.function_type}"
        r += f"\n{' ' * tree_depth} Parameters:"
        tree_depth += 3
        for parameter in self.parameters:
            r += f"\n{' ' * tree_depth} {parameter}"
        tree_depth -= 6
        r += f"{' ' * tree_depth} {self.block}"
        tree_depth -= 3
        return r


class Program(Node):
    def __init__(self, functions: list):
        self.functions = functions

    def accept(self, visitor):
        visitor.visit_program(self)

    def __repr__(self) -> str:
        return f"Program:{self.functions}"
    


class MainVisitor(ABC):
    @abstractmethod
    def visit_identifier(self, node):
        pass

    @abstractmethod
    def visit_block(self, block):
        pass

    @abstractmethod
    def visit_bool_value(self, node):
        pass

    @abstractmethod
    def visit_int_value(self, node):
        pass

    @abstractmethod
    def visit_float_value(self, node):
        pass

    @abstractmethod
    def visit_string_value(self, node):
        pass

    @abstractmethod
    def visit_function_type(self, node):
        pass

    @abstractmethod
    def visit_variable_type(self, node):
        pass

    @abstractmethod
    def visit_parameter(self, node):
        pass

    @abstractmethod
    def visit_assignment_expression(self, node):
        pass

    @abstractmethod
    def visit_binary_expression(self, node):
        pass

    @abstractmethod
    def visit_negation_expression(self, node):
        pass

    @abstractmethod
    def visit_method_call(self, node):
        pass

    @abstractmethod
    def visit_method_call_expression(self, node):
        pass

    @abstractmethod
    def visit_function_call(self, node):
        pass

    @abstractmethod
    def visit_block(self, node):
        pass

    @abstractmethod
    def visit_if_statement(self, node):
        pass

    @abstractmethod
    def visit_while_statement(self, node):
        pass

    @abstractmethod
    def visit_declaration_statement(self, node):
        pass

    @abstractmethod
    def visit_return_statement(self, node):
        pass

    @abstractmethod
    def visit_function(self, node):
        pass

    @abstractmethod
    def visit_program(self, node):
        pass


