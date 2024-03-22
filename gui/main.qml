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
            placeholderText: qsTr("Enter math expression...")

            onEditingFinished: {
                if (commandInput.isValid) {
                    commandInput.runCommand()
                    input.text = ""
                }
            }
            onTextChanged: {
                commandInput.input = input.text
                commandInput.changed()
                if (commandInput.isValid || input.text == "") {
                    input.background.color = "white"
                } else {
                    input.background.color = "#ffaaaa"
                }
            }

            background: Rectangle {
                color: "white"
            }
        }
    }
}
