import QtQuick 2.15
import QtQuick.Controls.Basic 2.15

ApplicationWindow {
    visible: true
    width: 300
    height: 500
    title: "Kalkulaattor"

    Rectangle {
        anchors.fill: parent

        gradient: Gradient {
            GradientStop { position: 0.0; color: "#3258ff" }
            GradientStop { position: 1.0; color: "#a2efff" }
        }

        ListView {
            id: "historyList"
            height: parent.height - input.height - line.height - line.anchors.topMargin
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 5

            verticalLayoutDirection: ListView.BottomToTop

            model: historyModel
            delegate: Text {
                text: display.command + "<br>&emsp;&rarr; " + display.result
                topPadding: 8
                lineHeight: 0.8
            }
        }

        Rectangle {
            id: "line"
            height: 1
            anchors.topMargin: 5
            anchors.top: historyList.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            color: "black"
        }
        
        TextField {
            id: "input"
            anchors.top: line.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: 40
            focus: true
            placeholderText: qsTr("Enter math expression...")

            onEditingFinished: {
                if (commandInput.isValid) {
                    commandInput.runCommand()
                    input.text = ""
                    historyIndex = -1
                }
            }
            onTextChanged: {
                commandInput.input = input.text
                if (commandInput.isValid || input.text == "") {
                    input.background.color = "white"
                } else {
                    input.background.color = "#ffaaaa"
                }
            }

            background: Rectangle {
                color: "white"
            }

            property int historyIndex: -1
            Keys.onUpPressed: {
                function min(a, b) {
                    return (a < b) ? a : b;
                }
                // - 4 = -1 - 3 lines that tell about usage
                historyIndex = min(historyIndex + 1, historyModel.rowCount() - 4)
                useOldLineAsInput()
            }
            Keys.onDownPressed: {
                function max(a, b) {
                    return (a > b) ? a : b;
                }
                historyIndex = max(-1, historyIndex - 1)
                useOldLineAsInput()
            }
            function useOldLineAsInput() {
                var newCommand = ""
                if (historyIndex != -1) {
                    newCommand = historyModel.data(historyModel.index(historyIndex,0)).command
                }
                input.text = newCommand
            }
        }
    }
}
