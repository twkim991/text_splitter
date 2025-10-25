# filpip uninstall python-docx -ye_parser.py
from docx import Document
import os

def parse_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

def parse_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return parse_txt(file_path)
    elif ext == '.docx':
        return parse_docx(file_path)
    elif ext == '.hwp':
        return parse_hwp(file_path)
    else:
        raise ValueError("지원하지 않는 파일 형식입니다.")

def parse_hwp(file_path: str) -> str:
    try:
        import win32com.client

        hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
        hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")  # 보안 모듈 등록

        hwp.Open(file_path)
        hwp.InitScan()
        text = hwp.GetTextFile("TEXT", "UTF-8")
        hwp.Quit()

        return text
    except Exception as e:
        raise RuntimeError(f"HWP 읽기 실패: {e}")