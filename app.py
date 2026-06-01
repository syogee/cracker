import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QTabWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QFont, QDoubleValidator

# Import local database and styles modules
import database
import styles

class StockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize Database
        database.initialize_db()
        
        # Window Configuration
        self.setWindowTitle("vedi - Stock Management")
        self.setMinimumSize(1100, 700)
        self.resize(1150, 750)
        
        # Main layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 20, 30, 30)
        self.main_layout.setSpacing(15)
        
        # Header / Title Bar Area
        self.setup_header()
        
        # Tab Widget Setup
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Initialize Tabs
        self.init_tab_add()
        self.init_tab_edit()
        self.init_tab_search()
        
        # Connect tab change event to refresh edit and search lists
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        # Pre-fill data in search list
        self.refresh_search_table()
        self.refresh_edit_dropdown()
        
    def setup_header(self):
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)
        
        title_label = QLabel("vedi")
        title_label.setObjectName("mainTitle")
        
        subtitle_label = QLabel("Stock & Inventory Manager")
        subtitle_label.setStyleSheet("color: #64748b; font-size: 14px; font-weight: 500;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        # Divider Line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #dee2e6; max-height: 1px; margin-top: 5px;")
        header_layout.addWidget(divider)
        
        self.main_layout.addWidget(header_widget)

    # =========================================================================
    # TAB 1: ADD STOCK ITEM
    # =========================================================================
    def init_tab_add(self):
        self.tab_add = QWidget()
        tab_layout = QVBoxLayout(self.tab_add)
        tab_layout.setContentsMargins(10, 20, 10, 10)
        
        # Core form card frame
        form_card = QFrame()
        form_card.setObjectName("cardFrame")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)
        
        form_title = QLabel("Add New Product")
        form_title.setObjectName("sectionTitle")
        form_layout.addWidget(form_title)
        
        # Grid layout for fields to mimic Bootstrap rows
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Field 1: Name (Full Width)
        lbl_name = QLabel("Product Name")
        lbl_name.setObjectName("inputLabel")
        self.txt_add_name = QLineEdit()
        self.txt_add_name.setPlaceholderText("e.g., Premium Wireless Mouse")
        grid.addWidget(lbl_name, 0, 0, 1, 2)
        grid.addWidget(self.txt_add_name, 1, 0, 1, 2)
        
        # Field 2: Type (Select)
        lbl_type = QLabel("Unit Type")
        lbl_type.setObjectName("inputLabel")
        self.cmb_add_type = QComboBox()
        self.cmb_add_type.addItems(["Piece", "Box"])
        grid.addWidget(lbl_type, 2, 0)
        grid.addWidget(self.cmb_add_type, 3, 0)
        
        # Field 3: Stock Quantity
        lbl_stock = QLabel("Initial Stock")
        lbl_stock.setObjectName("inputLabel")
        self.txt_add_stock = QLineEdit()
        self.txt_add_stock.setPlaceholderText("e.g., 100")
        self.txt_add_stock.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))
        grid.addWidget(lbl_stock, 2, 1)
        grid.addWidget(self.txt_add_stock, 3, 1)
        
        # Field 4: Stock Price
        lbl_stock_price = QLabel("Stock Cost Price ($)")
        lbl_stock_price.setObjectName("inputLabel")
        self.txt_add_stock_price = QLineEdit()
        self.txt_add_stock_price.setPlaceholderText("e.g., 15.50")
        self.txt_add_stock_price.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))
        grid.addWidget(lbl_stock_price, 4, 0)
        grid.addWidget(self.txt_add_stock_price, 5, 0)
        
        # Field 5: Sold Price
        lbl_sold_price = QLabel("Retail Selling Price ($)")
        lbl_sold_price.setObjectName("inputLabel")
        self.txt_add_sold_price = QLineEdit()
        self.txt_add_sold_price.setPlaceholderText("e.g., 29.99")
        self.txt_add_sold_price.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))
        grid.addWidget(lbl_sold_price, 4, 1)
        grid.addWidget(self.txt_add_sold_price, 5, 1)
        
        form_layout.addLayout(grid)
        
        # Error & Success message containers
        self.lbl_add_error = QLabel("")
        self.lbl_add_error.setObjectName("errorLabel")
        self.lbl_add_error.setVisible(False)
        form_layout.addWidget(self.lbl_add_error)
        
        self.card_add_success = QFrame()
        self.card_add_success.setObjectName("statusCard")
        self.card_add_success.setVisible(False)
        success_layout = QHBoxLayout(self.card_add_success)
        success_layout.setContentsMargins(15, 10, 15, 10)
        self.lbl_add_success = QLabel("✔ Product added successfully!")
        self.lbl_add_success.setObjectName("successLabel")
        success_layout.addWidget(self.lbl_add_success)
        form_layout.addWidget(self.card_add_success)
        
        # Buttons Layout
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_clear = QPushButton("Clear Fields")
        btn_clear.setObjectName("secondaryBtn")
        btn_clear.clicked.connect(self.clear_add_form)
        btn_layout.addWidget(btn_clear)
        
        btn_add = QPushButton("Add Product to Inventory")
        btn_add.clicked.connect(self.save_new_product)
        btn_layout.addWidget(btn_add)
        
        form_layout.addLayout(btn_layout)
        form_layout.addStretch()
        
        tab_layout.addWidget(form_card)
        tab_layout.addStretch()
        
        self.tabs.addTab(self.tab_add, "Add Product")

    def clear_add_form(self):
        self.txt_add_name.clear()
        self.txt_add_stock.clear()
        self.txt_add_stock_price.clear()
        self.txt_add_sold_price.clear()
        self.cmb_add_type.setCurrentIndex(0)
        self.lbl_add_error.setVisible(False)

    def save_new_product(self):
        # Retrieve values
        name = self.txt_add_name.text().strip()
        stock = self.txt_add_stock.text().strip()
        stock_price = self.txt_add_stock_price.text().strip()
        sold_price = self.txt_add_sold_price.text().strip()
        piece_or_box = self.cmb_add_type.currentText()
        
        # Validation
        if not name:
            self.show_add_error("Please enter a product name.")
            return
        if not stock:
            self.show_add_error("Please enter initial stock quantity.")
            return
        if not stock_price:
            self.show_add_error("Please enter a valid stock cost price.")
            return
        if not sold_price:
            self.show_add_error("Please enter a valid selling price.")
            return
            
        try:
            stock_val = float(stock)
            stock_p_val = float(stock_price)
            sold_p_val = float(sold_price)
            
            if stock_val < 0 or stock_p_val < 0 or sold_p_val < 0:
                self.show_add_error("Values cannot be negative.")
                return
        except ValueError:
            self.show_add_error("Please enter valid numerical values.")
            return
            
        # Add to DB
        database.add_item(name, stock_val, stock_p_val, sold_p_val, piece_or_box)
        
        # Success visual feedback
        self.lbl_add_error.setVisible(False)
        self.card_add_success.setVisible(True)
        self.clear_add_form()
        
        # Set a timer to hide success label after 3 seconds
        QTimer.singleShot(3000, lambda: self.card_add_success.setVisible(False))

    def show_add_error(self, message):
        self.lbl_add_error.setText(f"❌ {message}")
        self.lbl_add_error.setVisible(True)
        self.card_add_success.setVisible(False)

    # =========================================================================
    # TAB 2: EDIT STOCK ITEM
    # =========================================================================
    def init_tab_edit(self):
        self.tab_edit = QWidget()
        tab_layout = QVBoxLayout(self.tab_edit)
        tab_layout.setContentsMargins(10, 20, 10, 10)
        
        # Form card frame
        form_card = QFrame()
        form_card.setObjectName("cardFrame")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)
        
        form_title = QLabel("Modify Existing Product")
        form_title.setObjectName("sectionTitle")
        form_layout.addWidget(form_title)
        
        # Dropdown selection panel
        select_widget = QWidget()
        select_layout = QHBoxLayout(select_widget)
        select_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_select = QLabel("Select Product:")
        lbl_select.setObjectName("inputLabel")
        lbl_select.setStyleSheet("margin-right: 10px; font-size: 14px;")
        
        self.cmb_edit_select = QComboBox()
        self.cmb_edit_select.setMinimumWidth(300)
        self.cmb_edit_select.currentIndexChanged.connect(self.load_selected_product_details)
        
        select_layout.addWidget(lbl_select)
        select_layout.addWidget(self.cmb_edit_select)
        select_layout.addStretch()
        
        form_layout.addWidget(select_widget)
        
        # Divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #dee2e6; max-height: 1px;")
        form_layout.addWidget(divider)
        
        # Grid layout for edit fields
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Name
        lbl_name = QLabel("Product Name")
        lbl_name.setObjectName("inputLabel")
        self.txt_edit_name = QLineEdit()
        self.txt_edit_name.setPlaceholderText("Select a product above first")
        grid.addWidget(lbl_name, 0, 0, 1, 3)
        grid.addWidget(self.txt_edit_name, 1, 0, 1, 3)
        
        # Type (Col 0)
        lbl_type = QLabel("Unit Type")
        lbl_type.setObjectName("inputLabel")
        self.cmb_edit_type = QComboBox()
        self.cmb_edit_type.addItems(["Piece", "Box"])
        grid.addWidget(lbl_type, 2, 0)
        grid.addWidget(self.cmb_edit_type, 3, 0)
        
        # Current Stock (Col 1)
        lbl_stock = QLabel("Current Stock")
        lbl_stock.setObjectName("inputLabel")
        self.txt_edit_stock = QLineEdit()
        self.txt_edit_stock.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))
        grid.addWidget(lbl_stock, 2, 1)
        grid.addWidget(self.txt_edit_stock, 3, 1)
        
        # Additional Stock to Add (Col 2)
        lbl_add_stock = QLabel("Additional Stock to Add")
        lbl_add_stock.setObjectName("inputLabel")
        lbl_add_stock.setStyleSheet("color: #0d6efd; font-weight: bold;")
        self.txt_edit_add_stock = QLineEdit()
        self.txt_edit_add_stock.setPlaceholderText("e.g., 25 (adds to current)")
        self.txt_edit_add_stock.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))
        grid.addWidget(lbl_add_stock, 2, 2)
        grid.addWidget(self.txt_edit_add_stock, 3, 2)
        
        # Stock Cost Price (Col 0)
        lbl_stock_price = QLabel("Stock Cost Price ($)")
        lbl_stock_price.setObjectName("inputLabel")
        self.txt_edit_stock_price = QLineEdit()
        self.txt_edit_stock_price.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))
        grid.addWidget(lbl_stock_price, 4, 0)
        grid.addWidget(self.txt_edit_stock_price, 5, 0)
        
        # Retail Selling Price (Col 1)
        lbl_sold_price = QLabel("Retail Selling Price ($)")
        lbl_sold_price.setObjectName("inputLabel")
        self.txt_edit_sold_price = QLineEdit()
        self.txt_edit_sold_price.setValidator(QDoubleValidator(0.0, 999999.0, 2, self))
        grid.addWidget(lbl_sold_price, 4, 1)
        grid.addWidget(self.txt_edit_sold_price, 5, 1)
        
        form_layout.addLayout(grid)
        
        # Status/Feedback containers
        self.lbl_edit_error = QLabel("")
        self.lbl_edit_error.setObjectName("errorLabel")
        self.lbl_edit_error.setVisible(False)
        form_layout.addWidget(self.lbl_edit_error)
        
        self.card_edit_success = QFrame()
        self.card_edit_success.setObjectName("statusCard")
        self.card_edit_success.setVisible(False)
        success_layout = QHBoxLayout(self.card_edit_success)
        success_layout.setContentsMargins(15, 10, 15, 10)
        self.lbl_edit_success = QLabel("✔ Changes saved successfully!")
        self.lbl_edit_success.setObjectName("successLabel")
        success_layout.addWidget(self.lbl_edit_success)
        form_layout.addWidget(self.card_edit_success)
        
        # Actions Layout
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_cancel = QPushButton("Reset Changes")
        btn_cancel.setObjectName("secondaryBtn")
        btn_cancel.clicked.connect(self.load_selected_product_details)
        btn_layout.addWidget(btn_cancel)
        
        btn_save = QPushButton("Save Changes")
        btn_save.clicked.connect(self.save_edited_product)
        btn_layout.addWidget(btn_save)
        
        form_layout.addLayout(btn_layout)
        form_layout.addStretch()
        
        tab_layout.addWidget(form_card)
        tab_layout.addStretch()
        
        self.tabs.addTab(self.tab_edit, "Edit Product")

    def refresh_edit_dropdown(self, select_id=None):
        """Loads all database products into the edit dropdown."""
        # Block signals temporarily to prevent index trigger while populating
        self.cmb_edit_select.blockSignals(True)
        self.cmb_edit_select.clear()
        
        items = database.get_all_items()
        self.cmb_edit_select.addItem("-- Choose a product to edit --", None)
        
        selected_index = 0
        for i, item in enumerate(items):
            item_id = item[0]
            item_name = item[1]
            item_type = item[5]
            display_text = f"{item_name} ({item_type.capitalize()}) [ID: {item_id}]"
            self.cmb_edit_select.addItem(display_text, item_id)
            
            # Keep track if we need to select a specific product ID
            if select_id and item_id == select_id:
                selected_index = i + 1  # Offset by 1 for the placeholder item
                
        self.cmb_edit_select.blockSignals(False)
        
        # Select the desired index or default to placeholder
        self.cmb_edit_select.setCurrentIndex(selected_index)
        self.load_selected_product_details()

    def load_selected_product_details(self):
        """Loads the selected product's information into the edit fields."""
        current_data = self.cmb_edit_select.currentData()
        self.lbl_edit_error.setVisible(False)
        self.card_edit_success.setVisible(False)
        
        if current_data is None:
            # Clear all fields and disable them
            self.txt_edit_name.clear()
            self.txt_edit_stock.clear()
            self.txt_edit_add_stock.clear()
            self.txt_edit_stock_price.clear()
            self.txt_edit_sold_price.clear()
            self.cmb_edit_type.setCurrentIndex(0)
            self.set_edit_fields_enabled(False)
            return
            
        # Fetch from DB
        item = database.get_item_by_id(current_data)
        if item:
            self.set_edit_fields_enabled(True)
            self.txt_edit_name.setText(item[1])
            self.txt_edit_stock.setText(str(item[2]))
            self.txt_edit_add_stock.setText("0")  # Default additional stock to 0 when loading
            self.txt_edit_stock_price.setText(str(item[3]))
            self.txt_edit_sold_price.setText(str(item[4]))
            
            # Select Piece or Box
            t_index = self.cmb_edit_type.findText(item[5].capitalize())
            if t_index >= 0:
                self.cmb_edit_type.setCurrentIndex(t_index)

    def set_edit_fields_enabled(self, enabled):
        self.txt_edit_name.setEnabled(enabled)
        self.cmb_edit_type.setEnabled(enabled)
        self.txt_edit_stock.setEnabled(enabled)
        self.txt_edit_add_stock.setEnabled(enabled)
        self.txt_edit_stock_price.setEnabled(enabled)
        self.txt_edit_sold_price.setEnabled(enabled)

    def save_edited_product(self):
        item_id = self.cmb_edit_select.currentData()
        if item_id is None:
            self.show_edit_error("Please select a valid product first.")
            return
            
        name = self.txt_edit_name.text().strip()
        stock = self.txt_edit_stock.text().strip()
        add_stock = self.txt_edit_add_stock.text().strip() or "0"
        stock_price = self.txt_edit_stock_price.text().strip()
        sold_price = self.txt_edit_sold_price.text().strip()
        piece_or_box = self.cmb_edit_type.currentText()
        
        # Validation
        if not name:
            self.show_edit_error("Please enter a product name.")
            return
        if not stock:
            self.show_edit_error("Please enter current stock quantity.")
            return
        if not stock_price:
            self.show_edit_error("Please enter a valid stock cost price.")
            return
        if not sold_price:
            self.show_edit_error("Please enter a valid retail selling price.")
            return
            
        try:
            stock_base = float(stock)
            stock_add = float(add_stock)
            stock_p_val = float(stock_price)
            sold_p_val = float(sold_price)
            
            if stock_base < 0 or stock_p_val < 0 or sold_p_val < 0:
                self.show_edit_error("Stock quantities and prices cannot be negative.")
                return
                
            # Increment stock!
            stock_val = stock_base + stock_add
            if stock_val < 0:
                self.show_edit_error("Total stock quantity cannot be negative.")
                return
        except ValueError:
            self.show_edit_error("Please enter valid numerical values.")
            return
            
        # Update in database
        database.update_item(item_id, name, stock_val, stock_p_val, sold_p_val, piece_or_box)
        
        self.lbl_edit_error.setVisible(False)
        self.card_edit_success.setVisible(True)
        
        # Refresh the search grid and re-populate edit dropdown, keeping current item selected
        self.refresh_edit_dropdown(item_id)
        
        QTimer.singleShot(3000, lambda: self.card_edit_success.setVisible(False))

    def show_edit_error(self, message):
        self.lbl_edit_error.setText(f"❌ {message}")
        self.lbl_edit_error.setVisible(True)
        self.card_edit_success.setVisible(False)

    # =========================================================================
    # TAB 3: SEARCH, FILTER, DELETE & VIEW ALL
    # =========================================================================
    def init_tab_search(self):
        self.tab_search = QWidget()
        tab_layout = QVBoxLayout(self.tab_search)
        tab_layout.setContentsMargins(10, 20, 10, 10)
        
        # Search & Filter Card Panel
        filter_card = QFrame()
        filter_card.setObjectName("cardFrame")
        filter_layout = QVBoxLayout(filter_card)
        filter_layout.setContentsMargins(20, 20, 20, 20)
        filter_layout.setSpacing(15)
        
        filter_title = QLabel("Inventory Overview")
        filter_title.setObjectName("sectionTitle")
        filter_layout.addWidget(filter_title)
        
        # Search layout controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        # Text Search
        search_v_layout = QVBoxLayout()
        search_v_layout.setSpacing(3)
        lbl_search = QLabel("Search Name")
        lbl_search.setObjectName("inputLabel")
        self.txt_search_query = QLineEdit()
        self.txt_search_query.setPlaceholderText("Type to filter products instantly...")
        self.txt_search_query.textChanged.connect(self.on_search_filters_changed)
        search_v_layout.addWidget(lbl_search)
        search_v_layout.addWidget(self.txt_search_query)
        controls_layout.addLayout(search_v_layout, 3)
        
        # Type Select
        type_v_layout = QVBoxLayout()
        type_v_layout.setSpacing(3)
        lbl_filter_type = QLabel("Unit Type")
        lbl_filter_type.setObjectName("inputLabel")
        self.cmb_filter_type = QComboBox()
        self.cmb_filter_type.addItems(["All", "Piece", "Box"])
        self.cmb_filter_type.currentIndexChanged.connect(self.on_search_filters_changed)
        type_v_layout.addWidget(lbl_filter_type)
        type_v_layout.addWidget(self.cmb_filter_type)
        controls_layout.addLayout(type_v_layout, 1)
        
        # Action Buttons
        btn_v_layout = QVBoxLayout()
        btn_v_layout.setSpacing(3)
        btn_v_layout.addWidget(QLabel("")) # Spacer label
        btn_show_all = QPushButton("Show All")
        btn_show_all.setObjectName("secondaryBtn")
        btn_show_all.clicked.connect(self.reset_search_filters)
        btn_v_layout.addWidget(btn_show_all)
        controls_layout.addLayout(btn_v_layout, 1)
        
        filter_layout.addLayout(controls_layout)
        tab_layout.addWidget(filter_card)
        
        # Results Table Panel
        self.table_card = QFrame()
        self.table_card.setObjectName("cardFrame")
        table_card_layout = QVBoxLayout(self.table_card)
        table_card_layout.setContentsMargins(15, 15, 15, 15)
        
        # QTableWidget Initialization
        self.tbl_results = QTableWidget()
        self.tbl_results.setColumnCount(10)
        self.tbl_results.setHorizontalHeaderLabels([
            "ID", "Product Name", "Type", "Stock", 
            "Stock Cost", "Retail Sell", "Total Cost Value", "Total Sales Value",
            "Created Date", "Last Updated"
        ])
        
        # Style table headers
        header = self.tbl_results.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Product Name stretches
        
        self.tbl_results.setSelectionBehavior(QTableWidget.SelectRows)
        self.tbl_results.setSelectionMode(QTableWidget.SingleSelection)
        self.tbl_results.itemSelectionChanged.connect(self.on_table_row_selected)
        
        table_card_layout.addWidget(self.tbl_results)
        
        # Table Selection Management Actions Panel
        self.actions_bar = QHBoxLayout()
        self.actions_bar.setContentsMargins(5, 5, 5, 5)
        
        self.lbl_selected_status = QLabel("Select an item to view actions")
        self.lbl_selected_status.setStyleSheet("color: #64748b; font-weight: 500; font-size: 13px;")
        self.actions_bar.addWidget(self.lbl_selected_status)
        self.actions_bar.addStretch()
        
        self.btn_edit_selected = QPushButton("Edit Selected")
        self.btn_edit_selected.setObjectName("secondaryBtn")
        self.btn_edit_selected.setEnabled(False)
        self.btn_edit_selected.clicked.connect(self.edit_selected_item)
        self.actions_bar.addWidget(self.btn_edit_selected)
        
        self.btn_delete_selected = QPushButton("Delete Selected")
        self.btn_delete_selected.setObjectName("dangerBtn")
        self.btn_delete_selected.setEnabled(False)
        self.btn_delete_selected.clicked.connect(self.delete_selected_item)
        self.actions_bar.addWidget(self.btn_delete_selected)
        
        table_card_layout.addLayout(self.actions_bar)
        
        tab_layout.addWidget(self.table_card)
        
        self.tabs.addTab(self.tab_search, "Search & Manage")

    def on_search_filters_changed(self):
        """Triggered whenever user inputs search text or changes type selection."""
        self.refresh_search_table()

    def reset_search_filters(self):
        """Clears text searches and resets dropdown filter to 'All'."""
        self.txt_search_query.clear()
        self.cmb_filter_type.setCurrentIndex(0)
        self.refresh_search_table()

    def refresh_search_table(self):
        """Fetches filtered items from database and populates the table."""
        query = self.txt_search_query.text().strip()
        unit_type = self.cmb_filter_type.currentText()
        
        items = database.search_items(query, unit_type)
        
        self.tbl_results.blockSignals(True)
        self.tbl_results.setRowCount(0)
        
        for row_idx, item in enumerate(items):
            self.tbl_results.insertRow(row_idx)
            
            # Values
            item_id = item[0]
            name = item[1]
            stock = item[2]
            stock_price = item[3]
            sold_price = item[4]
            piece_or_box = item[5].capitalize()
            created_at = item[6]
            updated_at = item[7]
            
            total_stock_value = stock * stock_price
            total_sold_value = stock * sold_price
            
            # Map values into table items
            # ID (col 0)
            id_item = QTableWidgetItem(str(item_id))
            id_item.setFlags(id_item.flags() ^ Qt.ItemIsEditable)
            id_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_results.setItem(row_idx, 0, id_item)
            
            # Name (col 1)
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)
            self.tbl_results.setItem(row_idx, 1, name_item)
            
            # Type (col 2)
            type_item = QTableWidgetItem(piece_or_box)
            type_item.setFlags(type_item.flags() ^ Qt.ItemIsEditable)
            type_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_results.setItem(row_idx, 2, type_item)
            
            # Stock (col 3)
            # Format as integer if it represents a whole number, otherwise standard decimal
            stock_str = f"{int(stock)}" if stock.is_integer() else f"{stock:.2f}"
            stock_item = QTableWidgetItem(stock_str)
            stock_item.setFlags(stock_item.flags() ^ Qt.ItemIsEditable)
            stock_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tbl_results.setItem(row_idx, 3, stock_item)
            
            # Stock Price (col 4)
            s_price_item = QTableWidgetItem(f"${stock_price:.2f}")
            s_price_item.setFlags(s_price_item.flags() ^ Qt.ItemIsEditable)
            s_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tbl_results.setItem(row_idx, 4, s_price_item)
            
            # Sold Price (col 5)
            sold_price_item = QTableWidgetItem(f"${sold_price:.2f}")
            sold_price_item.setFlags(sold_price_item.flags() ^ Qt.ItemIsEditable)
            sold_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tbl_results.setItem(row_idx, 5, sold_price_item)
            
            # Total Cost Value (col 6)
            total_cost_item = QTableWidgetItem(f"${total_stock_value:.2f}")
            total_cost_item.setFlags(total_cost_item.flags() ^ Qt.ItemIsEditable)
            total_cost_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tbl_results.setItem(row_idx, 6, total_cost_item)
            
            # Total Sales Value (col 7)
            total_sales_item = QTableWidgetItem(f"${total_sold_value:.2f}")
            total_sales_item.setFlags(total_sales_item.flags() ^ Qt.ItemIsEditable)
            total_sales_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tbl_results.setItem(row_idx, 7, total_sales_item)
            
            # Created Date (col 8)
            created_item = QTableWidgetItem(created_at)
            created_item.setFlags(created_item.flags() ^ Qt.ItemIsEditable)
            created_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_results.setItem(row_idx, 8, created_item)
            
            # Last Updated (col 9)
            updated_item = QTableWidgetItem(updated_at)
            updated_item.setFlags(updated_item.flags() ^ Qt.ItemIsEditable)
            updated_item.setTextAlignment(Qt.AlignCenter)
            self.tbl_results.setItem(row_idx, 9, updated_item)
            
        self.tbl_results.blockSignals(False)
        
        # Reset actions state since list loaded afresh
        self.on_table_row_selected()

    def on_table_row_selected(self):
        """Called whenever the selection state of the table changes."""
        selected_ranges = self.tbl_results.selectedRanges()
        if not selected_ranges:
            self.lbl_selected_status.setText("Select an item to view actions")
            self.btn_edit_selected.setEnabled(False)
            self.btn_delete_selected.setEnabled(False)
            return
            
        row = selected_ranges[0].topRow()
        item_id = self.tbl_results.item(row, 0).text()
        item_name = self.tbl_results.item(row, 1).text()
        item_type = self.tbl_results.item(row, 2).text()
        
        self.lbl_selected_status.setText(f"Selected: <b>{item_name}</b> ({item_type}) [ID: {item_id}]")
        self.btn_edit_selected.setEnabled(True)
        self.btn_delete_selected.setEnabled(True)

    def edit_selected_item(self):
        """Switches to the Edit tab and triggers edit pre-filling for the selected item."""
        selected_ranges = self.tbl_results.selectedRanges()
        if not selected_ranges:
            return
            
        row = selected_ranges[0].topRow()
        item_id = int(self.tbl_results.item(row, 0).text())
        
        # Trigger edit dropdown selection update
        self.refresh_edit_dropdown(item_id)
        
        # Switch to Tab 2 (Edit tab - Index 1)
        self.tabs.setCurrentIndex(1)

    def delete_selected_item(self):
        """Asks for confirmation and deletes the selected stock item from database."""
        selected_ranges = self.tbl_results.selectedRanges()
        if not selected_ranges:
            return
            
        row = selected_ranges[0].topRow()
        item_id = int(self.tbl_results.item(row, 0).text())
        item_name = self.tbl_results.item(row, 1).text()
        
        # Confirmation Dialog
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to permanently delete \"{item_name}\" from your inventory?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete in Database
            database.delete_item(item_id)
            # Refresh both views
            self.refresh_search_table()
            self.refresh_edit_dropdown()
            
            QMessageBox.information(
                self,
                "Item Deleted",
                f"Successfully deleted \"{item_name}\" from stock.",
                QMessageBox.Ok
            )

    # =========================================================================
    # APP CONTROLS
    # =========================================================================
    def on_tab_changed(self, index):
        """Runs whenever tabs are changed to ensure fresh data in dropdowns/tables."""
        if index == 1: # Edit Tab
            # Cache the current selected ID if any, and refresh dropdown list
            current_selected = self.cmb_edit_select.currentData()
            self.refresh_edit_dropdown(current_selected)
        elif index == 2: # Search Tab
            self.refresh_search_table()

def main():
    app = QApplication(sys.argv)
    
    # Load fonts or configure smooth antialiasing
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Apply Premium Theme Styling (QSS)
    app.setStyleSheet(styles.STYLE_SHEET)
    
    window = StockApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
