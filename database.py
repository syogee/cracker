import sqlite3
import os

DB_NAME = "vedi_stock.db"

def get_db_path():
    # Keep the database file inside the workspace
    return os.path.abspath(DB_NAME)

def initialize_db():
    """Initializes the SQLite database, creates table, and runs migration for updated_at if needed."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Create table with updated_at column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            stock REAL NOT NULL,
            stock_price REAL NOT NULL,
            sold_price REAL NOT NULL,
            piece_or_box TEXT NOT NULL CHECK(piece_or_box IN ('piece', 'box')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Safe schema migration check to add updated_at to existing databases without data loss
    cursor.execute("PRAGMA table_info(stock_items)")
    columns = [col[1] for col in cursor.fetchall()]
    if columns and "updated_at" not in columns:
        cursor.execute("ALTER TABLE stock_items ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
    conn.commit()
    conn.close()

def add_item(name, stock, stock_price, sold_price, piece_or_box):
    """Adds a new stock item. Returns the ID of the new item."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO stock_items (name, stock, stock_price, sold_price, piece_or_box)
        VALUES (?, ?, ?, ?, ?)
    """, (name, float(stock), float(stock_price), float(sold_price), piece_or_box.lower()))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def update_item(item_id, name, stock, stock_price, sold_price, piece_or_box):
    """Updates an existing stock item's fields by ID and sets updated_at to CURRENT_TIMESTAMP."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE stock_items
        SET name = ?, stock = ?, stock_price = ?, sold_price = ?, piece_or_box = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (name, float(stock), float(stock_price), float(sold_price), piece_or_box.lower(), int(item_id)))
    conn.commit()
    conn.close()

def delete_item(item_id):
    """Deletes a stock item by ID."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stock_items WHERE id = ?", (int(item_id),))
    conn.commit()
    conn.close()

def get_all_items():
    """Fetches all stock items from the database, ordered by ID descending, including timestamps."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, stock, stock_price, sold_price, piece_or_box, created_at, updated_at
        FROM stock_items
        ORDER BY id DESC
    """)
    items = cursor.fetchall()
    conn.close()
    return items

def search_items(query="", unit_type="All"):
    """Searches stock items by name and/or filters by piece_or_box type, returning all columns."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    sql = "SELECT id, name, stock, stock_price, sold_price, piece_or_box, created_at, updated_at FROM stock_items WHERE 1=1"
    params = []
    
    if query:
        sql += " AND name LIKE ?"
        params.append(f"%{query}%")
        
    if unit_type and unit_type.lower() != "all":
        sql += " AND piece_or_box = ?"
        params.append(unit_type.lower())
        
    sql += " ORDER BY id DESC"
    
    cursor.execute(sql, params)
    items = cursor.fetchall()
    conn.close()
    return items

def get_item_by_id(item_id):
    """Retrieves a single stock item by its ID, returning all columns."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, stock, stock_price, sold_price, piece_or_box, created_at, updated_at
        FROM stock_items
        WHERE id = ?
    """, (int(item_id),))
    item = cursor.fetchone()
    conn.close()
    return item
