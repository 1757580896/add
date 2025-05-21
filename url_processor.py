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

def extract_links(text: str) -> list:
    """从文本/HTML中提取所有有效URL"""
    return list(set(re.findall(
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .-]*/?[?&#=\w.%+-]*', 
        text
    )))

def process_source(url: str, output_path: str) -> bool:
    """处理单个URL源"""
    try:
        print(f"⌛ 正在处理: {url}", file=sys.stderr)
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        
        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 提取并处理链接
        links = extract_links(resp.text)
        processed = [f"{PROXY_PREFIX}{link}" for link in links if link.startswith(('http://', 'https://'))]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(processed))
        
        print(f"✅ 成功处理: 从 {url} 提取到 {len(processed)} 个链接", file=sys.stderr)
        return True
        
    except Exception as e:
        print(f"❌ 处理失败 [{url}]: {type(e).__name__} - {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    results = [process_source(url, path) for url, path in SOURCES]
    sys.exit(0 if all(results) else 1)
