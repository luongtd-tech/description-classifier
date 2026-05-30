import csv
import io

def parse_csv_file(file_content):
    """Đọc nội dung file CSV (bytes) và trả về danh sách văn bản"""
    try:
        text_data = file_content.decode('utf-8')
        reader    = csv.reader(io.StringIO(text_data))
        texts     = []

        for row in reader:
            if not row:
                continue
            cell = row[0].strip()
            if cell:
                texts.append(cell)

        # Bỏ dòng tiêu đề nếu có (vd: "text", "description", "mô tả")
        header_words = ['text', 'description', 'mô tả', 'mota']
        if texts and texts[0].lower() in header_words:
            texts = texts[1:]

        return texts

    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return []
