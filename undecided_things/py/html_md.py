import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os

def clean_markdown(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def web_to_md(url):
    print(f"Fetching {url} ...")
    response = requests.get(url.strip())
    response.encoding = response.apparent_encoding
    print("Parsing HTML...")
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Converting to Markdown...")
    markdown_content = md(str(soup), heading_style="ATX")
    markdown_content = clean_markdown(markdown_content)
    return markdown_content

if __name__ == "__main__":
    print("=== Multi Web to Markdown Converter (Save Confirm Mode) ===")
    urls = [u.strip().strip('"') for u in input("Enter URLs separated by commas: ").split(",") if u.strip()]
    folder = input("Enter the folder to save files (e.g., C:/Users/YourName/Documents): ").strip().strip('"')
    if not os.path.exists(folder):
        os.makedirs(folder)

    for url in urls:
        choice = input(f"Do you want to set a custom file name for {url}? (y/n): ").strip().lower()
        if choice == "y":
            filename = input("Enter the file name (without extension): ").strip()
            filename = filename.replace(" ", "_") + ".md"
        else:
            filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".md"

        output_path = os.path.join(folder, filename)
        markdown_content = web_to_md(url)

        print("\n---------- MARKDOWN PREVIEW ----------")
        preview = "\n".join(markdown_content.splitlines()[:15])
        print(preview)
        print("... (truncated)\n")

        confirm = input(f"Save this file as {output_path}? (y/n): ").strip().lower()
        if confirm == "y":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print("File saved.")
        else:
            print("Skipped saving.")

    print("All conversions completed.")
