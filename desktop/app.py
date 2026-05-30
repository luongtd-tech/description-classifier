import customtkinter as ctk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import json
import os
import sys

# Thêm thư mục gốc dự án vào sys.path để import được module 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.classifier import NaiveBayesClassifier
from core.data_handler import parse_csv_file

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Phân loại sản phẩm ứng dụng AI")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Tải dữ liệu và huấn luyện mô hình khi khởi động
        self.classifier = NaiveBayesClassifier()
        self.load_model()

        # Chia bố cục: cột 0 = sidebar, cột 1 = nội dung chính
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Sidebar bên trái ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(self.sidebar, text="Description Classifier",
                     font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_single = ctk.CTkButton(self.sidebar, text="Nhập văn bản", command=self.show_single,
                                         text_color=("black", "white"))
        self.btn_single.grid(row=1, column=0, padx=20, pady=10)

        self.btn_batch = ctk.CTkButton(self.sidebar, text="Tải file lên", command=self.show_batch,
                                        text_color=("black", "white"))
        self.btn_batch.grid(row=2, column=0, padx=20, pady=10)

        ctk.CTkLabel(self.sidebar, text="Giao diện:", anchor="w").grid(row=5, column=0, padx=20, pady=(10, 0))
        self.mode_menu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                           command=lambda m: ctk.set_appearance_mode(m))
        self.mode_menu.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.mode_menu.set("System")

        # --- Khung nội dung bên phải ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Panel: Phân loại đơn lẻ
        self.single_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.single_frame, text="Phân loại đơn lẻ",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(10, 20), anchor="w")

        self.textbox = ctk.CTkTextbox(self.single_frame, height=150)
        self.textbox.pack(fill="x", pady=(0, 20))
        self.textbox.insert("0.0", "Nhập mô tả sản phẩm vào đây (vd: Điện thoại iPhone 17 Pro Max 2TB)...")

        ctk.CTkButton(self.single_frame, text="Phân Loại Ngay",
                      font=ctk.CTkFont(weight="bold"), command=self.predict_single).pack(anchor="w", pady=(0, 20))

        self.result_frame = ctk.CTkFrame(self.single_frame)
        self.result_frame.pack(fill="both", expand=True)
        self.lbl_result = ctk.CTkLabel(self.result_frame, text="", justify="left", font=ctk.CTkFont(size=14))
        self.lbl_result.pack(padx=20, pady=20, anchor="nw")

        # Panel: Phân loại hàng loạt qua file
        self.batch_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.batch_frame, text="Phân loại hàng loạt qua File",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(10, 20), anchor="w")

        self.lbl_file = ctk.CTkLabel(self.batch_frame, text="Chưa chọn file (Hỗ trợ định dạng .csv)")
        self.lbl_file.pack(anchor="w", pady=(0, 10))

        ctk.CTkButton(self.batch_frame, text="Chọn File CSV", command=self.choose_file).pack(anchor="w", pady=(0, 20))

        self.batch_result = ctk.CTkTextbox(self.batch_frame, wrap="word")
        self.batch_result.pack(fill="both", expand=True)

        self.footer_label = ctk.CTkLabel(self.main_frame,
                                        text="© Description Classifier - Developed by luongtd from Vinh University.",
                                        font=ctk.CTkFont(size=10),
                                        anchor="e")
        self.footer_label.pack(side="bottom", anchor="e", padx=(0, 20), pady=(0, 10))

        self.selected_file = None
        self.show_single()

    def load_model(self):
        """Đọc data.json và huấn luyện mô hình Naive Bayes"""
        base     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base, 'data', 'data.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                self.classifier.train(json.load(f))
        except Exception as e:
            mb.showerror("Lỗi dữ liệu", f"Không thể tải dữ liệu: {e}")

    def show_single(self):
        """Hiển thị panel nhập văn bản đơn lẻ"""
        self.batch_frame.pack_forget()
        self.single_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.btn_single.configure(fg_color=["#3B8ED0", "#1F6AA5"], text_color="white")
        self.btn_batch.configure(fg_color="transparent", text_color=("black", "white"))

    def show_batch(self):
        """Hiển thị panel tải file hàng loạt"""
        self.single_frame.pack_forget()
        self.batch_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.btn_batch.configure(fg_color=["#3B8ED0", "#1F6AA5"], text_color="white")
        self.btn_single.configure(fg_color="transparent", text_color=("black", "white"))

    def predict_single(self):
        """Lấy văn bản từ textbox, gọi mô hình và hiển thị kết quả"""
        text = self.textbox.get("0.0", "end").strip()
        if not text or text.startswith("Nhập mô tả"):
            mb.showwarning("Cảnh báo", "Vui lòng nhập văn bản cần phân loại!")
            return

        res  = self.classifier.predict(text)
        out  = f"Kết quả: {res['predicted_label']}\n"
        out += "-" * 40 + "\n"
        for label, prob in sorted(res['probabilities'].items(), key=lambda x: x[1], reverse=True):
            out += f"• {label}: {prob}%\n"
        out += f"\nNhận xét: {res['comment']}"
        self.lbl_result.configure(text=out)

    def choose_file(self):
        """Mở hộp thoại chọn file CSV và xử lý ngay"""
        path = fd.askopenfilename(
            title="Chọn file dữ liệu",
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            self.selected_file = path
            self.lbl_file.configure(text=f"Đã chọn: {os.path.basename(path)}")
            self.process_batch()

    def process_batch(self):
        """Đọc file CSV đã chọn và phân loại từng dòng"""
        if not self.selected_file:
            return

        self.batch_result.delete("0.0", "end")
        self.batch_result.insert("end", "Đang xử lý file...\n")
        self.update()

        try:
            with open(self.selected_file, 'rb') as f:
                texts = parse_csv_file(f.read())

            if not texts:
                self.batch_result.insert("end", "Không tìm thấy dữ liệu hợp lệ trong file.\n")
                return

            self.batch_result.delete("0.0", "end")
            self.batch_result.insert("end", f"Tìm thấy {len(texts)} mô tả. Bắt đầu phân loại...\n")
            self.batch_result.insert("end", "-" * 60 + "\n")

            for i, text in enumerate(texts, 1):
                res        = self.classifier.predict(text)
                label      = res['predicted_label']
                prob       = res['probabilities'][label]
                short_text = text[:50] + "..." if len(text) > 50 else text
                self.batch_result.insert("end", f"[{i}] {short_text}  =>  {label.upper()} ({prob}%)\n")

            self.batch_result.insert("end", "-" * 60 + "\n")
            self.batch_result.insert("end", "Hoàn tất xử lý file.\n")

        except Exception as e:
            mb.showerror("Lỗi", f"Có lỗi xảy ra: {e}")


if __name__ == "__main__":
    App().mainloop()
