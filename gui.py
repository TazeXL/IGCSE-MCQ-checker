import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

class MCQChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.excel_file_path = None
        self.markscheme_pdf_path = None
        self.process_files_callback = None

    def initUI(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f0f0f0;") 

        layout = QVBoxLayout(central_widget)

        title = QLabel("MCQ Checker")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        layout.addWidget(title)
        info_label = QLabel("Please choose your files!")
        info_label.setAlignment(Qt.AlignLeft)
        info_label.setStyleSheet("font-size: 20px; color: #333; margin-bottom: 10px;")
        layout.addWidget(info_label)

        excel_layout = QVBoxLayout()
        excel_label = QLabel("Excel File:")
        excel_label.setStyleSheet("font-size: 14px;")
        self.excel_label = QLabel("Not Selected")
        self.excel_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.excel_label.setStyleSheet("font-size: 14px;")
        excel_layout.addWidget(excel_label)
        self.excel_button = QPushButton("Choose Excel File")
        self.excel_button.setStyleSheet("font-size: 18px;")
        self.excel_button.setStyleSheet("background-color: #f44336; color: white;")  # Dark red
        self.excel_button.clicked.connect(self.select_excel_file)
        excel_layout.addWidget(self.excel_button)

        markscheme_layout = QVBoxLayout()
        markscheme_label = QLabel("Markscheme PDF:")
        markscheme_label.setStyleSheet("font-size: 14px;")
        self.markscheme_label = QLabel("Not Selected")
        self.markscheme_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.markscheme_label.setStyleSheet("font-size: 14px;")
        markscheme_layout.addWidget(markscheme_label)
        self.markscheme_button = QPushButton("Choose Markscheme PDF")
        self.markscheme_button.setStyleSheet("font-size: 18px;")
        self.markscheme_button.setStyleSheet("background-color: #f44336; color: white;")  # Dark red
        self.markscheme_button.clicked.connect(self.select_markscheme_pdf)
        markscheme_layout.addWidget(self.markscheme_button)

        layout.addLayout(excel_layout)
        layout.addLayout(markscheme_layout)

        layout.addStretch()

        submit_button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("font-size: 16px; background-color: #ff4545; color: white;")  # Bright green
        self.submit_button.clicked.connect(self.process_files)
        submit_button_layout.addWidget(self.submit_button)
        layout.addLayout(submit_button_layout)

        self.setCentralWidget(central_widget)

        self.setWindowTitle("MCQ Checker")
        self.setGeometry(300, 300, 400, 300)

    def select_excel_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls)")
        if file_dialog.exec_():
            self.excel_file_path = file_dialog.selectedFiles()[0]
            self.excel_label.setText(f"Not Selected\n{self.excel_file_path}")
            self.excel_button.setStyleSheet("background-color: #8BC34A; color: white;")  # Light green
            self.check_submit_color()
        else:
            self.excel_button.setStyleSheet("background-color: #f44336; color: white;")  # Dark red

    def select_markscheme_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        if file_dialog.exec_():
            self.markscheme_pdf_path = file_dialog.selectedFiles()[0]
            self.markscheme_label.setText(f"Not Selected\n{self.markscheme_pdf_path}")
            self.markscheme_button.setStyleSheet("background-color: #8BC34A; color: white;")  # Light green
            self.check_submit_color()
        else:
            self.markscheme_button.setStyleSheet("background-color: #f44336; color: white;")  # Dark red

    def check_submit_color(self):
        if self.excel_file_path and self.markscheme_pdf_path:
            self.submit_button.setStyleSheet("background-color: #4CAF50; color: white;")  # Bright green
        else:
            self.submit_button.setStyleSheet("background-color: #f44336; color: white;")  # Dark red

    def process_files(self):
        if self.process_files_callback:
         self.process_files_callback(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MCQChecker()
    window.show()
    sys.exit(app.exec_())
