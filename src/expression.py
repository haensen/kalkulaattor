from lark import Lark, Transformer, v_args, exceptions
import math
import enum

grammar = """
    ?start: sum
        | var_assignment
        | func_decl
    
    ?var_assignment: WORD "=" sum -> assign_var

    ?func_decl: WORD "(" WORD ["," WORD]* ")" "=" sum -> declare_function

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub
    
    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
        | "-" atom          -> neg
        | "(" sum ")"
        | WORD             -> variable
        | "abs(" sum ")"    -> abs
        | "sin(" sum ")"    -> sin
        | "cos(" sum ")"    -> cos
        | "tan(" sum ")"    -> tan
        | WORD "(" sum ["," sum]* ")" -> func
    
    %import common.NUMBER
    %import common.WORD
    %import common.WS_INLINE
    %ignore WS_INLINE
"""
parser = Lark(grammar, parser="earley")

@v_args(inline=True)
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg, abs
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
    
    def __init__(self, variables: dict, functions: dict):
        super().__init__()
        self._variables = variables
        self._functions = functions
    
    def func(self, name, *args):
        argNames = self._functions[name]['argNames']
        funcDef = self._functions[name]['definition']

        exprVariables = self._variables.copy()

        for argName, value in zip(argNames, args):
            exprVariables[argName] = value

        funcTree = parser.parse(funcDef)
        result = CalculateTree(exprVariables, self._functions).transform(funcTree)

        return result

class ExpressionType(enum.Enum):
    CALCULATION = 0
    VARIABLE_ASSIGNMENT = 1
    FUNCTION_DECLARATION = 2
    INVALID = 3

class Expression:
    def _topNodeName(self, parseTree) -> bool:
        for node in parseTree.iter_subtrees_topdown():
            return node.data
        return ""
    
    def __init__(self, expression: str, variables: dict = {}, functions: dict = {}):
        self._expression = expression
        self._type = ExpressionType.INVALID
        self._result = None
        try:
            parseTree = parser.parse(expression)

            if self._topNodeName(parseTree) == "declare_function":
                funcName = str(parseTree.children[0])
                funcArgs = map(str, parseTree.children[1:-1])
                # Args might have one element with type None if only one arg is used
                funcArgs = list(filter(lambda arg : arg != 'None', funcArgs))
                funcDef = expression.split('=')[1].replace(' ', '')
                self._result = {funcName: {'definition': funcDef, 'argNames': funcArgs}}
                self._type = ExpressionType.FUNCTION_DECLARATION
            else:
                self._result = CalculateTree(variables, functions).transform(parseTree)
                if self._topNodeName(parseTree) == "assign_var":
                    self._type = ExpressionType.VARIABLE_ASSIGNMENT
                else:
                    self._type = ExpressionType.CALCULATION
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
        return self._type
    
    def asString(self) -> str:
        return self._expression
    
    def result(self) -> float:
        return self._result
