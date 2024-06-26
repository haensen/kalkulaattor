from pathlib import Path
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QAbstractListModel, Qt, pyqtProperty, QObject, pyqtSlot, QModelIndex

from calculator import Calculator

class HistoryLine(QObject):
    def __init__(self, command = "", result = ""):
        super().__init__()
        self._command = command
        self._result = result
    
    @pyqtProperty(str, constant = True)
    def command(self):
        return self._command
    
    @pyqtProperty(str, constant = True)
    def result(self):
        return self._result

class QtList(QAbstractListModel):
    def __init__(self, lines = None):
        super().__init__()
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

class InputHandler(QObject):
    def __init__(self, historyList: QtList):
        super().__init__()
        self._historyList = historyList
        self._calculator = Calculator()
        self.input = ""
    
    @pyqtSlot()
    def runCommand(self):
        self._calculator.executeExpression(self.input)
        result = self._calculator.getExpressions()[-1]
        self._historyList.push(HistoryLine(result['expr'], result['result']))
    
    @pyqtProperty(str)
    def input(self):
        return self._input
    @input.setter
    def input(self, value):
        self._input = value
    
    @pyqtProperty(bool)
    def isValid(self):
        return self._calculator.isValidExpression(self.input)

class GuiApp:
    def run(self):
        app = QGuiApplication([])

        engine = QQmlApplicationEngine()
        engine.quit.connect(app.quit)

        historyModel = QtList([
            HistoryLine("Welcome!", "Insert an expression like 4 + 3 below"),
            HistoryLine("you can set and use variables", "var = 3"),
            HistoryLine("declare your own functions", "double(x) = x * 2"),
        ][::-1])
        engine.rootContext().setContextProperty('historyModel', historyModel)

        commandInput = InputHandler(historyModel)
        engine.rootContext().setContextProperty('commandInput', commandInput)

        engine.load(Path(__file__).with_name('mainWindow.qml').as_uri())

        return app.exec()
