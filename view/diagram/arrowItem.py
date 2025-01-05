import math

from PyQt5.QtCore import Qt, QLineF, QPointF
from PyQt5.QtGui import QPen, QBrush, QPolygonF
from PyQt5.QtWidgets import QGraphicsLineItem


class ArrowItem(QGraphicsLineItem):
    def __init__(self, start_item, end_item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.startItem = start_item
        self.endItem = end_item
        #self.setPen(QPen(Qt.black, 5))
        self.setPen(self.createArrowPen())
        self.updatePosition()

    def createArrowPen(self):
        pen = QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap)
        size = 10
        brush = QBrush(Qt.black)
        return pen  # Simplified arrowhead creation

    def updatePosition(self):
        start_center = self.startItem.sceneBoundingRect().center()
        end_center = self.endItem.sceneBoundingRect().center()
        self.setLine(QLineF(start_center, end_center))

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)

        # Calculate arrowhead dimensions
        line = self.line()
        angle = line.angle()
        length = line.length()

        arrow_size = 10  # Adjust arrowhead size as needed

        # Calculate arrowhead points
        p1 = line.p2()
        p2 = p1 + QPointF(
            arrow_size * math.cos(math.radians(angle - 135)),
            arrow_size * math.sin(math.radians(angle - 135))
        )
        p3 = p1 + QPointF(
            arrow_size * math.cos(math.radians(angle - 225)),
            arrow_size * math.sin(math.radians(angle - 225))
        )

        # Draw arrowhead polygon
        arrowhead_polygon = [p1, p2, p3]
        painter.setBrush(QBrush(Qt.black))  # Set arrowhead color
        painter.drawPolygon(QPolygonF(arrowhead_polygon))