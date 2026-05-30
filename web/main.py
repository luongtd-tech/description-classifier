from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
import sys

# Thêm thư mục gốc dự án vào sys.path để import được module 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')
from core.classifier import NaiveBayesClassifier
from core.data_handler import parse_csv_file

app = FastAPI(title="Product Description Classifier")

# Phục vụ các file tĩnh (CSS, JS) tại đường dẫn /static
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Cấu hình Jinja2 để render template HTML
templates = Jinja2Templates(directory="web/templates")

# Khởi tạo và huấn luyện mô hình ngay khi server khởi động
classifier = NaiveBayesClassifier()

data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'data.json')
if os.path.exists(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    classifier.train(dataset)
    print(f"Đã huấn luyện mô hình với {len(dataset)} mẫu dữ liệu.")
else:
    print("Không tìm thấy file dữ liệu!")

# Route chính: trả về trang HTML
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

# API dự đoán một văn bản đơn lẻ (gửi qua form POST)
@app.post("/predict")
async def predict(text: str = Form(...)):
    if not text.strip():
        return JSONResponse(status_code=400, content={"error": "Văn bản không được để trống"})
    result = classifier.predict(text)
    return {"text": text, "result": result}

# API dự đoán hàng loạt qua file CSV tải lên
@app.post("/predict_batch")
async def predict_batch(file: UploadFile = File(...)):
    content = await file.read()
    texts   = parse_csv_file(content)

    if not texts:
        return JSONResponse(status_code=400, content={"error": "File không hợp lệ hoặc không có dữ liệu"})

    results = []
    for t in texts:
        res = classifier.predict(t)
        results.append({
            "text":            t,
            "predicted_label": res['predicted_label'],
            "probabilities":   res['probabilities']
        })

    return {"filename": file.filename, "total_processed": len(texts), "results": results}
