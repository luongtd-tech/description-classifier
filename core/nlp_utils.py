import string
import re

# Chuyển toàn bộ ký tự về chữ thường
def lower_case(text: str) -> str:
    return text.lower()

# Xóa các ký tự dấu câu ra khỏi văn bản
def remove_punctuation(text: str) -> str:
    table = str.maketrans('', '', string.punctuation)
    return text.translate(table)

# Xóa khoảng trắng thừa (đầu, cuối, giữa các từ)
def remove_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

# Đếm số từ trong văn bản (sau khi đã làm sạch)
def count_words(text: str) -> int:
    cleaned = remove_whitespace(remove_punctuation(text))
    return len(cleaned.split()) if cleaned else 0

# Tiền xử lý đầy đủ: thường hóa -> xóa dấu câu -> xóa khoảng trắng
def preprocess(text: str) -> str:
    return remove_whitespace(remove_punctuation(lower_case(text)))
