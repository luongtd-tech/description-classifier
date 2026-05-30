import sys
import os
import json

# Thêm thư mục gốc dự án vào sys.path để import được module 'core'
# __file__ = .../exercises/ex_1.py
# dirname 1 lần => .../exercises
# dirname 2 lần => .../description-classifier  (thư mục gốc)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from core.nlp_utils import lower_case, remove_punctuation, remove_whitespace, preprocess, count_words

def main():
    print("=" * 90)
    print(f"{'BÀI TẬP 1: TIỀN XỬ LÝ NGÔN NGỮ TỰ NHIÊN':^90}")
    print("=" * 90 + "\n")

    # Đọc dữ liệu từ data.json
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        texts = [item['text'] for item in dataset]
    except Exception as e:
        print(f"Lỗi khi đọc file dữ liệu: {e}")
        texts = []

    print(f"Tổng số văn bản cần xử lý: {len(texts)}\n")
    print("-" * 90)

    for i, text in enumerate(texts, 1):
        print(f"[{i}] VĂN BẢN GỐC      : '{text}'")
        print(f"    {'Số từ':<22}: {count_words(text)}")
        print(f"    {'Chuyển chữ thường':<22}: {lower_case(text)}")
        print(f"    {'Xóa dấu câu':<22}: {remove_punctuation(text)}")
        print(f"    {'Xóa khoảng trắng':<22}: {remove_whitespace(text)}")
        print(f"    {'KẾT QUẢ CUỐI CÙNG':<22}: {preprocess(text)}")
        print("-" * 90)

if __name__ == '__main__':
    main()
