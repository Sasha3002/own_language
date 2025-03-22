from lexer.lexer import Lexer
from lexer.tokens import TokenType, Token
from errors.errors import InvalidSyntaxError
import parser.nodes as nodes
from enum import Enum, auto

class Operators(Enum):
    OR = auto()
    AND = auto()
    EQ = auto()
    NEQ = auto()
    LESS = auto()
    GREATER = auto()
    LE = auto()
    GE = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    NOT = auto()


OPERATORS = {
    TokenType.OR: Operators.OR,
    TokenType.AND: Operators.AND,
    TokenType.EQ: Operators.EQ,
    TokenType.NEQ: Operators.NEQ,
    TokenType.LESS: Operators.LESS,
    TokenType.GREATER: Operators.GREATER,
    TokenType.LE: Operators.LE,
    TokenType.GE: Operators.GE,
    TokenType.PLUS: Operators.PLUS,
    TokenType.MINUS: Operators.MINUS,
    TokenType.MUL: Operators.MUL,
    TokenType.DIV: Operators.DIV,
    TokenType.NOT: Operators.NOT
}



class Parser:
    VARIABLE_TOKENS = [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING,
                       TokenType.LIST, TokenType.POINT, TokenType.LINE, TokenType.POLYHEDRON,
                       TokenType.COLLECTION]
    COMPLEX_VARIABLE_TOKENS = [TokenType.LIST, TokenType.POINT, TokenType.LINE,
                               TokenType.POLYHEDRON, TokenType.COLLECTION]
    COMPARISON_TOKENS = [TokenType.EQ, TokenType.NEQ, TokenType.LE, TokenType.GE,
                         TokenType.GREATER, TokenType.LESS]

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def get_current_token_type(self) -> TokenType:
        return self.current_token.type

    def get_current_token_value(self):
        return self.current_token.value

    def consume(self) -> Token:
        self.current_token = self.lexer.get_next_token()
        while self.get_current_token_type() == TokenType.COMMENT:
            self.current_token = self.lexer.get_next_token()
        return self.current_token
    
    def get_value_and_consume(self):
        if not self.token_or_null(TokenType.IDENTIFIER):
            return None
        else:
            value = self.get_current_token_value()
            self.consume()
            return value

    def consume_if_token(self, token_type: TokenType):
        if self.get_current_token_type() != token_type:
            return False
        else:
            self.consume()
            return True


    def token_or_null(self, token_types: TokenType):
        if self.get_current_token_type() != token_types:
            return False
        else:
            return True

    def tokens_or_null(self, token_types: list[TokenType]):
        if self.get_current_token_type() not in token_types:
            return False
        else:
            return True


    def require_token(self, token_type: TokenType, message) -> bool:
        if self.get_current_token_type() != token_type:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     f"{message}. Expected {token_type}, got {self.get_current_token_type()}") 
        return True

    def require_tokens(self, token_types: list[TokenType], message) -> bool:
        if self.get_current_token_type() not in token_types:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     f"{message}. Expected one of {token_types}, got {self.get_current_token_type()}")
        return True

    def require_token_and_consume(self, token_type: TokenType, message) -> None:
        self.require_token(token_type, message)
        self.consume()

    def parse_program(self) -> nodes.Program:
        functions = []
        while fundef := self.parse_function():
            functions.append(fundef) 
        self.require_token(TokenType.EOF, 'Need EOF at the end of stream')
        return nodes.Program(functions)

    def parse_function(self) -> nodes.Function:
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        function_type = self.parse_function_type()
        if function_type == None:
            return None
        #self.require_token(TokenType.IDENTIFIER, 'Was function type but didnt get name')
        # name = self.get_current_token_value()
        name = self.get_value_and_consume()
        if name == None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Was function type but didnt get name")
        self.require_token_and_consume(TokenType.LPAREN, 'You need to open paren before function parametrs')
        parameters = self.parse_function_parameters()
        self.require_token_and_consume(TokenType.RPAREN, 'You need to close paren after function parametrs')
        block = self.parse_block()
        if block == None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Tried to build function block but got None")
        return nodes.Function(function_type, name, parameters, block, column, line)



    def parse_function_type(self) -> nodes.FunctionType:
        if not self.tokens_or_null(self.VARIABLE_TOKENS + [TokenType.VOID]):
            return None
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        type = self.get_current_token_value()
        self.consume()
        return nodes.FunctionType(type, column, line)

    def parse_variable_type(self) -> nodes.VariableType:
        if not self.tokens_or_null(self.VARIABLE_TOKENS):
            return None
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        type = self.get_current_token_value()
        self.consume()
        return nodes.VariableType(type, column, line)
    
    def parse_variable_tokens(self):
        if not self.tokens_or_null(self.COMPLEX_VARIABLE_TOKENS):
            return None
        identifier = self.get_current_token_value()
        self.consume()
        return identifier
        #return nodes.Identifier(identifier, column, line)

    def parse_identifier(self) -> nodes.Identifier:
        if not self.token_or_null(TokenType.IDENTIFIER):
            return None
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        identifier = self.get_current_token_value()
        self.consume()
        return nodes.Identifier(identifier, column, line)

    def parse_function_parameters(self) -> list[nodes.Parameter]:
        parameters = []
        parameter = self.parse_function_parameter()
        if parameter == None:
            return parameters
        parameters.append(parameter)
        while self.consume_if_token(TokenType.COMMA):
            if parameter := self.parse_function_parameter():
                parameters.append(parameter)
            else:
                raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Was \',\' in function parameters but didnt get parametr after it")    
        return parameters


    def parse_function_parameter(self) -> nodes.Parameter:
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        type = self.parse_variable_type()
        if type == None:
            return None
        identifier = self.get_value_and_consume()
        if identifier == None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Tried to build function parameter but didnt get name")
        return nodes.Parameter(type, identifier, column, line)

    def parse_block(self) -> nodes.Block:
        if not self.consume_if_token(TokenType.LBRACE):
            return None
        statements = []
        while statement:= self.parse_statement():
            statements.append(statement)
        self.require_token_and_consume(TokenType.RBRACE, 'You need to close Block')
        return nodes.Block(statements)


    def parse_statement(self):
        return self.parse_return_statement() or self.parse_if_statement() or self.parse_while_statement() or self.parse_declaration_statement() or self.parse_identifier_statements()

    def parse_identifier_statements(self):
        identifier = self.parse_identifier()
        if identifier is None: 
            return None
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if method_call:= self.parse_method_call_statement(identifier):
            self.require_token_and_consume(TokenType.SEMI, 'You need to close method call by \';\'')
            return method_call
        elif expression := self.parse_assigment():
            self.require_token_and_consume(TokenType.SEMI, 'You need to close assignment statement by \';\'')
            return nodes.AssignmentExpression(identifier, expression, column, line)
        elif funcall := self.parse_function_call_statement(identifier):
            return funcall
        
    def parse_assigment(self):
        if not self.consume_if_token(TokenType.ASSIGN):
            return None
        expression = self.parse_expression()
        if expression is None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     'Was assigment operator but didnt get expression')
        return expression
        

    def parse_return_statement(self) -> nodes.ReturnStatement:
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if not self.consume_if_token(TokenType.RETURN):
            return None
        expression = self.parse_expression()
        self.require_token_and_consume(TokenType.SEMI, 'You need to close return statement by \';\'')
        return nodes.ReturnStatement(expression, column, line)
    

    def parse_if_statement(self) -> nodes.IfStatement:
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if not self.consume_if_token(TokenType.IF):
            return None
        self.require_token_and_consume(TokenType.LPAREN, "Must be open paren for If condition")
        condition = self.parse_expression()
        if condition == None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Condition for if statement is None")
        self.require_token_and_consume(TokenType.RPAREN, "Must be close paren for If condition")
        block = self.parse_block()
        if block == None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Block for if statement is None")
        if self.consume_if_token(TokenType.ELSE):
            else_block = self.parse_block()
            if else_block == None:
                raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Was else but else_block for if statement is None")
            return nodes.IfStatement(condition, block, column, line, else_block)
        return nodes.IfStatement(condition, block, column, line)


    def parse_while_statement(self) -> nodes.WhileStatement:
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if not self.consume_if_token(TokenType.WHILE):
            return None
        self.require_token_and_consume(TokenType.LPAREN, "Must be open paren for While condition")
        condition = self.parse_expression()
        if condition == None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Condition for while statement is None")
        self.require_token_and_consume(TokenType.RPAREN, "Must be close paren for While condition")
        block = self.parse_block()
        if block == None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Block for while statement is None")
        return nodes.WhileStatement(condition, block, column, line)

    def parse_declaration_statement(self) -> nodes.DeclarationStatement:
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        type = self.parse_variable_type()
        if type == None:
            return None
        identifier = self.get_value_and_consume()
        if identifier == None:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Must be identifier after type in declaration statement")
        if self.consume_if_token(TokenType.ASSIGN):
            expression = self.parse_expression()
            if expression is None:
                raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Was assign operator but didnt get any expression")
            self.require_token_and_consume(TokenType.SEMI, 'You need to close declaration statement by \';\'')
            return nodes.DeclarationStatement(type, identifier, column, line, expression)
        self.require_token_and_consume(TokenType.SEMI, 'You need to close declaration statement by \';\'')
        return nodes.DeclarationStatement(type, identifier, column, line)

    def parse_method_call_statement(self, caller: nodes.Identifier):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if not self.token_or_null(TokenType.DOT):
            return None
        method_calls = []
        while self.consume_if_token(TokenType.DOT):
            identifier = self.parse_identifier()
            if identifier == None:
                raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "'After dot in method call must be Identifier")
            self.require_token_and_consume(TokenType.LPAREN, 'Must be \'( \' in call arguments')
            arguments = []
            if argument := self.parse_call_arguments():
                arguments = argument
            self.require_token_and_consume(TokenType.RPAREN, 'Must be \') \' in call arguments')
            method_calls.append(nodes.MethodCall(identifier, column, line, arguments))
        return nodes.MethodCallExpression(caller, method_calls, column, line)

    def parse_function_call_statement(self, identifier: nodes.Identifier): #(self, name:str)
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if not self.consume_if_token(TokenType.LPAREN):
            return None
        arguments = []
        if argument := self.parse_call_arguments():
                arguments = argument
        self.require_token_and_consume(TokenType.RPAREN, 'Must be \') \' in function call')
        self.require_token_and_consume(TokenType.SEMI, 'Must be \'; \' at the end of function call')
        return nodes.FunctionCallStatement(identifier, arguments, column, line)

    def parse_call_arguments(self) -> list:
        arguments = []
        if argument:= self.parse_expression():
            arguments.append(argument)
            while self.consume_if_token(TokenType.COMMA):
                arguments.append(self.parse_expression())
        return arguments

    def parse_expression(self):
        return self.parse_or_expression()


    def parse_or_expression(self):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        left = self.parse_and_expression()
        if left is None:
            return None
        while self.get_current_token_type() == TokenType.OR:
            operator = OPERATORS[self.get_current_token_type()]
            self.consume()
            right = self.parse_and_expression()
            if right is None:
                raise InvalidSyntaxError(
                    self.current_token.pos[0], self.current_token.pos[1],
                    "Expected expression after 'or' operator."
                )
            left = nodes.BinaryExpression(left, operator, right, column, line)
        return left

    def parse_and_expression(self):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        left = self.parse_comparison_expression()
        if left is None:
            return None
        while self.get_current_token_type() == TokenType.AND:
            operator = OPERATORS[self.get_current_token_type()]
            self.consume()
            right = self.parse_comparison_expression()
            if right is None:
                raise InvalidSyntaxError(
                    self.current_token.pos[0], self.current_token.pos[1],
                    "Expected expression after 'and' operator."
                )
            left = nodes.BinaryExpression(left, operator, right, column, line)
        return left

    def parse_comparison_expression(self):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        left = self.parse_additive_expression()
        if left is None:
            return None
        while self.get_current_token_type() in self.COMPARISON_TOKENS:
            operator = OPERATORS[self.get_current_token_type()]
            self.consume()
            right = self.parse_additive_expression()
            if right is None:
                raise InvalidSyntaxError(
                    self.current_token.pos[0], self.current_token.pos[1],
                    "Expected expression after comparison operator."
                )
            left = nodes.BinaryExpression(left, operator, right, column, line)
        return left

    def parse_additive_expression(self):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        left = self.parse_multiplicative_expression()
        if left is None:
            return None
        while self.get_current_token_type() in [TokenType.PLUS, TokenType.MINUS]:
            operator = OPERATORS[self.get_current_token_type()]
            self.consume()
            right = self.parse_multiplicative_expression()
            if right is None:
                raise InvalidSyntaxError(
                    self.current_token.pos[0], self.current_token.pos[1],
                    "Expected expression after additive operator."
                )
            left = nodes.BinaryExpression(left, operator, right, column, line)
        return left

    def parse_multiplicative_expression(self):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        left = self.parse_negation_expression()
        if left is None:
            return None
        while self.get_current_token_type() in [TokenType.MUL, TokenType.DIV]:
            operator = OPERATORS[self.get_current_token_type()]
            self.consume()
            right = self.parse_negation_expression()
            if right is None:
                raise InvalidSyntaxError(
                    self.current_token.pos[0], self.current_token.pos[1],
                    "Expected expression after multiplicative operator."
                )
            left = nodes.BinaryExpression(left, operator, right, column, line)
        return left


    def parse_negation_expression(self):
        negated = False
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if self.get_current_token_type() in [TokenType.NOT, TokenType.MINUS]:
            operator = OPERATORS[self.get_current_token_type()]
            self.consume()
            negated = True
        expression = self.parse_factor()
        if negated:
            if expression is None:
                raise InvalidSyntaxError(
                    self.current_token.pos[0], self.current_token.pos[1],
                    "Expected expression after negation operator."
                )
            return nodes.NegationExpression(operator, expression, column, line)
        return expression

    def parse_factor(self):
        expression = self.parse_literal()
        if expression is not None:
            return expression
        elif self.consume_if_token(TokenType.LPAREN):
            if expression := self.parse_expression():
                self.require_token_and_consume(TokenType.RPAREN, 'You need to close RPAREN in expression')
                return expression
            else:
                raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "as")
        elif meth_func_ident :=  self.meth_func_ident():
            return meth_func_ident
        else:
            return None


    def meth_func_ident(self):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        ident_or_call = self.parse_identifier_or_call()
        references = []
        while self.consume_if_token(TokenType.DOT):
            if identifier_call := self.parse_identifier_or_call():
                if isinstance(identifier_call,nodes.FunctionCallStatement):  # nie potrz references.append(identifier_call)
                    references.append(nodes.MethodCall(identifier_call.identifier, column, line, identifier_call.arguments))
                else:
                    references.append(nodes.MethodCall(identifier_call, column, line))
            else:
                raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                    "Was \'.\' but after it didnt get any identifier or call")
        if references:
            return nodes.MethodCallExpression(ident_or_call, references, column, line)
        else:
            return ident_or_call
    def parse_identifier_or_call(self):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if identifier := (self.parse_identifier() or self.parse_variable_tokens()):
            if not self.consume_if_token(TokenType.LPAREN):
                return identifier
            arguments = []
            if argument:= self.parse_call_arguments():
                arguments = argument
            self.require_token_and_consume(TokenType.RPAREN, 'You need to close RPAREN in function call')
            return nodes.FunctionCallStatement(identifier, arguments, column, line)
        else:
            return None

    def parse_literal(self):
        column = self.current_token.pos[0]
        line = self.current_token.pos[1]
        if self.get_current_token_type() == TokenType.INT_VALUE:
            value = self.get_current_token_value()
            self.consume()
            return nodes.IntValue(value, column, line)
        elif self.get_current_token_type() == TokenType.FLOAT_VALUE:
            value = self.get_current_token_value()
            self.consume()
            return nodes.FloatValue(value, column, line)
        elif self.get_current_token_type() == TokenType.STRING_VALUE:
            value = self.get_current_token_value()
            self.consume()
            return nodes.StringValue(value, column, line)
        elif self.get_current_token_type() in [TokenType.TRUE, TokenType.FALSE]:
            value = self.get_current_token_value()
            if value == "True":
                value = True
            else:
                value = False
            self.consume()
            return nodes.BoolValue(value, column, line)
        else:
            return None
