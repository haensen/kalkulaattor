import sys

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QAbstractListModel, Qt, pyqtProperty, QObject, pyqtSlot, QModelIndex

from expression import Expression

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
        endOfList = self.rowCount(0)
        self.beginInsertRows(QModelIndex(), endOfList, endOfList)
        self._lines.append(data)
        self.endInsertRows()

class CommandInput(QObject):
    def __init__(self, historyList: QtList):
        super().__init__()
        self._historyList = historyList
    
    @pyqtSlot(str)
    def newCommand(self, command):
        expr = Expression(command)
        if expr.isValid():
            self._historyList.push(HistoryLine(expr.asString(), str(expr.result())))

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    historyModel = QtList([
        HistoryLine("mummo", "hyva"),
        HistoryLine("mamma", "3"),
        HistoryLine("jee", "5")
    ])
    engine.rootContext().setContextProperty('historyModel', historyModel)

    commandInput = CommandInput(historyModel)
    engine.rootContext().setContextProperty('commandInput', commandInput)

    engine.load('gui/main.qml')

    sys.exit(app.exec())
