#!/usr/bin/env python3
import requests
import sys
import re
from pathlib import Path

# 配置
PROXY_PREFIX = "https://mg.345564.xyz/proxy.php?url="
SOURCES = [
    ("https://raw.githubusercontent.com/cxr9912/cxr2025/main/my.txt", "processed_url1.txt"),
    ("https://raw.githubusercontent.com/bharing19/List1/main/1", "processed_url2.txt")
]
TIMEOUT = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def process_url(url: str) -> str:
    """为URL添加代理前缀"""
    url = url.strip()
    if url.startswith(('http://', 'https://')):
        return f"{PROXY_PREFIX}{url}"
    return url

def process_source(url: str, output_path: str) -> bool:
    """处理单个URL源"""
    try:
        print(f"⌛ 正在处理: {url}", file=sys.stderr)
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in resp.text.splitlines():
                f.write(f"{process_url(line)}\n")
        
        print(f"✅ 成功生成: {output_path}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"❌ 处理失败 [{url}]: {type(e).__name__} - {str(e)}", file=sys.stderr)
        return False

def combine_files(output_files: list):
    """合并结果文件"""
    with open("combined_results.txt", 'w', encoding='utf-8') as out:
        for file in output_files:
            out.write(f"=== {Path(file).name} ===\n")
            with open(file, encoding='utf-8') as f:
                out.write(f.read() + "\n\n")

if __name__ == "__main__":
    results = [process_source(url, path) for url, path in SOURCES]
    
    if all(results):
        combine_files([path for _, path in SOURCES])
        print("✅ 所有任务完成", file=sys.stderr)
        sys.exit(0)
    else:
        print("❌ 部分任务失败", file=sys.stderr)
        sys.exit(1)
