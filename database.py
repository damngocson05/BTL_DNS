from __future__ import annotations
import pyodbc
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    def __init__(self, server: str, database: str, trusted_connection: bool = True) -> None:
        self.server = server
        self.database = database
        self.trusted_connection = trusted_connection
        self.conn: Optional[pyodbc.Connection] = None

    def connect(self) -> bool:
        try:
            if self.trusted_connection:
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"Trusted_Connection=yes;"
                )
            else:
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                )
            self.conn = pyodbc.connect(conn_str, timeout=10)
            return True
        except Exception:
            return False

    def connect_master(self) -> Optional[pyodbc.Connection]:
        try:
            if self.trusted_connection:
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE=master;"
                    f"Trusted_Connection=yes;"
                )
            else:
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE=master;"
                )
            return pyodbc.connect(conn_str, timeout=10)
        except Exception:
            return None

    def setup_database(self) -> bool:
        master = self.connect_master()
        if not master:
            return False
        try:
            master.autocommit = True
            cursor = master.cursor()
            cursor.execute(f"""
                IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{self.database}')
                CREATE DATABASE [{self.database}]
            """)
            cursor.close()
            master.close()
        except Exception:
            return False

        if not self.connect():
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='transactions' AND xtype='U')
                CREATE TABLE transactions (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    asset NVARCHAR(20) NOT NULL,
                    asset_type NVARCHAR(20) NOT NULL,
                    side NVARCHAR(10) NOT NULL,
                    quantity FLOAT NOT NULL,
                    price FLOAT NOT NULL,
                    realized_pnl FLOAT DEFAULT 0.0,
                    created_at DATETIME DEFAULT GETDATE()
                )
            """)
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='alerts' AND xtype='U')
                CREATE TABLE alerts (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    asset NVARCHAR(20) NOT NULL,
                    asset_type NVARCHAR(20) NOT NULL,
                    stop_loss FLOAT NULL,
                    take_profit FLOAT NULL,
                    updated_at DATETIME DEFAULT GETDATE(),
                    UNIQUE(asset, asset_type)
                )
            """)
            self.conn.commit()
            cursor.close()
            return True
        except Exception:
            return False

    def is_connected(self) -> bool:
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except Exception:
            return False

    def save_transaction(self, asset: str, asset_type: str, side: str, quantity: float, price: float, realized_pnl: float = 0.0) -> bool:
        if not self.is_connected():
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (asset, asset_type, side, quantity, price, realized_pnl) VALUES (?, ?, ?, ?, ?, ?)",
                (asset.upper(), asset_type, side, quantity, price, realized_pnl)
            )
            self.conn.commit()
            cursor.close()
            return True
        except Exception:
            return False

    def load_transactions(self) -> List[Dict]:
        if not self.is_connected():
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT asset, asset_type, side, quantity, price, realized_pnl, created_at FROM transactions ORDER BY id")
            rows = cursor.fetchall()
            cursor.close()
            transactions = []
            for row in rows:
                transactions.append({
                    "asset": row[0],
                    "asset_type": row[1],
                    "side": row[2],
                    "quantity": row[3],
                    "price": row[4],
                    "realized_pnl": row[5],
                    "created_at": row[6],
                })
            return transactions
        except Exception:
            return []

    def save_alert(self, asset: str, asset_type: str, stop_loss: Optional[float], take_profit: Optional[float]) -> bool:
        if not self.is_connected():
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                IF EXISTS (SELECT 1 FROM alerts WHERE asset = ? AND asset_type = ?)
                    UPDATE alerts SET stop_loss = ?, take_profit = ?, updated_at = GETDATE() WHERE asset = ? AND asset_type = ?
                ELSE
                    INSERT INTO alerts (asset, asset_type, stop_loss, take_profit) VALUES (?, ?, ?, ?)
            """, (asset.upper(), asset_type, stop_loss, take_profit, asset.upper(), asset_type, asset.upper(), asset_type, stop_loss, take_profit))
            self.conn.commit()
            cursor.close()
            return True
        except Exception:
            return False

    def load_alerts(self) -> Dict[str, Dict]:
        if not self.is_connected():
            return {}
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT asset, asset_type, stop_loss, take_profit FROM alerts")
            rows = cursor.fetchall()
            cursor.close()
            alerts = {}
            for row in rows:
                key = f"{row[0]}|{row[1]}"
                alerts[key] = {"stop_loss": row[2], "take_profit": row[3]}
            return alerts
        except Exception:
            return {}

    def delete_alert(self, asset: str, asset_type: str) -> bool:
        if not self.is_connected():
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM alerts WHERE asset = ? AND asset_type = ?", (asset.upper(), asset_type))
            self.conn.commit()
            cursor.close()
            return True
        except Exception:
            return False

    def delete_transactions(self, asset: str, asset_type: str) -> bool:
        if not self.is_connected():
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE asset = ? AND asset_type = ?", (asset.upper(), asset_type))
            self.conn.commit()
            cursor.close()
            return True
        except Exception:
            return False

    def get_transaction_history(self, asset: Optional[str] = None, limit: int = 100) -> List[Dict]:
        if not self.is_connected():
            return []
        try:
            cursor = self.conn.cursor()
            if asset:
                cursor.execute(
                    "SELECT TOP (?) id, asset, asset_type, side, quantity, price, realized_pnl, created_at FROM transactions WHERE asset = ? ORDER BY id DESC",
                    (limit, asset.upper())
                )
            else:
                cursor.execute(
                    "SELECT TOP (?) id, asset, asset_type, side, quantity, price, realized_pnl, created_at FROM transactions ORDER BY id DESC",
                    (limit,)
                )
            rows = cursor.fetchall()
            cursor.close()
            history = []
            for row in rows:
                history.append({
                    "id": row[0],
                    "asset": row[1],
                    "asset_type": row[2],
                    "side": row[3],
                    "quantity": row[4],
                    "price": row[5],
                    "realized_pnl": row[6],
                    "created_at": row[7],
                })
            return history
        except Exception:
            return []

    def close(self) -> None:
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None
