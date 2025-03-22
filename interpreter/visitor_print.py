#class VisitorPrint(ProgramVisitor):
#    def visit_program(self, program):
#        for function in program.functions:
#            self.indent += 1
#            function.accept(self)
#            self.indent -= 1
#    def __init__(self):
#        self.indent = 0
#
#    def visit_function(self,function):
#        self.indent += 1

class PrintVisitor:
    def __init__(self):
        self.indentation = 0

    def indent(self):
        return ' ' * self.indentation

    def visit_identifier(self, node):
        print(f"{self.indent()}Identifier: {node.name}")

    def visit_bool_value(self, node):
        print(f"{self.indent()}BoolValue: {node.value}")

    def visit_int_value(self, node):
        print(f"{self.indent()}IntValue: {node.value}")

    def visit_float_value(self, node):
        print(f"{self.indent()}FloatValue: {node.value}")

    def visit_string_value(self, node):
        print(f"{self.indent()}StringValue: \"{node.value}\"")

    def visit_function_type(self, node):
        print(f"{self.indent()}FunctionType: {node.type}")

    def visit_variable_type(self, node):
        print(f"{self.indent()}VariableType: {node.type}")

    def visit_parameter(self, node):
        print(f"{self.indent()}Parameter:")
        self.indentation += 2
        node.type.accept(self)
        node.identifier.accept(self)
        self.indentation -= 2

    def visit_assignment_expression(self, node):
        print(f"{self.indent()}AssignmentExpression:")
        self.indentation += 2
        print(f"{self.indent()}Identifier:")
        node.identifier.accept(self)
        print(f"{self.indent()}Expression:")
        node.expression.accept(self)
        self.indentation -= 2

    def visit_additive_expression(self, node):
        print(f"{self.indent()}AdditiveExpression:")
        self.indentation += 2
        print(f"{self.indent()}LeftOperand:")
        node.left.accept(self)
        print(f"{self.indent()}Operator: {node.operator}")
        print(f"{self.indent()}RightOperand:")
        node.right.accept(self)
        self.indentation -= 2

    def visit_multiplicative_expression(self, node):
        print(f"{self.indent()}MultiplicativeExpression:")
        self.indentation += 2
        print(f"{self.indent()}LeftOperand:")
        node.left.accept(self)
        print(f"{self.indent()}Operator: {node.operator}")
        print(f"{self.indent()}RightOperand:")
        node.right.accept(self)
        self.indentation -= 2

    def visit_negation_expression(self, node):
        print(f"{self.indent()}NegationExpression:")
        self.indentation += 2
        print(f"{self.indent()}Operator: {node.operator}")
        print(f"{self.indent()}Expression:")
        node.expression.accept(self)
        self.indentation -= 2

    def visit_or_expression(self, node):
        print(f"{self.indent()}OrExpression:")
        self.indentation += 2
        print(f"{self.indent()}LeftOperand:")
        node.left.accept(self)
        print(f"{self.indent()}RightOperand:")
        node.right.accept(self)
        self.indentation -= 2

    def visit_and_expression(self, node):
        print(f"{self.indent()}AndExpression:")
        self.indentation += 2
        print(f"{self.indent()}LeftOperand:")
        node.left.accept(self)
        print(f"{self.indent()}RightOperand:")
        node.right.accept(self)
        self.indentation -= 2

    def visit_comparison_expression(self, node):
        print(f"{self.indent()}ComparisonExpression:")
        self.indentation += 2
        print(f"{self.indent()}LeftOperand:")
        node.left.accept(self)
        print(f"{self.indent()}Operator: {node.operator}")
        print(f"{self.indent()}RightOperand:")
        node.right.accept(self)
        self.indentation -= 2

    def visit_method_call(self, node):
        print(f"{self.indent()}MethodCall:")
        self.indentation += 2
        print(f"{self.indent()}MethodName:")
        node.name.accept(self)
        print(f"{self.indent()}Arguments:")
        self.indentation += 2
        for argument in node.arguments or []:
            argument.accept(self)
        self.indentation -= 4

    def visit_method_call_expression(self, node):
        print(f"{self.indent()}MethodCallExpression:")
        self.indentation += 2
        print(f"{self.indent()}Caller:")
        node.caller.accept(self)
        print(f"{self.indent()}Methods:")
        self.indentation += 2
        for method in node.methods:
            method.accept(self)
        self.indentation -= 4

    def visit_function_call(self, node):
        print(f"{self.indent()}FunctionCallStatement:")
        self.indentation += 2
        print(f"{self.indent()}FunctionName:")
        node.identifier.accept(self)
        print(f"{self.indent()}Arguments:")
        self.indentation += 2
        for argument in node.arguments:
            argument.accept(self)
        self.indentation -= 4

    def visit_block(self, node):
        print(f"{self.indent()}Block:")
        self.indentation += 2
        print(f"{self.indent()}Statements:")
        self.indentation += 2
        for statement in node.statements:
            statement.accept(self)
        self.indentation -= 4

    def visit_if_statement(self, node):
        print(f"{self.indent()}IfStatement:")
        self.indentation += 2
        print(f"{self.indent()}Condition:")
        node.condition.accept(self)
        print(f"{self.indent()}IfBlock:")
        node.block.accept(self)
        if node.else_block:
            print(f"{self.indent()}ElseBlock:")
            node.else_block.accept(self)
        self.indentation -= 2

    def visit_while_statement(self, node):
        print(f"{self.indent()}WhileStatement:")
        self.indentation += 2
        print(f"{self.indent()}Condition:")
        node.condition.accept(self)
        print(f"{self.indent()}Block:")
        node.block.accept(self)
        self.indentation -= 2

    def visit_declaration_statement(self, node):
        print(f"{self.indent()}DeclarationStatement:")
        self.indentation += 2
        print(f"{self.indent()}VariableType:")
        node.variable_type.accept(self)
        print(f"{self.indent()}Identifier:")
        node.identifier.accept(self)
        if node.expression:
            print(f"{self.indent()}Expression:")
            node.expression.accept(self)
        self.indentation -= 2

    def visit_return_statement(self, node):
        print(f"{self.indent()}ReturnStatement:")
        self.indentation += 2
        print(f"{self.indent()}ReturnExpression:")
        node.expression.accept(self)
        self.indentation -= 2

    def visit_function(self, node):
        print(f"{self.indent()}Function:")
        self.indentation += 2
        print(f"{self.indent()}FunctionName:")
        node.identifier.accept(self)
        print(f"{self.indent()}FunctionType:")
        node.function_type.accept(self)
        print(f"{self.indent()}Parameters:")
        self.indentation += 2
        for parameter in node.parameters:
            parameter.accept(self)
        self.indentation -= 4
        print(f"{self.indent()}Block:")
        node.block.accept(self)

    def visit_program(self, node):
        print(f"{self.indent()}Program:")
        self.indentation += 2
        for function in node.functions:
            function.accept(self)
        self.indentation -= 2

        


