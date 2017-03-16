from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGroupBox, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QStyleFactory, QMessageBox, QButtonGroup, QTableWidget, QAbstractItemView, QHeaderView, QRadioButton, QStyle, QSpinBox, QHBoxLayout, QActionGroup, QAction, QFileDialog, QDialog, QTableWidgetItem, QComboBox, QItemDelegate
from PyQt5.QtGui import QKeySequence, QImageReader, QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QRegularExpression, QSize, QFileInfo, QDir, pyqtSignal

from list_view import HListView

class MainWindow(QMainWindow):
	
	def __init__(self, *args):
		super(QMainWindow, self).__init__(*args)
		
		centerWidget = QWidget(self)
		
		self.setCentralWidget(centerWidget)
		
		mainLayout = QGridLayout(centerWidget)
		
		self.listView = HListView(self)
		
		mainLayout.addWidget(self.listView, 0, 0, 1, 2)
		
		self.setWindowTitle("List View")
	