from lexer.lexer import Lexer
from lexer.source import Source
from parser.parser import Parser
from interpreter.visitor import Visitor


class Interpreter:
    def __init__(self, source):
        self.data = Source(source)  
        self.lexer = Lexer(self.data)
        self.parser = Parser(self.lexer)
        self.visitor = Visitor()


    def run(self):
        program = self.parser.parse_program()
        program.accept(self.visitor)
        return self.visitor.last_result
