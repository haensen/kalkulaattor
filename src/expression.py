from lark import Lark, Transformer, v_args, exceptions
import math
import enum

grammar = """
    ?start: sum
        | assignment
    
    ?assignment.1: CNAME "=" sum -> assign_var

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub
    
    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
        | "-" atom          -> neg
        | "(" sum ")"
        | CNAME             -> variable
        | "abs(" sum ")"    -> abs
        | "sin(" sum ")"    -> sin
        | "cos(" sum ")"    -> cos
        | "tan(" sum ")"    -> tan
    
    %import common.NUMBER
    %import common.CNAME
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

@v_args(inline=True)
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg, abs
    from math import sin, cos, tan
    number = float

    def sin(self, value):
        return math.sin(math.radians(value))
    def cos(self, value):
        return math.cos(math.radians(value))
    def tan(self, value):
        return math.tan(math.radians(value))
    
    def assign_var(self, name, value):
        return (name, value)
    def variable(self, name):
        return self._variables[name]
    
    def __init__(self, variables: dict):
        super().__init__()
        self._variables = variables

parser = Lark(grammar, parser="earley")

class ExpressionType(enum.Enum):
    CALCULATION = 0
    VARIABLE_ASSIGNMENT = 1

class Expression:
    def __init__(self, expression: str, variables: dict = {}):
        self._expression = expression
        self._isValid = False
        self._result = 0

        try:
            parseTree = parser.parse(expression)
            self._result = CalculateTree(variables).transform(parseTree)
            self._isValid = True
        except exceptions.UnexpectedToken:
            pass
        except exceptions.UnexpectedCharacters:
            pass
        except exceptions.VisitError:
            pass
        except exceptions.UnexpectedEOF:
            pass
        except ZeroDivisionError:
            pass
    
    def type(self) -> ExpressionType:
        exprType = ExpressionType.CALCULATION
        if type(self.result()) is tuple:
            exprType = ExpressionType.VARIABLE_ASSIGNMENT
        return exprType
    
    def isValid(self) -> bool:
        return self._isValid
    
    def asString(self) -> str:
        return self._expression
    
    def result(self) -> float:
        return self._result
