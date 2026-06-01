# Premium Stylesheet for vedi Stock Management App

STYLE_SHEET = """
/* Central and Main Window Styles */
QMainWindow {
    background-color: #f8f9fa;
}

QWidget {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #212529;
}

/* Card layout wrapper to group elements beautifully */
QFrame#cardFrame {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
}

QFrame#statusCard {
    background-color: #e8f5e9;
    border: 1px solid #c8e6c9;
    border-radius: 6px;
}

/* Title and typography styling */
QLabel#mainTitle {
    font-size: 24px;
    font-weight: 700;
    color: #0f172a;
    padding-bottom: 5px;
}

QLabel#sectionTitle {
    font-size: 18px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 10px;
}

QLabel#inputLabel {
    font-size: 13px;
    font-weight: 600;
    color: #495057;
    margin-bottom: 2px;
}

QLabel#successLabel {
    font-size: 14px;
    font-weight: 600;
    color: #2e7d32;
}

QLabel#errorLabel {
    font-size: 13px;
    font-weight: 500;
    color: #d32f2f;
}

/* Form Line Edits (Inputs) */
QLineEdit {
    border: 1px solid #ced4da;
    border-radius: 5px;
    padding: 8px 12px;
    background-color: #ffffff;
    color: #212529;
    font-size: 14px;
}

QLineEdit:hover {
    border: 1px solid #adb5bd;
}

QLineEdit:focus {
    border: 1px solid #86b7fe;
    background-color: #ffffff;
}

/* Combo Box Dropdowns */
QComboBox {
    border: 1px solid #ced4da;
    border-radius: 5px;
    padding: 8px 12px;
    background-color: #ffffff;
    color: #212529;
    font-size: 14px;
    min-width: 100px;
}

QComboBox:hover {
    border: 1px solid #adb5bd;
}

QComboBox:focus {
    border: 1px solid #86b7fe;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left-width: 0px;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}

QComboBox::down-arrow {
    image: none; /* Let's draw a nice clean arrow or use Qt's native arrow if fallback */
    border-top: 5px solid #495057;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    width: 0;
    height: 0;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    border: 1px solid #dee2e6;
    background-color: #ffffff;
    selection-background-color: #0d6efd;
    selection-color: #ffffff;
    outline: 0px;
    padding: 4px;
}

/* Modern Tab Bar Widget styling */
QTabWidget::pane {
    border: none;
    background: transparent;
}

QTabBar::tab {
    background: #e9ecef;
    border: 1px solid #dee2e6;
    border-bottom-color: transparent;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 10px 24px;
    margin-right: 4px;
    font-weight: 600;
    font-size: 14px;
    color: #495057;
}

QTabBar::tab:selected {
    background: #ffffff;
    border-color: #dee2e6;
    border-bottom-color: #ffffff;
    border-top: 3px solid #0d6efd;
    color: #0d6efd;
}

QTabBar::tab:hover:!selected {
    background: #f1f3f5;
    border-color: #e9ecef;
    color: #212529;
}

/* Beautiful Premium Buttons */
QPushButton {
    background-color: #0d6efd;
    color: #ffffff;
    border: 1px solid #0d6efd;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #0b5ed7;
    border-color: #0a58ca;
}

QPushButton:pressed {
    background-color: #0a58ca;
    border-color: #0a58ca;
}

QPushButton:disabled {
    background-color: #6c757d;
    border-color: #6c757d;
    color: #adb5bd;
}

/* Secondary Button styling */
QPushButton#secondaryBtn {
    background-color: #ffffff;
    color: #495057;
    border: 1px solid #ced4da;
}

QPushButton#secondaryBtn:hover {
    background-color: #f8f9fa;
    border-color: #adb5bd;
    color: #212529;
}

QPushButton#secondaryBtn:pressed {
    background-color: #e9ecef;
}

/* Danger Button styling */
QPushButton#dangerBtn {
    background-color: #dc3545;
    color: #ffffff;
    border: 1px solid #dc3545;
}

QPushButton#dangerBtn:hover {
    background-color: #bb2d3b;
    border-color: #b02a37;
}

QPushButton#dangerBtn:pressed {
    background-color: #b02a37;
}

/* Table Widget styling */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    gridline-color: #f1f3f5;
    font-size: 13px;
    outline: none;
}

QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #f1f3f5;
    color: #334155;
}

QTableWidget::item:selected {
    background-color: #e7f1ff;
    color: #0d6efd;
}

QHeaderView::section {
    background-color: #f8f9fa;
    color: #475569;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #dee2e6;
    font-weight: 600;
    font-size: 13px;
    text-align: left;
}

/* Scrollbars styling */
QScrollBar:vertical {
    border: none;
    background: #f1f3f5;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #f1f3f5;
    height: 8px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #cbd5e1;
    min-width: 20px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background: #94a3b8;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""
