from PyQt5.QtWidgets import QListView, QTableView, QAbstractItemView, QFileSystemModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt, QSize, QDir

class HListViewModel(QStandardItemModel):
	def __init__(self, *args):
		QStandardItemModel.__init__(self, *args)
	
	

class HListView(QListView):
	
	def __init__(self, *args):
		QListView.__init__(self, *args)
		
		self.setAcceptDrops(True)
		self.setDragEnabled(False)
		self.setDropIndicatorShown(True)
		
		self.setViewMode(QListView.IconMode)
		#self.setIconSize(QSize(131, 108))
		self.setResizeMode(QListView.Adjust)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		#self.setUniformItemSizes(True)
		#self.setWordWrap(True)
		#self.setStyleSheet("QListView::item { padding-top: 2px; }")
		#self.model = HListViewModel(self)
		self.model = QFileSystemModel()
		self.model.setRootPath(QDir.currentPath())
		self.setModel(self.model)
		self.setRootIndex(self.model.index(QDir.currentPath()))
		
		#self.define_model()
	
	def define_model(self):
		self.model.setColumnCount(1)
		self.model.setHorizontalHeaderLabels(["Thumb", "Name"])
		row = []
		
		col = QStandardItem()
		col.setIcon(QIcon("mask.png"))
		col.setText("HIHI")
		row.append(col)
		#self.model.insertColumn(0, [col])
		self.model.appendRow(row)
		row = []
		col = QStandardItem("Name")
		col.setIcon(QIcon("mask.png"))
		col.setText("HOHO")
		row.append(col)
		#self.model.insertColumn(1, [col])
		self.model.appendRow(row)