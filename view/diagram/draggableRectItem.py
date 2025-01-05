from PyQt5.QtWidgets import QMenu, QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
    QGraphicsLineItem, QGraphicsTextItem, QVBoxLayout, QDialog, QPushButton, QInputDialog, QMessageBox, QGraphicsItem, \
    QHBoxLayout, QFileDialog, QGraphicsObject
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt5.QtGui import QPen

from view.diagram.resizer import Resizer


class DraggableRectItem(QGraphicsRectItem):
    def __init__(self, rect, label, *args, **kwargs):
        super().__init__(rect, *args, **kwargs)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemIsFocusable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)
        self.label = label
        self.text = QGraphicsTextItem(label, self)
        self.text.setDefaultTextColor(Qt.black)
        """
        self.text.setPos(rect.width() / 2 - self.text.boundingRect().width() / 2,
                       rect.height() / 2 - self.text.boundingRect().height() / 2)
        """
        self.text.setPos(rect.x(), rect.y())

        self.resizer = Resizer(parent=self)
        resizerWidth = self.resizer.rect.width() / 2
        resizerOffset = QPointF(resizerWidth, resizerWidth)
        self.resizer.setPos(self.rect().bottomRight() - resizerOffset)
        self.resizer.resizeSignal.connect(self.resize)

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        painter.drawRect(self.rect())

    #@pyqtSlot()
    def resize(self, change: QPointF):
        self.setRect(self.rect().adjusted(0, 0, change.x(), change.y()))
        self.prepareGeometryChange()
        self.update()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange or change == QGraphicsItem.ItemScaleChange:
            self.updateConnections()
            self.updateTextPosition()  # Update text position after resize
        return super().itemChange(change, value)

    def updateConnections(self):
        for line in self.scene().items():
            if isinstance(line, QGraphicsLineItem):
                if line.startItem == self or line.endItem == self:
                    line.updatePosition()

    def updateTextPosition(self):
        self.text.setPos(self.boundingRect().center() - self.text.boundingRect().center())

    def contextMenuEvent(self, event):
        menu = QMenu(self.scene().views()[0])
        edit_action = menu.addAction("Edit Label")
        edit_action.triggered.connect(self.editLabel)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete)
        menu.exec_(event.screenPos())

    def editLabel(self):
        new_label, ok = QInputDialog.getText(None, "Edit Label", "Enter new label:")
        if ok and new_label:
            self.label = new_label
            self.text.setPlainText(new_label)
            self.text.setPos(self.boundingRect().width() / 2 - self.text.boundingRect().width() / 2,
                             self.boundingRect().height() / 2 - self.text.boundingRect().height() / 2)

    def delete(self):
        # Remove connected arrows
        for line in self.scene().items():
            if isinstance(line, QGraphicsLineItem) and (line.startItem == self or line.endItem == self):
                self.scene().removeItem(line)
        # Remove the rectangle itself
        self.scene().removeItem(self)
