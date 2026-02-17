import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt
import threading

shutdown_event = threading.Event()
ui_state = {"status": "Starting"}

def start_ui():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("HERO")
    window.setFixedSize(250, 80)

    label = QLabel("Starting", window)
    label.setAlignment(Qt.AlignCenter)
    label.setGeometry(0, 0, 250, 80)

    def update():
        label.setText(ui_state["status"])
        if not shutdown_event.is_set():
            app.processEvents()
            threading.Timer(0.3, update).start()
        else:
            app.quit()

    update()
    window.show()
    sys.exit(app.exec_())
