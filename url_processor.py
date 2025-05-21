#!/usr/bin/env python3
import requests
import sys
from pathlib import Path
import re

# 配置
PROXY_PREFIX = "https://mg.345564.xyz/proxy.php?url="
SOURCES = [
    ("https://raw.githubusercontent.com/cxr9912/cxr2025/main/my.txt", "processed_url1.txt"),
    ("https://raw.githubusercontent.com/bharing19/List1/main/1", "processed_url2.txt")
]
TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def extract_links(text: str) -> list:
    """从文本中提取所有HTTP链接"""
    return re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)

def process_source(url: str, output_path: str) -> bool:
    """处理单个URL源"""
    try:
        print(f"Fetching {url}...", file=sys.stderr)
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        
        # 提取所有链接并添加前缀
        links = extract_links(resp.text)
        processed_links = [f"{PROXY_PREFIX}{link}" for link in links if link.startswith(('http://', 'https://'))]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(processed_links))
        
        print(f"Extracted {len(processed_links)} links from {url}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"ERROR processing {url}: {type(e).__name__} - {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = all(process_source(url, path) for url, path in SOURCES)
    sys.exit(0 if success else 1)
