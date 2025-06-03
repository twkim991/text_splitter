# splitter.py
import os
import zipfile
from file_parser import parse_file

def split_text(text: str, chunk_size: int):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def split_and_save(file_path: str, chunk_size: int, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)

    text = parse_file(file_path)
    chunks = split_text(text, chunk_size)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_files = []

    for idx, chunk in enumerate(chunks, start=1):
        output_path = os.path.join(output_dir, f"{base_name}_{idx}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(chunk)
        output_files.append(output_path)

    # 압축하기
    zip_path = os.path.join(output_dir, f"{base_name}_splitted.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in output_files:
            arcname = os.path.basename(file)
            zipf.write(file, arcname=arcname)

    return zip_path