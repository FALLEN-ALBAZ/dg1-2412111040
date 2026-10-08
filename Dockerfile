# 1. Image nền python alpine siêu nhẹ, tải nhanh
FROM python:3.11-alpine

# 2. Thư mục làm việc
WORKDIR /app

# 3. Cài đặt thư viện trước để cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Sao chép mã nguồn
COPY app/ ./app/

# 5. Tạo user không phải root trên Alpine (dùng adduser)
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

# 6. Khai báo cổng
EXPOSE 5000

# 7. Lệnh chạy
CMD ["python", "app/app.py"]# 1. Image nền python slim
FROM python:3.11-slim

# 2. Thiết lập thư mục làm việc trong container
WORKDIR /app

# 3. Cài đặt thư viện trước khi sao chép mã nguồn (tối ưu cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Sao chép toàn bộ mã nguồn ứng dụng vào container
COPY app/ ./app/

# 5. Tạo và chuyển sang người dùng không phải root (bảo mật)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 6. Khai báo cổng ứng dụng lắng nghe
EXPOSE 5000

# 7. Lệnh khởi chạy ứng dụng
CMD ["python", "app/app.py"]
