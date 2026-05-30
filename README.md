# Hệ thống Phân loại Mô tả Sản phẩm

> **Môn học:** Xử lý Ngôn ngữ Tự nhiên  
> **Sinh viên:** luongtd — Trường Đại học Vinh  
> **Mô tả:** Dự án xây dựng hệ thống tự động phân loại mô tả sản phẩm thương mại điện tử sử dụng thuật toán Naive Bayes, được triển khai dưới hai hình thức: ứng dụng Desktop và giao diện Website.

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
| Điện thoại | 🔵 Xanh dương |
| Máy tính | 🟣 Tím |
| Thời trang | 🩷 Hồng |
| Mỹ phẩm | 🟡 Vàng cam |
| Đồ gia dụng | 🟢 Xanh lá |

### Độ chính xác mô hình

Mô hình Naive Bayes được huấn luyện với 50 mẫu cân bằng (10 mẫu/nhãn). Với các văn bản có từ khóa rõ ràng, độ tin cậy thường đạt trên **90%**. Với các văn bản mơ hồ hoặc chứa nhiều từ không có trong tập huấn luyện, độ tin cậy có thể thấp hơn và mô hình sẽ tự động đưa ra cảnh báo trong phần nhận xét.
