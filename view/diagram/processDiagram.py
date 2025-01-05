import math

import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
    QGraphicsLineItem, QGraphicsTextItem, QVBoxLayout, QGraphicsItem
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF, QPoint
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF


class DraggableRectItem(QGraphicsRectItem):
    def __init__(self, rect, label, *args, **kwargs):
        super().__init__(rect, *args, **kwargs)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.label = label
        self.text = QGraphicsTextItem(label, self)
        self.text.setDefaultTextColor(Qt.black)
        self.text.setPos(rect.width() / 2 - self.text.boundingRect().width() / 2,
                         rect.height() / 2 - self.text.boundingRect().height() / 2)
        self.connected_arrows = []  # Store connected arrows

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.updateConnections()
            self.text.setPos(self.boundingRect().center() - self.text.boundingRect().center())
        return super().itemChange(change, value)

    def updateConnections(self):
        for arrow in self.connected_arrows:
            arrow.updatePosition()


class ArrowItem(QGraphicsLineItem):
    def __init__(self, start_item, end_item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_item = start_item
        self.end_item = end_item
        self.setPen(self.createArrowPen())

    def updatePosition(self):
        start_center = self.start_item.sceneBoundingRect().center()
        end_center = self.end_item.sceneBoundingRect().center()
        self.setLine(QLineF(start_center, end_center))

    def createArrowPen(self):
        pen = QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap)
        size = 10  # Adjust arrowhead size here
        brush = QBrush(Qt.black)
        return pen  # Simplified arrowhead creation

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

class ProcessDiagram(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Process Diagram")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.create_diagram(df)

    def create_diagram(self, df):
        x_offset = 150
        y_offset = 100
        rect_width = 150
        rect_height = 50

        rectangles = []

        for index, row in df.iterrows():
            process_name = row['Process']
            order = row['Order']

            rect = DraggableRectItem(QRectF(x_offset * order, y_offset, rect_width, rect_height), process_name)
            rect.setBrush(QColor(200, 200, 200))
            rect.setPen(QPen(Qt.black))
            self.scene.addItem(rect)

            rectangles.append(rect)

            if index > 0:
                arrow = ArrowItem(rectangles[index - 1], rect)
                self.scene.addItem(arrow)
                rectangles[index - 1].connected_arrows.append(arrow)


# Sample DataFrame
df = pd.DataFrame({'Process': ['Start', 'Process A', 'Process B', 'Process C', 'End'], 'Order': [1, 2, 3, 4, 5]})

# Create and show the diagram
app = QApplication([])
window = ProcessDiagram(df)
window.show()
app.exec_()
