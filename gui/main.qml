import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "Kalkulaattor"

    Rectangle {
        anchors.fill: parent

        gradient: Gradient {
            GradientStop { position: 0.0; color: "aqua" }
            GradientStop { position: 1.0; color: "teal" }
        }

        Column {
            anchors.fill: parent

            spacing: 5

            ListView {
                // color: "red"
                width: parent.width
                height: parent.height - parent.spacing - input.height

                model: historyModel
                delegate: Text {
                    text: display.command + ": " + display.result
                }
            }
            
            TextField {
                id: "input"
                anchors.left: parent.left
                anchors.right: parent.right
                placeholderText: qsTr("Enter math expression...")

                onEditingFinished: {
                    commandInput.newCommand(input.text)
                    input.text = ""
                }
            }
        }
    }
}
