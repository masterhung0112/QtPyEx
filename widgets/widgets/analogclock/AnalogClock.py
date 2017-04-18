from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5.QtCore import QTimer, QPoint, QTime
from PyQt5.Qt import Qt

class AnalogClock(QWidget):
	
	hourHand = QPolygon([QPoint(7, 8), QPoint(-7, 8), QPoint(0, -40)])
	minuteHand = QPolygon([QPoint(7, 8), QPoint(-7, 8), QPoint(0, -70)])
	secondHand = QPolygon([QPoint(7, 8), QPoint(-7, 8), QPoint(0, -96)])
	
	hourColor = QColor(127, 0, 127)
	minuteColor = QColor(0, 127, 127, 191)
	secondColor = QColor(127, 127, 0, 191)
	
	def __init__(self, *args):
		super(QWidget, self).__init__(*args)
		
		timer = QTimer(self)
		timer.timeout.connect(self.update)
		
		timer.start(1000)
		
		self.setWindowTitle(self.tr("Analog Clock"))
		self.resize(200, 200)
	
	def paintEvent(self, event):
		
		side = min(self.width(), self.height())
		time = QTime.currentTime()
		
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		
		painter.translate(self.width() / 2, self.height() / 2)
		painter.scale(side / 200.0, side / 200.0)
		
		painter.setPen(Qt.NoPen)
		painter.setBrush(self.hourColor)
		
		painter.save()
		painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
		painter.drawConvexPolygon(self.hourHand)
		painter.restore()
		
		painter.setPen(self.hourColor)
		
		for i in range(12):
			painter.drawLine(88, 0, 96, 0)
			painter.rotate(30.0)
		
		painter.setPen(Qt.NoPen)
		painter.setBrush(self.minuteColor)
		
		painter.save()
		painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
		painter.drawConvexPolygon(self.minuteHand)
		painter.restore()
		
		painter.setPen(self.minuteColor)
		for i in range(60):
			if (i % 5) != 0:
				painter.drawLine(92, 0, 96, 0)
			painter.rotate(6.0)
			
		painter.setPen(Qt.NoPen)
		painter.setBrush(self.secondColor)
		
		painter.save()
		painter.rotate(6.0 * time.second())
		painter.drawConvexPolygon(self.secondHand)
		painter.restore()