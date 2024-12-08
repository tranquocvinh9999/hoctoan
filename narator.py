from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

label = QLabel("Welcome to the app")
label.setAccessibleName("Welcome Label")
label.setAccessibleDescription("This label displays a welcome message.")

button = QPushButton("Click Me")
button.setAccessibleName("Click Button")
button.setAccessibleDescription("This button triggers an action when clicked.")

layout.addWidget(label)
layout.addWidget(button)
window.setLayout(layout)

window.show()
app.exec()
