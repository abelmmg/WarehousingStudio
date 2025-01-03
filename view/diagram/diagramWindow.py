from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
    QGraphicsLineItem, QGraphicsTextItem, QVBoxLayout, QDialog, QPushButton, QInputDialog, QMessageBox, QGraphicsItem, \
    QHBoxLayout
from PyQt5.QtCore import Qt, QRectF, QLineF
from PyQt5.QtGui import QPen


class DraggableRectItem(QGraphicsRectItem):
    def __init__(self, rect, label, *args, **kwargs):
        super().__init__(rect, *args, **kwargs)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)
        self.label = label
        self.text = QGraphicsTextItem(label, self)
        self.text.setDefaultTextColor(Qt.black)
        self.text.setPos(rect.width() / 2 - self.text.boundingRect().width() / 2,
                         rect.height() / 2 - self.text.boundingRect().height() / 2)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.updateConnections()
        return super().itemChange(change, value)

    def updateConnections(self):
        for line in self.scene().items():
            if isinstance(line, QGraphicsLineItem):
                if line.startItem == self or line.endItem == self:
                    line.updatePosition()


class ArrowItem(QGraphicsLineItem):
    def __init__(self, start_item, end_item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.startItem = start_item
        self.endItem = end_item
        self.setPen(QPen(Qt.black, 2))
        self.updatePosition()

    def updatePosition(self):
        start_center = self.startItem.sceneBoundingRect().center()
        end_center = self.endItem.sceneBoundingRect().center()
        self.setLine(QLineF(start_center, end_center))


class DiagramWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Diagram Window')
        self.setGeometry(100, 100, 1700, 1500)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)

        # Create initial rectangles
        self.rect_wms = DraggableRectItem(QRectF(0, 0, 100, 50), 'WMS')
        self.rect_tms = DraggableRectItem(QRectF(200, 200, 100, 50), 'TMS')

        self.scene.addItem(self.rect_wms)
        self.scene.addItem(self.rect_tms)

        # Create initial arrow
        self.arrow = ArrowItem(self.rect_wms, self.rect_tms)
        self.scene.addItem(self.arrow)

        # Create buttons
        self.add_app_button = QPushButton('Add Application', self)
        self.add_app_button.clicked.connect(self.add_application)
        self.add_interface_button = QPushButton('Add Interface', self)
        self.add_interface_button.clicked.connect(self.add_interface)

        # Layout
        layout = QHBoxLayout()

        layout_buttons = QVBoxLayout()
        layout_buttons.addWidget(self.add_app_button)
        layout_buttons.addWidget(self.add_interface_button)

        layout.addLayout(layout_buttons)
        layout.addWidget(self.view)
        self.setLayout(layout)

    def add_application(self):
        text, ok = QInputDialog.getText(self, 'Add Application', 'Enter application name:')
        if ok and text:
            rect = DraggableRectItem(QRectF(50, 50, 100, 50), text)
            self.scene.addItem(rect)

    def add_interface(self):
        selected_items = self.scene.selectedItems()
        if len(selected_items) != 2:
            QMessageBox.warning(self, 'Error', 'Please select exactly two rectangles.')
            return
        if not all(isinstance(item, DraggableRectItem) for item in selected_items):
            QMessageBox.warning(self, 'Error', 'Selected items must be rectangles.')
            return

        start_item, end_item = selected_items
        arrow = ArrowItem(start_item, end_item)
        self.scene.addItem(arrow)
