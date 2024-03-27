import sys

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QAbstractListModel, Qt, pyqtProperty, QObject, pyqtSlot, QModelIndex

from expression import Expression, ExpressionType

class HistoryLine(QObject):
    def __init__(self, command = "", result = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._command = command
        self._result = result
    
    @pyqtProperty(str)
    def command(self):
        return self._command
    
    @pyqtProperty(str)
    def result(self):
        return self._result

class QtList(QAbstractListModel):
    def __init__(self, lines = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lines = []
        if lines:
            self._lines = lines

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._lines[index.row()]
    
    def rowCount(self, index):
        return len(self._lines)
    
    def push(self, data):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._lines.insert(0, data)
        self.endInsertRows()

class CommandInput(QObject):
    def __init__(self, historyList: QtList, variables: dict, functions: dict):
        super().__init__()
        self._historyList = historyList
        self._variables = variables
    
    @pyqtSlot()
    def runCommand(self):
        if not self._expr.isValid():
            return
        
        command = self._expr.asString()
        result = self._expr.result()

        if self._expr.type() == ExpressionType.VARIABLE_ASSIGNMENT:
            self._variables[result[0]] = result[1]
            result = result[1]
        elif self._expr.type() == ExpressionType.FUNCTION_DECLARATION:
            result = 0
            # TODO: FIX THIS UGLINESS AND SHOW SOMETHING MORE MEANINGFUL
        
        self._historyList.push(HistoryLine(command, f'{result:g}'))
    
    @pyqtSlot()
    def changed(self):
        self._expr = Expression(self._input, self._variables)
    
    @pyqtProperty(str)
    def input(self):
        return self._input
    @input.setter
    def input(self, value):
        self._input = value
    
    @pyqtProperty(bool)
    def isValid(self):
        return self._expr.isValid()


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    historyModel = QtList([
        HistoryLine("you can declare your own functions", "plusTree(x) = x + 3"),
        HistoryLine("you can set and use variables", "var = 3"),
        HistoryLine("Welcome!", "Insert an expression like 4 + 3 below"),
    ])
    engine.rootContext().setContextProperty('historyModel', historyModel)

    variables = {
        "pi": 3.141592653
    }
    functions = {}
    commandInput = CommandInput(historyModel, variables, functions)
    engine.rootContext().setContextProperty('commandInput', commandInput)

    engine.load('gui/main.qml')

    sys.exit(app.exec())
