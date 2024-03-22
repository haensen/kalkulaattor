from lark import Lark, Transformer, v_args, exceptions
import math

grammar = """
    ?start: sum
    
    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub
    
    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
        | "-" atom          -> neg
        | "(" sum ")"
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

parser = Lark(grammar, parser="lalr", transformer=CalculateTree())

class Expression:
    def __init__(self, expression: str):
        self._expression = expression
        self._isValid = False
        self._result = 0

        try:
            self._result = parser.parse(expression)
            self._isValid = True
        except exceptions.UnexpectedToken:
            pass
        except exceptions.UnexpectedCharacters:
            pass
        except ZeroDivisionError:
            pass
    
    def isValid(self) -> bool:
        return self._isValid
    
    def asString(self) -> str:
        return self._expression
    
    def result(self) -> float:
        return self._result
