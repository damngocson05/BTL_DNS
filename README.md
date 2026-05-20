# Hệ thống quản lý danh mục đầu tư và cảnh báo giá

Dự án này là một hệ thống Python để quản lý danh mục đầu tư crypto/cổ phiếu, tính toán điểm hòa vốn và lãi/lỗ theo lịch sử giao dịch, cập nhật giá theo nền tảng `threading`, và gửi cảnh báo qua Telegram khi giá chạm ngưỡng.

## Tính năng

- Quản lý danh mục đầu tư bằng các giao dịch `buy` / `sell`
- Tính toán:
  - Giá nhập trung bình (break-even)
  - Lợi nhuận/thua lỗ thực tế (realized PnL)
  - Lợi nhuận/thua lỗ chưa thực hiện (unrealized PnL)
  - Tổng PnL
- Cập nhật giá không làm đơ giao diện bằng luồng nền
- Lấy giá crypto từ CoinGecko API
- Lấy giá cổ phiếu từ Yahoo Finance (`yfinance`)
- Gửi cảnh báo Telegram khi đạt ngưỡng cắt lỗ/chốt lời
- Giao diện đơn giản bằng Tkinter

## Yêu cầu

- Python 3.10+
- `requests`
- `yfinance`

## Cài đặt

1. Cài dependencies:
```powershell
python -m pip install -r requirements.txt
```

2. Tạo file cấu hình:
```powershell
copy config_example.py config.py
```

3. Mở `config.py` và điền `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`.

4. Chạy ứng dụng:
```powershell
python app.py
```

## Lưu ý

- Nếu không sử dụng Telegram, hệ thống vẫn chạy bình thường nhưng sẽ không gửi tin nhắn.
- `CoinGecko` cung cấp giá crypto, `yfinance` cung cấp giá cổ phiếu.
- Bạn có thể thêm tài sản mới và đặt ngưỡng stop-loss / take-profit.
