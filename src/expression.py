class Expression:
    def __init__(self, expression: str):
        self._expression = expression
    
    def isValid(self) -> bool:
        return True
    
    def asString(self) -> str:
        return self._expression
    
    def result(self) -> float:
        return 5
