from expression import Expression, ExpressionType

class Calculator:
    """ A class that performs calculations and remembers previously added variables etc.
    Exists mainly to separate logic from Qt code.
    """

    def __init__(self):
        self._functions = {}
        self._variables = {
            "pi": 3.141592653
        }
        self._results = []

    def executeExpression(self, expr: str) -> None:
        """ Calculates/executes given expression. """
        executedExpr = Expression(expr, self._variables, self._functions)

        record = {'expr': expr}
        if executedExpr.type() == ExpressionType.CALCULATION:
            record['result'] = f'{executedExpr.result():g}'
        elif executedExpr.type() == ExpressionType.VARIABLE_ASSIGNMENT:
            record['result'] = f'{executedExpr.result()[1]:g}'

            self._variables[executedExpr.result()[0]]  = executedExpr.result()[1]
        elif executedExpr.type() == ExpressionType.FUNCTION_DECLARATION:
            record['result'] = "Declared!"

            self._functions.update(executedExpr.result())
        else:
            return
        self._results.append(record)

    def isValidExpression(self, expr: str) -> bool:
        """ Returns true if the given expression can be executed. """
        return Expression(expr, self._variables, self._functions).type() != ExpressionType.INVALID

    def getExpressions(self) -> list[dict]:
        """ Returns given expressions and their results
        Structure: [{'expr': '3+5', 'result': '8'}, {'expr': 'a=3+5', 'result': '8'} ...]
        """
        return self._results
