# Portfolio Manager & Price Alert System

Hệ thống quản lý danh mục đầu tư và cảnh báo giá tiền điện tử/cổ phiếu. Tích hợp Binance API, Telegram Bot API, SQL Server, đa luồng cập nhật giá realtime.

## Tính năng chính

### Quản lý danh mục (Portfolio)
- Thêm giao dịch mua/bán (buy/sell)
- Tính toán PnL theo phương pháp FIFO (First In First Out)
- Điểm hòa vốn (break-even), giá vốn trung bình
- Lãi/lỗ đã thực hiện (realized PnL) và chưa thực hiện (unrealized PnL)

### Tích hợp API
- **Binance API**: Giá crypto theo thời gian thực, lịch sử giao dịch, số dư tài khoản, biểu đồ nến
- **Yahoo Finance**: Giá cổ phiếu (AAPL, GOOGL, TSLA...)
- **Telegram Bot API**: Cảnh báo tự động khi giá chạm ngưỡng cắt lỗ/chốt lời

### Đa luồng (Threading)
- Cập nhật giá nền không làm đơ giao diện
- Queue thread-safe cho giao tiếp giữa luồng nền và GUI

### Cảnh báo thông minh
- Đặt ngưỡng Stop-loss (cắt lỗ) và Take-profit (chốt lời)
- Tự động gửi tin nhắn Telegram khi giá chạm ngưỡng
- De-duplication: không spam tin nhắn khi giá dao động quanh ngưỡng

### Cơ sở dữ liệu
- SQL Server (pyodbc) lưu trữ giao dịch và cảnh báo
- Tự động tạo database và tables khi khởi động lần đầu
- Fallback sang JSON nếu SQL Server không khả dụng

### Biểu đồ
- Candlestick chart (biểu đồ nến) cho crypto
- Nhiều khung thời gian: 1m, 5m, 15m, 1h, 4h, 1d
- Volume bars

### Giao diện
- Dark theme và Light theme (chuyển đổi bằng nút bấm)
- Treeview hiển thị danh mục với màu sắc theo lãi/lỗ
- Nhật ký (log) thời gian thực
- Menu bar đầy đủ

## Cài đặt

### Yêu cầu
- Python 3.10+
- SQL Server (tùy chọn, có fallback JSON)
- ODBC Driver 17 for SQL Server (nếu dùng database)

### Bước 1: Cài dependencies
```bash
pip install -r requirements.txt
```

### Bước 2: Cấu hình
```bash
copy config_example.py config.py
```

Mở `config.py` và điền các thông tin:

```python
# Telegram Bot (bắt buộc để nhận cảnh báo)
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

# Binance API (tùy chọn, để trống vẫn lấy giá được)
BINANCE_API_KEY = ""
BINANCE_API_SECRET = ""

# SQL Server (tùy chọn, để trống dùng JSON)
SQL_SERVER = "localhost"
SQL_DATABASE = "PortfolioDB"
SQL_TRUSTED_CONNECTION = True
```

### Bước 3: Chạy
```bash
python app.py
```

## Cách sử dụng

### Thêm giao dịch
1. Nhập mã tài sản (ví dụ: BTC, ETH, AAPL)
2. Chọn loại: Crypto hoặc Stock
3. Chọn hình thức: Buy (mua) hoặc Sell (bán)
4. Nhập số lượng và giá giao dịch
5. Nhấn **Thêm giao dịch**

### Đặt cảnh báo
1. Nhập mã tài sản đã thêm
2. Nhập Stop-loss (giá cắt lỗ) và Take-profit (giá chốt lời)
3. Nhấn **Cập nhật ngưỡng**
4. Bấm **Bắt đầu cập nhật giá** → Telegram tự động cảnh báo khi giá chạm ngưỡng

### Xem biểu đồ
1. Nhập mã crypto (ví dụ BTC)
2. Bấm **Biểu đồ**
3. Chọn khung thời gian và nhấn **Vẽ biểu đồ**

### Kết nối Binance
- **Xem số dư**: Xem tất cả tài sản trên Binance
- **Lịch sử giao dịch**: Xem lệnh gần nhất
- **Lệnh đang mở**: Xem các lệnh chờ

## Cấu trúc dự án

```
├── app.py                 # Giao diện chính (Tkinter)
├── api_client.py          # API client (Binance + Yahoo Finance)
├── portfolio_manager.py   # Logic quản lý danh mục (FIFO PnL)
├── database.py            # Quản lý SQL Server
├── telegram_alert.py      # Telegram Bot API
├── config_example.py      # Template cấu hình
├── .env.example           # Template biến môi trường
├── requirements.txt       # Dependencies
└── README.md              # Tài liệu
```

## Đóng gói thành exe

```bash
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed --name "PortfolioManager" app.py
```

File exe sẽ nằm trong thư mục `dist/PortfolioManager/`.

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Giao diện | Tkinter |
| API crypto | Binance API (REST) |
| API cổ phiếu | Yahoo Finance (yfinance) |
| Thông báo | Telegram Bot API |
| Database | SQL Server (pyodbc) |
| Biểu đồ | matplotlib + mplfinance |
| Đa luồng | threading + queue |
| Đóng gói | PyInstaller |
