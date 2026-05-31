import sys
import os
import json
import math

# Thêm thư mục gốc dự án vào sys.path để import được module 'core'
# __file__ = .../exercises/ex_2.py
# dirname 1 lần => .../exercises
# dirname 2 lần => .../description-classifier  (thư mục gốc)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from core.nlp_utils import preprocess
from core.classifier import NaiveBayesClassifier

# ============================================================
# Chạy thử khi chạy trực tiếp file này
# ============================================================
if __name__ == '__main__':
    # Đọc dữ liệu huấn luyện
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)

        print("=" * 70)
        print(f"{'BÀI TẬP 2: PHÂN LOẠI VĂN BẢN NAIVE BAYES':^70}")
        print("=" * 70)
        print(f"\nĐang huấn luyện mô hình với {len(dataset)} mẫu dữ liệu...")

        model = NaiveBayesClassifier()
        model.train(dataset)
        print("Huấn luyện xong!\n")

        # Các văn bản dùng để kiểm tra
        test_texts = [
            "Điện thoại giá rẻ chụp ảnh đẹp",
            "Laptop mỏng nhẹ cho sinh viên",
            "Áo sơ mi nam công sở"
        ]

        print("=" * 70)
        print(f"{'KẾT QUẢ KIỂM TRA MÔ HÌNH':^70}")
        print("=" * 70)

        for i, text in enumerate(test_texts, 1):
            res = model.predict(text)

            print(f"\n[{i}] VĂN BẢN    : '{text}'")
            print(f"    {'Nhãn dự đoán':<14}: {res['predicted_label'].upper()}")
            print(f"    {'Độ tin cậy':<14}: {res['probabilities'][res['predicted_label']]}%")
            print(f"    {'Chi tiết':<14}:")
            for label, prob in sorted(res['probabilities'].items(), key=lambda x: x[1], reverse=True):
                print(f"        - {label:<15}: {prob:>6.2f}%")
            print(f"    {'Nhận xét':<14}: {res['comment']}")
            print("-" * 70)

    except Exception as e:
        print(f"Lỗi khi chạy ex_2.py: {e}")
