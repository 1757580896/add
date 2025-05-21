#!/usr/bin/env python3
"""
URL 处理器：为指定URL列表中的HTTP链接添加代理前缀
"""
import requests
import sys
from pathlib import Path

# 配置常量
PROXY_PREFIX = "https://mg.345564.xyz/proxy.php?url="
SOURCE_URLS = [
    ("https://raw.githubusercontent.com/cxr9912/cxr2025/main/my.txt", "processed_url1.txt"),
    ("https://raw.githubusercontent.com/bharing19/List1/main/1", "processed_url2.txt")
]
TIMEOUT = 10  # 请求超时时间(秒)

def process_url(url: str) -> str:
    """为单个URL添加前缀"""
    url = url.strip()
    if url.startswith(('http://', 'https://')):
        return f"{PROXY_PREFIX}{url}"
    return url

def fetch_and_process(source_url: str, output_file: str) -> bool:
    """获取并处理单个源URL"""
    try:
        response = requests.get(source_url, timeout=TIMEOUT)
        response.raise_for_status()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in response.text.splitlines():
                f.write(f"{process_url(line)}\n")
        return True
    except Exception as e:
        print(f"Error processing {source_url}: {type(e).__name__} - {str(e)}", file=sys.stderr)
        return False

def combine_results(output_files: list, combined_file: str) -> None:
    """合并多个结果文件"""
    with open(combined_file, 'w', encoding='utf-8') as out:
        for file in output_files:
            out.write(f"=== {Path(file).name} ===\n")
            with open(file, encoding='utf-8') as f:
                out.write(f.read() + "\n\n")

def main():
    """主处理流程"""
    success = all(fetch_and_process(url, output) for url, output in SOURCE_URLS)
    
    if success:
        combine_results(
            output_files=[output for _, output in SOURCE_URLS],
            combined_file="combined_results.txt"
        )
        print("Processing completed successfully")
        sys.exit(0)
    else:
        print("Processing failed for some URLs", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
