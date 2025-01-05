from PyQt5.QtWidgets import QMenu, QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
    QGraphicsLineItem, QGraphicsTextItem, QVBoxLayout, QDialog, QPushButton, QInputDialog, QMessageBox, QGraphicsItem, \
    QHBoxLayout, QFileDialog, QGraphicsObject
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt5.QtGui import QPen, QIcon
import pickle

from view.diagram.arrowItem import ArrowItem
from view.diagram.draggableRectItem import DraggableRectItem


class DiagramWindow(QDialog):
    def __init__(self, interfaces, applications):
        super().__init__()

        self.interfaces = interfaces
        self.applications = applications

        self.setWindowTitle('Diagram Window')
        self.setGeometry(100, 100, 1700, 1500)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)

        self.create_diagram_applications()

        # Create buttons
        self.add_app_button = QPushButton('Add Application', self)
        self.add_app_button.clicked.connect(self.add_application)
        self.add_interface_button = QPushButton('Add Interface', self)
        self.add_interface_button.clicked.connect(self.add_interface)
        self.save_button = QPushButton('Save Diagram', self)
        self.save_button.clicked.connect(self.save_diagram)
        self.load_button = QPushButton('Load Diagram', self)
        self.load_button.clicked.connect(self.load_diagram)

        # Layout
        layout = QHBoxLayout()

        layout_buttons = QVBoxLayout()
        layout_buttons.addWidget(self.add_app_button)
        layout_buttons.addWidget(self.add_interface_button)
        layout_buttons.addWidget(self.save_button)
        layout_buttons.addWidget(self.load_button)

        layout.addLayout(layout_buttons)
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Load the icon from a file
        icon_path = "../resources/warehouse-bn1.png"
        self.setWindowIcon(QIcon(icon_path))

    def create_diagram_applications(self):
        # Create initial rectangles
        app_list = []
        pos = 0
        for index, app in self.applications.iterrows():
            app_name = app['Solution']
            pos += 190
            self.app_rect = DraggableRectItem(QRectF(pos, 0, 180, 50), app_name)
            app_list.append(self.app_rect)
            self.scene.addItem(self.app_rect)

        """
        self.rect_wms = DraggableRectItem(QRectF(0, 0, 100, 50), 'WMS')
        self.rect_tms = DraggableRectItem(QRectF(200, 200, 100, 50), 'TMS')
        self.scene.addItem(self.rect_wms)
        self.scene.addItem(self.rect_tms)
        # Create initial arrow
        self.arrow = ArrowItem(self.rect_wms, self.rect_tms)
        self.scene.addItem(self.arrow)
        """

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

    def save_diagram(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "Diagram Files (*.diag)")
        if filename:
            try:
                with open(filename, 'wb') as f:
                    data = []
                    for item in self.scene.items():
                        if isinstance(item, DraggableRectItem):
                            data.append(('rect', item.label, item.pos().x(), item.pos().y()))
                        elif isinstance(item, ArrowItem):
                            data.append(('arrow', item.startItem.label, item.endItem.label))
                    pickle.dump(data, f)
                    QMessageBox.information(self, "Success", "Diagram saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save diagram: {e}")

    def load_diagram(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Diagram", "", "Diagram Files (*.diag)")
        if filename:
            try:
                with open(filename, 'rb') as f:
                    data = pickle.load(f)
                    self.scene.clear()  # Clear existing items

                    rectangles = {}
                    for item_type, *args in data:
                        if item_type == 'rect':
                            label, x, y = args
                            rect = DraggableRectItem(QRectF(x, y, 100, 50), label)
                            rectangles[label] = rect
                            self.scene.addItem(rect)
                        elif item_type == 'arrow':
                            start_label, end_label = args
                            start_rect = rectangles.get(start_label)
                            end_rect = rectangles.get(end_label)
                            if start_rect and end_rect:
                                arrow = ArrowItem(start_rect, end_rect)
                                self.scene.addItem(arrow)

                    QMessageBox.information(self, "Success", "Diagram loaded successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load diagram: {e}")
