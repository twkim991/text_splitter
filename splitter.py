# splitter.py
import os
import zipfile
from file_parser import parse_file

import re

def split_text(text: str, chunk_size: int):
    result = []
    pos = 0
    length = len(text)

    # 사용할 문장 경계 문자들
    split_chars = ['.', '?', '!', ']']

    while pos < length:
        end = min(pos + chunk_size, length)
        segment = text[pos:end]

        # segment 안에서 마지막으로 등장한 문장경계문자의 위치를 찾음
        split_points = [segment.rfind(c) for c in split_chars]
        last_split_pos = max(split_points)

        # 기준 문자 못 찾으면 그냥 chunk_size로 자름
        if last_split_pos == -1 or pos + last_split_pos + 1 >= length:
            split_point = end
        else:
            split_point = pos + last_split_pos + 1  # 경계 문자 포함하여 자름

        result.append(text[pos:split_point].strip())
        pos = split_point

    return result


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