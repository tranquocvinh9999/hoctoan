from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
import sys

class VirtualKeyboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout
        self.setWindowTitle("Virtual Keyboard")
        layout = QVBoxLayout()

        # Input field
        self.input_field = QLineEdit(self)
        self.input_field.setAccessibleName("Input Field")
        layout.addWidget(self.input_field)

        # Horizontal layout for number buttons
        number_layout = QHBoxLayout()
        number_layout.setSpacing(5)  # Set spacing between buttons to 5 pixels

        # Button labels for numbers
        number_buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        
        # Create number buttons
        for button_text in number_buttons:
            button = QPushButton(button_text, self)
            button.setAccessibleName(f"Button {button_text}")
            button.clicked.connect(lambda _, t=button_text: self.on_button_click(t))
            button.setFixedSize(80, 50)  # Set uniform button size
            number_layout.addWidget(button)

        # Add the number layout to the main layout
        layout.addLayout(number_layout)

        # Horizontal layout for function keys
        function_layout = QHBoxLayout()
        function_layout.setSpacing(5)  # Set spacing between buttons to 5 pixels

        # Button labels for function keys
        function_buttons = ['Backspace', 'Enter', 'Space', ',', '/', '<', '>', 'Exit']
        
        # Create function buttons
        for button_text in function_buttons:
            button = QPushButton(button_text, self)
            button.setAccessibleName(f"Button {button_text}")
            button.clicked.connect(lambda _, t=button_text: self.on_button_click(t))
            button.setFixedSize(80, 50)  # Set uniform button size
            function_layout.addWidget(button)

        # Add function layout to the main layout
        layout.addLayout(function_layout)

        # Set the layout for the widget
        self.setLayout(layout)

    def on_button_click(self, button_text):
        if button_text == "Enter":
            print("Entered:", self.input_field.text())
        elif button_text == "Backspace":
            self.input_field.backspace()
        elif button_text == "Space":
            self.input_field.insert(" ")
        elif button_text == "Exit":
            print("Exiting application.")
            QApplication.quit()
        else:
            self.input_field.insert(button_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    keyboard = VirtualKeyboard()
    keyboard.resize(800, 200)  # Resize to a reasonable initial size
    keyboard.showFullScreen()   # Make the window full screen
    sys.exit(app.exec())
