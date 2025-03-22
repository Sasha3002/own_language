

class InvalidTokenError(Exception):
    """Exception raised when lexer meets invalid token
    """

    def __init__(self, column, line, char):
        text = f'Error occured in line {line}, column {column}: \nInvalid character \'{char}\''
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ExceedsMaxLengthError(Exception):
    """Exception raised when created number or string is too long
    """

    def __init__(self, column, line, message=""):
        text = f'Error occured in line {line}, column {column}: \n{message} exceeds max length'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message

class UndefEscapeChar(Exception):
    def __init__(self, column, line, char):
        text = f'Error occured in line {line}, column {column}: \nInvalid character \'{char}\''
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message
    

class InvalidSyntaxError(Exception):
    """Exception raised when parser meets invalid syntax
    """

    def __init__(self, column, line, message=""):
        text = f'Error occured in line {line}, column {column}: \nInvalid syntax: ' + message
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message
    
class MainFunctionNotFoundError(Exception):
    """Exception raised when visitor doesn't find main function
    """

    def __init__(self):
        self.message = "Main function not found"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class RedefinitionError(Exception):
    """Exception raised when visitor finds redefinition of variable or function
    """

    def __init__(self, message="", column = None, line = None):
        if column is not None:
            text = f'Redefinition oocured in line {line}, column {column}: \n\'{message}\' already exists'
        else:
            text = f'Redefinition oocured: \n\'{message}\' already exists'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UndeclaredVariableError(Exception):
    """Exception raised when visitor finds undeclared variable
    """

    def __init__(self, message="", column = None, line = None):
        if column is not None:
            text = f'Variable undeclared in line {line}, column {column}: \nVariable \'{message}\' is not declared'
        else:
            text = f'Variable undeclared: \nVariable \'{message}\' is not declared'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UndeclaredFunctionError(Exception):
    """Exception raised when visitor finds undeclared function
    """

    def __init__(self, message="", column = None, line = None):
        if column is not None:
            text = f'Function undeclared in line {line}, column {column}: \nFunction \'{message}\' is not declared'
        else:
            text = f'Function undeclared: \nFunction \'{message}\' is not declared'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidConditionError(Exception):
    """Exception raised when visitor finds invalid condition
    """

    def __init__(self, column, line, message=""):
        text = f'Invalid condition in line {line}, column {column}: \n\'{message}\' is not a valid bool-type condition'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class TypeMismatchError(Exception):
    """Exception raised when visitor finds type mismatch
    """

    def __init__(self, message="", column = None, line = None):
        if column is not None:
            text = f'Type mismatch in line {line}, column {column}: \n{message} is not a valid type'
        else:
            text = f'Type mismatch: \n{message} is not a valid type'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidNumberOfArgumentsError(Exception):
    """Exception raised when visitor finds invalid number of arguments
    """

    def __init__(self, message=""):
        text = f'Invalid number of arguments: \nFunction \'{message}\' called with invalid number of arguments'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidMethodCallError(Exception):
    """Exception raised when visitor finds invalid method call
    """

    def __init__(self, object, method_name):
        text = f'Invalid method call: \nYou cannot call method \'{method_name}\' on object of type \'{object}\''
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidReturnTypeError(Exception):
    """Exception raised when visitor finds invalid return type
    """

    def __init__(self, expected_type, return_type, column, line):
        text = f'Invalid return type in line {line}, column {column}: \nExxpected type \'{expected_type}\', got \'{return_type}\''
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidTypeError(Exception):
    """Exception raised when visitor finds invalid type
    """

    def __init__(self, message="", column = None, line = None):
        if column is not None:
            text = f'Invalid type in line {line}, column {column}: \n{message}'
        else:
            text = f'Invalid type: \n{message}'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message
    

class DivisionByZeroError(Exception):
    """Exception raised when visitor find Division By Zero
    """

    def __init__(self,column, line, message=""):
        text = f'Division By Zero in line {line}, column {column}: \n{message}'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message

