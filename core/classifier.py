import math
from core.nlp_utils import preprocess

class NaiveBayesClassifier:
    def __init__(self):
        # Số lần xuất hiện của từng từ trong mỗi nhóm: { nhãn: { từ: số_lần } }
        self.class_word_counts = {}
        # Số văn bản thuộc mỗi nhóm: { nhãn: số_lượng }
        self.class_doc_counts = {}
        # Tổng số từ trong mỗi nhóm: { nhãn: tổng_từ }
        self.class_total_words = {}
        # Tập hợp toàn bộ từ vựng xuất hiện trong dữ liệu
        self.vocab = set()
        # Tổng số văn bản đã huấn luyện
        self.total_docs = 0

    def train(self, dataset):
        """Huấn luyện mô hình từ danh sách dữ liệu [{ text, label }]"""
        for item in dataset:
            text  = item['text']
            label = item['label']

            # Khởi tạo bộ đếm cho nhãn mới nếu chưa có
            if label not in self.class_word_counts:
                self.class_word_counts[label] = {}
                self.class_doc_counts[label]  = 0
                self.class_total_words[label] = 0

            self.class_doc_counts[label] += 1
            self.total_docs += 1

            # Đếm tần suất từng từ trong văn bản
            for word in preprocess(text).split():
                self.vocab.add(word)
                self.class_total_words[label] += 1
                self.class_word_counts[label][word] = self.class_word_counts[label].get(word, 0) + 1

    def predict(self, text):
        """Dự đoán nhãn cho một văn bản, trả về nhãn + xác suất + nhận xét"""
        words      = preprocess(text).split()
        vocab_size = len(self.vocab)
        scores     = {}

        for label in self.class_doc_counts:
            # Xác suất tiên nghiệm: P(nhãn) = số văn bản nhãn / tổng văn bản
            log_prob = math.log(self.class_doc_counts[label] / self.total_docs)

            # Cộng dồn log xác suất có điều kiện của từng từ (Laplace smoothing)
            for word in words:
                count   = self.class_word_counts[label].get(word, 0)
                prob    = (count + 1) / (self.class_total_words[label] + vocab_size)
                log_prob += math.log(prob)

            scores[label] = log_prob

        # Nhãn có điểm log-prob cao nhất là kết quả dự đoán
        best_label = max(scores, key=scores.get)

        # Chuẩn hóa điểm số thành xác suất % (dùng softmax ổn định)
        max_score  = max(scores.values())
        exp_scores = {l: math.exp(s - max_score) for l, s in scores.items()}
        total      = sum(exp_scores.values())
        probs      = {l: round(v / total * 100, 2) for l, v in exp_scores.items()}

        # Tạo nhận xét tự động
        confidence = probs[best_label]
        comment = f"Văn bản này có xác suất cao nhất thuộc về nhóm '{best_label}' với {confidence}%."
        if confidence < 50:
            comment += " Tuy nhiên, độ tin cậy không cao, có thể văn bản chứa nhiều từ mới hoặc gây nhầm lẫn."

        return {
            "predicted_label": best_label,
            "scores":          scores,   # Điểm log-probability gốc
            "probabilities":   probs,    # Xác suất đã chuẩn hóa (%)
            "comment":         comment
        }
