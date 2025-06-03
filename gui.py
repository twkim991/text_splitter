# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from splitter import split_and_save
import os
import threading

class TextSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("텍스트 분할기")
        self.root.geometry("450x300")
        self.root.resizable(False, False)  # 창 크기 고정
        
        # 폰트 설정
        label_font = ("맑은 고딕", 10)
        button_font = ("맑은 고딕", 10, "bold")

        # 파일 경로
        self.file_path = None

        # 파일 선택 버튼
        self.file_label = tk.Label(root, text="파일을 선택하세요:", font=label_font)
        self.file_label.pack(pady=(20, 0))

        self.select_button = tk.Button(root, text="파일 선택", font=button_font, command=self.select_file, width=20)
        self.select_button.pack(pady=5)

        self.selected_file_label = tk.Label(root, text="선택된 파일 없음", fg="gray", font=("맑은 고딕", 9))
        self.selected_file_label.pack(pady=(0, 10))

        # 글자 수 입력
        self.char_label = tk.Label(root, text="몇 글자 단위로 자를까요?", font=label_font)
        self.char_label.pack()

        self.char_entry = tk.Entry(root, font=("맑은 고딕", 10), justify="center", width=10)
        self.char_entry.insert(0, "1000")
        self.char_entry.pack(pady=5)

        # 시작 버튼
        self.start_button = tk.Button(root, text="분할 시작", font=button_font, command=self.start_split, width=20)
        self.start_button.pack(pady=15)

        # 상태 표시
        self.status_label = tk.Label(root, text="", fg="blue", font=("맑은 고딕", 9))
        self.status_label.pack(pady=(10, 0))
        

    def select_file(self):
        filetypes = [("Text files", "*.txt"),
                     ("Word files", "*.docx"),
                     ("HWP files", "*.hwp"),
                     ("All files", "*.*")]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            self.file_path = path
            ext = os.path.splitext(path)[1].lower()
            
            # .hwp 파일이면 안내 메시지 추가
            if ext == '.hwp':
                label_text = f"{path} (HWP 파일은 한글 프로그램 설치 필요)"
            else:
                label_text = path
                
            self.selected_file_label.config(text=path, fg="black")

    def start_split(self):
        if not self.file_path:
            messagebox.showwarning("경고", "파일을 먼저 선택하세요.")
            return

        try:
            num_chars = int(self.char_entry.get())
            if num_chars <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("오류", "올바른 숫자를 입력해주세요.")
            return

        # 🔧 진행 중 메시지 먼저 표시
        self.status_label.config(text="🔧 분할 중입니다...")
        self.root.update()  # 즉시 반영
        
        # 작업 스레드 시작
        threading.Thread(target=self.run_split_thread, args=(num_chars,)).start()
    
    def run_split_thread(self, num_chars):
        try:
            output_zip = split_and_save(self.file_path, num_chars, "./output")
            self.status_label.config(text=f"✅ 완료: {os.path.basename(output_zip)}")
            os.startfile(output_zip)
        except Exception as e:
            self.status_label.config(text="❌ 오류 발생")
            messagebox.showerror("오류 발생", str(e))
