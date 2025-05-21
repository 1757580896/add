#!/usr/bin/env python3
import sys
import requests

def process_url(input_url, output_file):
    try:
        response = requests.get(input_url)
        response.raise_for_status()
        
        with open(output_file, 'w') as f:
            for line in response.text.splitlines():
                if line.startswith('http'):
                    processed = f"https://mg.345564.xyz/proxy.php?url={line}"
                    f.write(processed + '\n')
                else:
                    f.write(line + '\n')
        
        print(f"Successfully processed {input_url} -> {output_file}")
        return True
    except Exception as e:
        print(f"Error processing {input_url}: {str(e)}")
        return False

def main():
    urls_to_process = [
        ("https://raw.githubusercontent.com/cxr9912/cxr2025/main/my.txt", "processed_url1.txt"),
        ("https://raw.githubusercontent.com/bharing19/List1/main/1", "processed_url2.txt")
    ]
    
    for url, output in urls_to_process:
        if not process_url(url, output):
            sys.exit(1)
    
    # 合并结果
    with open("combined_results.txt", 'w') as outfile:
        outfile.write("=== Processed URL 1 ===\n")
        with open("processed_url1.txt") as infile:
            outfile.write(infile.read())
        
        outfile.write("\n\n=== Processed URL 2 ===\n")
        with open("processed_url2.txt") as infile:
            outfile.write(infile.read())

if __name__ == "__main__":
    main()
