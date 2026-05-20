# Copy this file to config.py và điền token/chat ID của bạn
# Hoặc tạo file .env với các biến: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
PRICE_POLL_INTERVAL_SECONDS = 10

# Binance API (để trống nếu chỉ dùng giá công khai)
BINANCE_API_KEY = ""
BINANCE_API_SECRET = ""

# SQL Server (để trống nếu muốn dùng JSON thay vì database)
SQL_SERVER = "localhost"           # hoặc "localhost\\SQLEXPRESS"
SQL_DATABASE = "PortfolioDB"
SQL_TRUSTED_CONNECTION = True      # True = Windows Authentication
