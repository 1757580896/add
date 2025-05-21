#!/usr/bin/env python3
import requests
import sys
from pathlib import Path

# 配置
PROXY_PREFIX = "https://mg.345564.xyz/proxy.php?url="
SOURCES = [
    ("https://raw.githubusercontent.com/cxr9912/cxr2025/main/my.txt", "processed_url1.txt"),
    ("https://raw.githubusercontent.com/bharing19/List1/main/1", "processed_url2.txt")
]
TIMEOUT = 10

def process_line(line: str) -> str:
    """处理单行文本"""
    line = line.strip()
    if line.startswith(('http://', 'https://')):
        return f"{PROXY_PREFIX}{line}"
    return line

def process_source(url: str, output_path: str) -> bool:
    """处理单个URL源"""
    try:
        print(f"Processing {url}...", file=sys.stderr)
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in resp.text.splitlines():
                f.write(f"{process_line(line)}\n")
        
        print(f"Success: {url} -> {output_path}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"ERROR processing {url}: {type(e).__name__} - {str(e)}", file=sys.stderr)
        return False

def combine_files(output_files: list, combined_path: str):
    """合并结果文件"""
    with open(combined_path, 'w', encoding='utf-8') as out:
        for file in output_files:
            out.write(f"=== {Path(file).name} ===\n")
            with open(file, 'r', encoding='utf-8') as f:
                out.write(f.read() + "\n\n")

if __name__ == "__main__":
    # 处理所有源
    results = [process_source(url, path) for url, path in SOURCES]
    
    if all(results):
        combine_files(
            output_files=[path for _, path in SOURCES],
            combined_path="combined_results.txt"
        )
        print("All tasks completed successfully", file=sys.stderr)
    else:
        print("Some tasks failed", file=sys.stderr)
        sys.exit(1)
