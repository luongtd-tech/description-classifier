# Hệ thống phân loại sản phẩm dựa trên mô tả

> **Đơn vị**: Trường Kỹ thuật và Công nghệ - Trường Đại học Vinh
> **Học phần**: Xử lý ngôn ngữ tự nhiên
> **Hướng dẫn**: TS. Trần Xuân Sang  
> **Thực hiện**: Trần Đức Lương  
> **Mô tả**: Dự án xây dựng hệ thống tự động phân loại mô tả sản phẩm thương mại điện tử sử dụng thuật toán Naive Bayes, được triển khai dưới hai hình thức: ứng dụng Desktop và giao diện Website.

---

## Mục lục

1. [Giới thiệu](#1-giới-thiệu)
2. [Cấu trúc thư mục](#2-cấu-trúc-thư-mục)
3. [Yêu cầu cài đặt](#3-yêu-cầu-cài-đặt)
4. [Dữ liệu](#4-dữ-liệu)
5. [Các module cốt lõi](#5-các-module-cốt-lõi)
6. [Bài tập thực hành](#6-bài-tập-thực-hành)
7. [Ứng dụng Desktop](#7-ứng-dụng-desktop)
8. [Ứng dụng Website](#8-ứng-dụng-website)
9. [Hướng dẫn chạy](#9-hướng-dẫn-chạy)
10. [Kết quả minh họa](#10-kết-quả-minh-họa)
11. [Triển khai trên Render](#11-triển-khai-trên-render)

---

## 1. Giới thiệu

Dự án gồm hai bài tập chính:

| Bài tập | Nội dung |
|---------|----------|
| **Bài tập 1** (`ex_1.py`) | Tiền xử lý ngôn ngữ tự nhiên: đếm từ, chuyển chữ thường, xóa dấu câu, xóa khoảng trắng thừa |
| **Bài tập 2** (`ex_2.py`) | Xây dựng bộ phân loại Naive Bayes từ đầu (không dùng thư viện ML), huấn luyện và dự đoán nhãn sản phẩm |

Ngoài ra, dự án còn cung cấp:
- **Ứng dụng Desktop** (`desktop/app.py`): giao diện đồ họa bằng CustomTkinter
- **Ứng dụng Website** (`web/main.py`): API REST bằng FastAPI + giao diện web hiện đại

---

## 2. Cấu trúc thư mục

```
description-classifier/
│
├── core/                       # Các module dùng chung cho toàn dự án
│   ├── nlp_utils.py            # Hàm tiền xử lý văn bản (NLP)
│   ├── classifier.py           # Lớp NaiveBayesClassifier
│   └── data_handler.py         # Đọc và phân tích file CSV
│
├── data/                       # Dữ liệu huấn luyện
│   ├── data.json               # Dữ liệu chính (50 mẫu, định dạng JSON)
│   └── data.csv                # Dữ liệu mẫu (dùng để test tính năng tải file)
│
├── exercises/                  # Bài tập thực hành chạy trên terminal
│   ├── ex_1.py                 # Bài tập 1: Tiền xử lý NLP
│   └── ex_2.py                 # Bài tập 2: Phân loại Naive Bayes
│
├── desktop/                    # Ứng dụng giao diện đồ họa
│   └── app.py                  # Ứng dụng Desktop (CustomTkinter)
│
├── web/                        # Ứng dụng web
│   ├── main.py                 # FastAPI server (backend)
│   ├── static/
│   │   ├── style.css           # Giao diện (glassmorphism, dark mode)
│   │   └── script.js           # Xử lý tương tác phía client
│   └── templates/
│       └── index.html          # Trang HTML chính
│
├── requirements.txt            # Danh sách thư viện cần cài đặt
└── README.md                   # Tài liệu hướng dẫn (file này)
```

### Lý do tổ chức như vậy

- **`core/`** chứa logic nghiệp vụ thuần túy, không phụ thuộc vào bất kỳ giao diện nào. Cả `exercises/`, `desktop/` và `web/` đều import từ đây.
- **`exercises/`** tách riêng để từng bài tập có thể chạy độc lập qua terminal, phục vụ mục đích học tập và báo cáo.
- **`web/`** tổ chức theo chuẩn FastAPI: `main.py` là server, `static/` chứa CSS/JS, `templates/` chứa HTML.

---

## 3. Yêu cầu cài đặt

### Phiên bản Python

Yêu cầu **Python 3.9 trở lên**.

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Nội dung `requirements.txt`:

| Thư viện | Công dụng |
|----------|-----------|
| `fastapi` | Framework web để xây dựng API |
| `uvicorn` | ASGI server để chạy FastAPI |
| `python-multipart` | Xử lý form data và file upload |
| `jinja2` | Render template HTML phía server |
| `customtkinter` | Xây dựng giao diện desktop hiện đại |

> **Lưu ý:** Các thuật toán NLP và Naive Bayes trong dự án này được **tự cài đặt từ đầu**, không dùng `scikit-learn`, `nltk` hay bất kỳ thư viện ML nào.

---

## 4. Dữ liệu

### `data/data.json`

File dữ liệu chính với **50 mẫu** gồm 5 nhãn phân loại:

| Nhãn | Số mẫu | Ví dụ |
|------|--------|-------|
| Điện thoại | 10 | "Điện thoại iPhone 14 Pro Max 256GB chính hãng VNA" |
| Máy tính | 10 | "Laptop Dell XPS 15 Core i7 RAM 16GB SSD 512GB" |
| Thời trang | 10 | "Áo sơ mi nam Oxford tay dài form Regular" |
| Mỹ phẩm | 10 | "Kem chống nắng Anessa SPF 50+ PA++++ chống nước" |
| Đồ gia dụng | 10 | "Nồi chiên không dầu Philips 5 lít bảo hành 2 năm" |

Định dạng từng phần tử:
```json
{
    "text": "Điện thoại iPhone 14 Pro Max 256GB chính hãng VNA",
    "label": "Điện thoại"
}
```

### `data/data.csv`

File CSV dùng để kiểm tra tính năng **tải file hàng loạt** trong ứng dụng Desktop và Website. Mỗi dòng là một mô tả sản phẩm (không có nhãn).

```
text
Điện thoại iPhone 14 Pro Max 256GB chính hãng VNA
Laptop Dell XPS 15 Core i7 RAM 16GB SSD 512GB
...
```

---

## 5. Các module cốt lõi

### `core/nlp_utils.py` — Tiền xử lý văn bản

| Hàm | Đầu vào | Đầu ra | Mô tả |
|-----|---------|--------|-------|
| `lower_case(text)` | chuỗi | chuỗi | Chuyển toàn bộ ký tự thành chữ thường |
| `remove_punctuation(text)` | chuỗi | chuỗi | Xóa tất cả ký tự dấu câu |
| `remove_whitespace(text)` | chuỗi | chuỗi | Xóa khoảng trắng đầu, cuối và thừa giữa các từ |
| `count_words(text)` | chuỗi | số nguyên | Đếm số từ sau khi làm sạch |
| `preprocess(text)` | chuỗi | chuỗi | Áp dụng toàn bộ 3 bước trên theo thứ tự |

**Quy trình tiền xử lý (`preprocess`):**
```
Văn bản gốc
    → lower_case()        (chữ thường)
    → remove_punctuation() (xóa dấu câu)
    → remove_whitespace()  (xóa khoảng trắng thừa)
    → kết quả sạch
```

---

### `core/classifier.py` — Bộ phân loại Naive Bayes

Lớp `NaiveBayesClassifier` triển khai thuật toán **Multinomial Naive Bayes** với **Laplace Smoothing**:

**Công thức tính điểm:**

```
log P(nhãn | văn bản) = log P(nhãn) + Σ log P(từ | nhãn)
```

Trong đó:
- `P(nhãn) = số văn bản nhãn / tổng văn bản`
- `P(từ | nhãn) = (số lần từ xuất hiện trong nhãn + 1) / (tổng từ trong nhãn + kích thước từ vựng)`
  *(+1 là Laplace Smoothing để tránh xác suất bằng 0)*

**Phương thức chính:**

| Phương thức | Mô tả |
|-------------|-------|
| `train(dataset)` | Huấn luyện mô hình từ danh sách `[{text, label}]` |
| `predict(text)` | Dự đoán nhãn và trả về xác suất (%) cho từng nhãn |

**Kết quả trả về của `predict()`:**
```python
{
    "predicted_label": "Điện thoại",       # nhãn dự đoán
    "scores":          { ... },             # điểm log-probability gốc
    "probabilities":   { "Điện thoại": 98.97, ... },  # xác suất chuẩn hóa (%)
    "comment":         "Văn bản này có xác suất..."   # nhận xét tự động
}
```

---

### `core/data_handler.py` — Đọc file CSV

Hàm `parse_csv_file(file_content)`:
- Nhận vào dữ liệu bytes của file CSV
- Trả về danh sách các chuỗi văn bản
- Tự động bỏ qua dòng tiêu đề nếu có (phát hiện các từ khóa: `text`, `description`, `mô tả`, `mota`)

---

## 6. Bài tập thực hành

### Bài tập 1 — `exercises/ex_1.py`

Minh họa từng bước tiền xử lý NLP trên toàn bộ 50 văn bản trong `data.json`.

**Chạy:**
```bash
python exercises\ex_1.py
```

**Kết quả mẫu:**
```
==========================================================================================
                        BÀI TẬP 1: TIỀN XỬ LÝ NGÔN NGỮ TỰ NHIÊN
==========================================================================================

Tổng số văn bản cần xử lý: 50

------------------------------------------------------------------------------------------
[1] VĂN BẢN GỐC      : 'Điện thoại iPhone 14 Pro Max 256GB chính hãng VNA'
    Số từ                 : 9
    Chuyển chữ thường     : điện thoại iphone 14 pro max 256gb chính hãng vna
    Xóa dấu câu           : Điện thoại iPhone 14 Pro Max 256GB chính hãng VNA
    Xóa khoảng trắng      : Điện thoại iPhone 14 Pro Max 256GB chính hãng VNA
    KẾT QUẢ CUỐI CÙNG     : điện thoại iphone 14 pro max 256gb chính hãng vna
------------------------------------------------------------------------------------------
```

---

### Bài tập 2 — `exercises/ex_2.py`

Xây dựng bộ phân loại Naive Bayes hoàn chỉnh, huấn luyện với 50 mẫu rồi kiểm tra trên 3 văn bản mẫu.

**Chạy:**
```bash
python exercises\ex_2.py
```

**Kết quả mẫu:**
```
======================================================================
               BÀI TẬP 2: PHÂN LOẠI VĂN BẢN NAIVE BAYES
======================================================================

Đang huấn luyện mô hình với 50 mẫu dữ liệu...
Huấn luyện xong!

[1] VĂN BẢN    : 'Điện thoại giá rẻ chụp ảnh đẹp'
    Nhãn dự đoán  : ĐIỆN THOẠI
    Độ tin cậy    : 98.97%
    Chi tiết      :
        - Điện thoại     :  98.97%
        - Máy tính       :   0.42%
        - Đồ gia dụng    :   0.35%
        - Thời trang     :   0.13%
        - Mỹ phẩm        :   0.13%
    Nhận xét      : Văn bản này có xác suất cao nhất thuộc về nhóm 'Điện thoại' với 98.97%.
```

---

## 7. Ứng dụng Desktop

File: `desktop/app.py` — Giao diện đồ họa xây dựng bằng **CustomTkinter**.

**Chạy:**
```bash
python desktop\app.py
```

**Tính năng:**

| Tính năng | Mô tả |
|-----------|-------|
| Phân loại đơn lẻ | Nhập văn bản → hiển thị nhãn + % từng nhóm |
| Phân loại hàng loạt | Chọn file CSV → xử lý và hiển thị từng kết quả |
| Đổi giao diện | Chuyển đổi giữa Light / Dark / System |

---

## 8. Ứng dụng Website

File: `web/main.py` — API REST bằng **FastAPI**, giao diện HTML/CSS/JS hiện đại (dark mode, glassmorphism).

**Chạy:**
```bash
uvicorn web.main:app --host 127.0.0.1 --port 8000
```

Sau đó mở trình duyệt và truy cập: **http://127.0.0.1:8000**

### Các API endpoint

| Endpoint | Phương thức | Mô tả |
|----------|-------------|-------|
| `/` | GET | Trả về trang HTML chính |
| `/predict` | POST | Phân loại một văn bản (form field: `text`) |
| `/predict_batch` | POST | Phân loại hàng loạt (form file: `file`) |

**Ví dụ gọi API `/predict`:**
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -F "text=Điện thoại giá rẻ chụp ảnh đẹp"
```

**Kết quả trả về (JSON):**
```json
{
  "text": "Điện thoại giá rẻ chụp ảnh đẹp",
  "result": {
    "predicted_label": "Điện thoại",
    "probabilities": {
      "Điện thoại": 98.97,
      "Máy tính": 0.42,
      "Đồ gia dụng": 0.35,
      "Thời trang": 0.13,
      "Mỹ phẩm": 0.13
    },
    "comment": "Văn bản này có xác suất cao nhất thuộc về nhóm 'Điện thoại' với 98.97%."
  }
}
```

**Tính năng giao diện web:**
- Phân loại đơn lẻ với thanh xác suất động có animation
- Tải file CSV để phân loại hàng loạt, hiển thị kết quả dạng bảng
- Màu sắc badge phân biệt theo từng nhóm sản phẩm
- Giao diện tối (dark mode) với hiệu ứng glassmorphism

---

## 9. Hướng dẫn chạy

### Bước 1: Clone hoặc tải về dự án

```bash
# Nếu dùng git
git clone <url-repository>
cd description-classifier
```

### Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy theo mục đích

```bash
# Chạy bài tập 1 (tiền xử lý NLP)
python exercises\ex_1.py

# Chạy bài tập 2 (phân loại Naive Bayes)
python exercises\ex_2.py

# Chạy ứng dụng Desktop
python desktop\app.py

# Chạy ứng dụng Website (từ thư mục gốc dự án)
uvicorn web.main:app --host 127.0.0.1 --port 8000
```

> **Lưu ý:** Tất cả lệnh phải được chạy từ **thư mục gốc** (`description-classifier/`), không phải từ bên trong các thư mục con.

---

## 10. Kết quả minh họa

### Các nhãn phân loại và màu sắc tương ứng (trên Web)

| Nhãn | Màu |
|------|-----|
| Điện thoại | Xanh dương |
| Máy tính | Tím |
| Thời trang | Hồng |
| Mỹ phẩm | Vàng cam |
| Đồ gia dụng | Xanh lá |

### Độ chính xác mô hình

Mô hình Naive Bayes được huấn luyện với 50 mẫu cân bằng (10 mẫu/nhãn). Với các văn bản có từ khóa rõ ràng, độ tin cậy thường đạt trên **90%**. Với các văn bản mơ hồ hoặc chứa nhiều từ không có trong tập huấn luyện, độ tin cậy có thể thấp hơn và mô hình sẽ tự động đưa ra cảnh báo trong phần nhận xét.

---

## 11. Triển khai trên Render

### 11.1 Giới thiệu Render

**Render** là nền tảng cloud hosting miễn phí cho phép triển khai các ứng dụng web Python, Node.js, Docker, v.v. với tính năng:

- **Miễn phí**: Free tier đủ để chạy các ứng dụng nhỏ và trung bình
- **Tự động deploy**: Chỉ cần push code lên GitHub, Render sẽ tự động build và deploy
- **HTTPS tự động**: Cấp certificate SSL/TLS miễn phí
- **Dễ cấu hình**: Hỗ trợ Python, có thể chạy các lệnh tùy chỉnh

### 11.2 Yêu cầu trước deploy

Để deploy dự án này lên Render, bạn cần:

1. **Tài khoản Render** — Đăng ký miễn phí tại [render.com](https://render.com)
2. **Tài khoản GitHub** — Code phải được push lên repository GitHub (Render sẽ pull từ đây)
3. **Git cài đặt** — Để push code lên GitHub
4. **Code đã sẵn sàng** — Đảm bảo tất cả file cần thiết đã được commit

### 11.3 Các file cấu hình cần thiết

Dự án đã có sẵn các file cấu hình sau:

#### `Procfile` (cho Render hoặc Heroku)
```
web: uvicorn web.main:app --host 0.0.0.0 --port $PORT
```

**Giải thích:**
- `web:` — Đây là process type, cho biết đây là web service
- `uvicorn web.main:app` — Khởi động FastAPI server
- `--host 0.0.0.0` — Lắng nghe trên tất cả địa chỉ IP (bắt buộc trên cloud)
- `--port $PORT` — Dùng port từ biến môi trường `$PORT` do Render cấp

#### `render.yaml` (cấu hình Render tùy chọn)
```yaml
services:
  - type: web
    name: description-classifier
    runtime: python
    pythonVersion: 3.11
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn web.main:app --host 0.0.0.0 --port $PORT
```

**Lưu ý:** Nếu dùng file này, Render sẽ ưu tiên cấu hình từ `render.yaml` thay vì UI dashboard.

#### `requirements.txt`
Chứa danh sách các thư viện Python cần cài đặt:
```
fastapi
uvicorn
python-multipart
jinja2
customtkinter
```

### 11.4 Các bước deploy chi tiết

#### Bước 1: Chuẩn bị code trên GitHub

**1.1 Khởi tạo Git (nếu chưa có)**

```bash
cd description-classifier
git init
```

**1.2 Thêm repository GitHub remote**

```bash
git remote add origin https://github.com/YOUR_USERNAME/description-classifier.git
```

Thay `YOUR_USERNAME` bằng username GitHub của bạn.

**1.3 Commit tất cả file**

```bash
git add .
git commit -m "Initial commit: Product Description Classifier"
```

**1.4 Tạo branch chính và push**

```bash
git branch -M main
git push -u origin main
```

Sau lệnh này, tất cả file sẽ được push lên GitHub. Kiểm tra tại `https://github.com/YOUR_USERNAME/description-classifier` để đảm bảo code đã có.

#### Bước 2: Đăng nhập Render

1. Truy cập [render.com](https://render.com)
2. Click **"Sign up"** hoặc **"Sign in"**
3. Chọn đăng nhập bằng **GitHub** (được khuyến khích)
4. Cấp quyền để Render có thể truy cập repository của bạn

#### Bước 3: Tạo Web Service mới

1. Sau khi đăng nhập, truy cập **Dashboard**
2. Click nút **"New +"** ở góc trên phải
3. Chọn **"Web Service"**

#### Bước 4: Kết nối repository

1. Chọn repository `description-classifier` từ danh sách
2. Nếu không thấy, click **"Configure account"** để cho phép Render truy cập thêm repository
3. Click **"Connect"** để kết nối

#### Bước 5: Cấu hình Web Service

Điền thông tin sau:

| Trường | Giá trị |
|-------|--------|
| **Name** | `description-classifier` (hoặc tên tùy ý, sẽ tạo subdomain) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn web.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` (đủ cho phát triển) |

**Ví dụ cấu hình:**

```
Name:              description-classifier
Runtime:           Python 3
Build Command:     pip install -r requirements.txt
Start Command:     uvicorn web.main:app --host 0.0.0.0 --port $PORT
Instance Type:     Free
```

#### Bước 6: Cấu hình Environment Variables (nếu cần)

Để thêm biến môi trường (ví dụ API keys, config, v.v.):

1. Cuộn xuống phần **"Environment"**
2. Click **"Add Environment Variable"**
3. Nhập `key` và `value`

**Ví dụ** (tùy chọn, dự án này không yêu cầu):
- `KEY`: `LOG_LEVEL`, `VALUE`: `info`

Để trống nếu không cần.

#### Bước 7: Deploy

1. Cuộn xuống, click **"Create Web Service"**
2. Render sẽ bắt đầu build và deploy
3. Chờ 2-5 phút để quá trình hoàn tất

**Trạng thái build:**
- **In Progress** — Đang build
- **Live** — Deploy thành công!
- **Failed** — Có lỗi, xem logs

#### Bước 8: Truy cập ứng dụng

Sau khi thành công, bạn sẽ nhận được URL dạng:

```
https://description-classifier.onrender.com
```

- Truy cập trang web chính: `https://description-classifier.onrender.com`
- Xem API docs (Swagger UI): `https://description-classifier.onrender.com/docs`
- Xem ReDoc docs: `https://description-classifier.onrender.com/redoc`

### 11.5 Kiểm tra Logs (gỡ lỗi)

Nếu deploy không thành công hoặc ứng dụng báo lỗi:

1. Vào **Dashboard** → Chọn web service
2. Click vào tab **"Logs"**
3. Đọc thông báo lỗi để tìm nguyên nhân

Một số lỗi thường gặp:

| Lỗi | Nguyên nhân | Cách sửa |
|-----|-----------|---------|
| `ModuleNotFoundError` | Thiếu thư viện trong `requirements.txt` | Thêm thư viện vào `requirements.txt`, commit và push |
| `ERROR: failed to build one or more wheels` | Thư viện không tương thích | Xem phiên bản Python (3.9+), cập nhật `requirements.txt` |
| `Connection refused on port` | Port sai hoặc không dùng `$PORT` | Kiểm tra `Procfile` hoặc command, phải dùng `--port $PORT` |
| `FileNotFoundError: data.json` | File data chưa được commit | Commit tất cả file, push lại |

### 11.6 Cập nhật sau deploy

Khi cần cập nhật code:

**Cách 1: Tự động (được khuyến khích)**
```bash
# Sửa code locally
# Commit và push
git add .
git commit -m "Update: Fix bug or add feature"
git push origin main

# Render sẽ tự động phát hiện và deploy lại trong 1-2 phút
```

**Cách 2: Thủ công**
1. Vào Render Dashboard
2. Chọn web service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

### 11.7 Lưu ý quan trọng

#### 1. **Dữ liệu không được lưu giữa deploys**
- File system trên Render là **ephemeral** (tạm thời)
- Nếu có dữ liệu upload hoặc tạo, nó sẽ bị xóa khi container restart
- **Giải pháp:** Lưu dữ liệu vào database (MongoDB, PostgreSQL, v.v.)

#### 2. **Sleep sau 15 phút không sử dụng**
- Free tier sẽ tự động sleep nếu không có request trong 15 phút
- Khi có request mới, mất 30 giây để wake up (cold start)
- **Giải pháp:** Upgrade lên tier trả phí nếu cần uptime 24/7

#### 3. **Giới hạn tài nguyên**
- **CPU:** Chia sẻ (shared), không độc quyền
- **Memory:** 512 MB
- **Bandwidth:** ~50 GB/tháng
- Đủ cho phát triển và demo

#### 4. **HTTPS bắt buộc**
- Tất cả kết nối Render đều là HTTPS
- API client phải sử dụng `https://`, không phải `http://`

### 11.8 Nâng cấp (tùy chọn)

Nếu muốn cải thiện hiệu suất:

| Upgrade | Chi phí | Lợi ích |
|---------|--------|--------|
| **Paid Instance** | $7/tháng | CPU riêng, RAM đầy đủ, không sleep |
| **PostgreSQL Database** | $15/tháng | Lưu dữ liệu persistent |
| **Environment variables** | Miễn phí | Cấu hình an toàn (API keys, v.v.) |

### 11.9 Kết nối Custom Domain (tùy chọn)

Nếu muốn dùng domain riêng thay vì `*.onrender.com`:

1. Mua domain (từ Namecheap, GoDaddy, v.v.)
2. Vào **Web Service** → **Settings** → **Custom Domains**
3. Thêm domain và cập nhật DNS records
4. Chờ xác nhận (có thể mất vài phút đến vài giờ)

### 11.10 Ví dụ Deploy hoàn chỉnh

Tóm tắt quy trình:

```bash
# 1. Chuẩn bị code
cd description-classifier
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/description-classifier.git
git push -u origin main

# 2. Đăng nhập Render, tạo Web Service, điền thông tin:
#    - Name: description-classifier
#    - Build: pip install -r requirements.txt
#    - Start: uvicorn web.main:app --host 0.0.0.0 --port $PORT
#    - Instance: Free

# 3. Chờ deploy ~2-5 phút

# 4. Truy cập
#    https://description-classifier.onrender.com

# 5. Cập nhật trong tương lai
git add .
git commit -m "Update features"
git push origin main
# Render tự động deploy lại
```

### 11.11 Kiểm tra ứng dụng sau deploy

**Trang chủ (giao diện web):**
```
https://description-classifier.onrender.com
```

**API Endpoints:**

```bash
# 1. Phân loại một văn bản
curl -X POST "https://description-classifier.onrender.com/predict" \
     -F "text=Điện thoại giá rẻ chụp ảnh đẹp"

# 2. Xem API documentation
# https://description-classifier.onrender.com/docs (Swagger UI)
# https://description-classifier.onrender.com/redoc (ReDoc)

# 3. Phân loại hàng loạt (tải file)
curl -X POST "https://description-classifier.onrender.com/predict_batch" \
     -F "file=@data/data.csv"
```

**Kết quả mong đợi:**
```json
{
  "text": "Điện thoại giá rẻ chụp ảnh đẹp",
  "result": {
    "predicted_label": "Điện thoại",
    "probabilities": {
      "Điện thoại": 98.97,
      "Máy tính": 0.42,
      "Đồ gia dụng": 0.35,
      "Thời trang": 0.13,
      "Mỹ phẩm": 0.13
    },
    "comment": "Văn bản này có xác suất cao nhất thuộc về nhóm 'Điện thoại' với 98.97%."
  }
}
```

---

## Liên hệ và Hỗ trợ

Nếu gặp vấn đề hoặc có câu hỏi:

- **Email:** luongtd.tech@gmail.com
- **GitHub:** luongtd-tech/description-classifier
- **Tài liệu thêm:**
  - [Render Docs](https://render.com/docs)
  - [FastAPI Docs](https://fastapi.tiangolo.com/)
  - [Uvicorn Docs](https://www.uvicorn.org/)

## © Description Classifier - Developed by luongtd from Vinh University.