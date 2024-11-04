import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSlider, QLabel, QPushButton, QFileDialog, QDialog, QFontDialog, QColorDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

def start_text_scroller_with_controls(initial_scroll_speed=50):
    """
    Starts a text scroller with speed control slider and pause/resume button.
    
    Parameters:
        text_file_path (str): Path to the text file to display and scroll.
        initial_scroll_speed (int): Initial scrolling speed in milliseconds.
    """

    # Initialize the application
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Text Scroller with Controls")

    # Layout
    layout = QVBoxLayout()

    # Create a text display widget
    text_display = QTextEdit()
    text_display.setReadOnly(True)
    text_display.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    layout.addWidget(text_display)

    # Load text content
    # try:
    #     with open(text_file_path, 'r', encoding='utf-8') as file:
    #         text_data = file.read()
    #         text_display.setPlainText(text_data)  # Load text into display
    # except Exception as e:
    #     print(f"Error loading text file: {e}")
    #     return

    # Timer for automatic scrolling
    scroll_timer = QTimer()
    scroll_timer.setInterval(initial_scroll_speed)

    def load_text_file():

        """Load a text file chosen by the user."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName()
    
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_data = file.read()
                text_display.clear()
                text_display.setPlainText(text_data)  # Load text into display
        except Exception as e:
            print(f"Error loading text file: {e}")
            return
        

# Define the scroll function
    def scroll_text():
        scroll_bar = text_display.verticalScrollBar()
        if scroll_bar.value() < scroll_bar.maximum():
            scroll_bar.setValue(scroll_bar.value() + 1)
        else:
            scroll_timer.stop()

    # Connect the scroll function to the timer
    scroll_timer.timeout.connect(scroll_text)
    scroll_timer.start()

    # Speed Label and Slider
    speed_label = QLabel(f"Scroll Speed: {initial_scroll_speed} ms", window)
    
    speed_slider = QSlider(Qt.Horizontal)
    speed_slider.setMinimum(1)
    speed_slider.setMaximum(100)
    speed_slider.setValue(initial_scroll_speed)
    speed_slider.setTickInterval(10)

    # Update the scroll speed when the slider value changes
    def update_scroll_speed():
        new_speed = speed_slider.value()
        speed_label.setText(f"Scroll Speed: {new_speed} ms")
        scroll_timer.setInterval(new_speed)

    speed_slider.valueChanged.connect(update_scroll_speed)

    # Pause/Resume Button
    pause_button = QPushButton()
    pause_button.setIcon(QIcon("./icons/play-png.png"))  # Initial icon is play

    is_paused = True


    def toggle_pause_resume():
        nonlocal is_paused
        if is_paused:
            scroll_timer.start()
            pause_button.setIcon(QIcon("./icons/pause-png.png"))  # Set icon to pause
        else:
            scroll_timer.stop()
            pause_button.setIcon(QIcon("./icons/play-png.png"))  # Set icon to play
        is_paused = not is_paused

    pause_button.clicked.connect(toggle_pause_resume)



    # Settings dialog
    def open_settings_dialog():
        settings_dialog = QDialog()
        settings_dialog.setWindowTitle("Settings")
        settings_layout = QVBoxLayout(settings_dialog)

        # Font selection button
        def change_font():
            font, ok = QFontDialog.getFont(text_display.font())
            if ok:
                text_display.setFont(font)

        font_button = QPushButton("Change Font")
        font_button.clicked.connect(change_font)
        settings_layout.addWidget(font_button)

        # Font color selection button
        def change_font_color():
            color = QColorDialog.getColor()
            if color.isValid():
                text_display.setTextColor(color)

        color_button = QPushButton("Change Font Color")
        color_button.clicked.connect(change_font_color)
        settings_layout.addWidget(color_button)

        # "Paste in own text" button
        def open_paste_text_dialog():
            paste_dialog = QDialog(settings_dialog)
            paste_dialog.setWindowTitle("Paste Your Own Text")
            paste_layout = QVBoxLayout(paste_dialog)
            paste_text_edit = QTextEdit()
            paste_layout.addWidget(paste_text_edit)

            # Apply pasted text to the main text display
            def apply_pasted_text():
                pasted_text = paste_text_edit.toPlainText()
                text_display.clear()
                text_display.setPlainText(pasted_text)
                paste_dialog.accept()

            apply_button = QPushButton("Apply Text")
            apply_button.clicked.connect(apply_pasted_text)
            paste_layout.addWidget(apply_button)
            paste_dialog.exec_()

        paste_button = QPushButton("Paste in Own Text")
        paste_button.clicked.connect(open_paste_text_dialog)
        settings_layout.addWidget(paste_button)

        # Display the settings dialog
        settings_dialog.exec_()

   


    
    # Horizontal layout for slider and button
    control_layout = QHBoxLayout()
    control_layout.addWidget(speed_label)
    control_layout.addWidget(speed_slider)
    control_layout.addWidget(pause_button)
    layout.addLayout(control_layout)

    upload_button = QPushButton("Upload Text File")
    upload_button.clicked.connect(load_text_file)
    layout.addWidget(upload_button)  
    
    # Settings button
    settings_button = QPushButton("Settings")
    settings_button.clicked.connect(open_settings_dialog)
    layout.addWidget(settings_button)

    # Set the layout and display the window
    window.setLayout(layout)
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())

# Example usage:
# start_text_scroller_with_controls("path/to/your/textfile.txt", initial_scroll_speed=50)