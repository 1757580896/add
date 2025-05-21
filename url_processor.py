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

def process_line(line: str) -> str:
    """处理单行文本"""
    line = line.strip()
    # 匹配包含逗号的格式（如："频道名称,http://..."）
    if "," in line:
        parts = line.split(",", 1)
        if parts[1].startswith(('http://', 'https://')):
            return f"{parts[0]},{PROXY_PREFIX}{parts[1]}"
    # 匹配纯URL格式
    elif line.startswith(('http://', 'https://')):
        return f"{PROXY_PREFIX}{line}"
    return line

def process_source(url: str, output_path: str) -> bool:
    """处理单个URL源"""
    try:
        print(f"⌛ 正在处理: {url}", file=sys.stderr)
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in resp.text.splitlines():
                processed = process_line(line)
                if processed:  # 跳过空行
                    f.write(f"{processed}\n")
        
        print(f"✅ 成功生成: {output_path}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"❌ 处理失败 [{url}]: {type(e).__name__} - {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    results = [process_source(url, path) for url, path in SOURCES]
    sys.exit(0 if all(results) else 1)
