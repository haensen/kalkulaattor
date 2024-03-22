from lark import Lark, Transformer, v_args, exceptions

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
    
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

@v_args(inline=True)
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = float

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
