import tkinter as tk
from tkinter import filedialog, messagebox, PanedWindow
from tkhtmlview import HTMLLabel
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import markdown
import os

class HtmlToMdConverterApp:
    def __init__(self, root):
        self.root = root

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Web to Markdown Converter (No CSS)")
        self.root.geometry("1200x700")

        # --- Toolbar ---
        self.toolbar = tk.Frame(self.root, padx=5, pady=5)
        self.toolbar.pack(side="top", fill="x")

        self.url_label = tk.Label(self.toolbar, text="URL:")
        self.url_label.pack(side="left", padx=(0, 5))
        self.url_entry = tk.Entry(self.toolbar)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.url_entry.bind("<Return>", self.fetch_and_convert)

        self.convert_button = tk.Button(self.toolbar, text="Fetch & Convert", command=self.fetch_and_convert)
        self.convert_button.pack(side="left", padx=5)
        self.save_button = tk.Button(self.toolbar, text="Save as MD", command=self.save_file)
        self.save_button.pack(side="left", padx=5)

        # --- Paned Window ---
        self.paned_window = PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.paned_window.pack(fill="both", expand=True, padx=5, pady=5)

        self.editor = tk.Text(self.paned_window, wrap="word", undo=True, relief=tk.SUNKEN, borderwidth=1)
        self.editor.bind("<KeyRelease>", self.update_preview)
        self.paned_window.add(self.editor, width=600)

        self.preview = HTMLLabel(self.paned_window, html="", relief=tk.SUNKEN, borderwidth=1)
        self.paned_window.add(self.preview, width=600)

        # --- Status Bar ---
        self.status_label = tk.Label(self.root, text="Ready", anchor="w", padx=5)
        self.status_label.pack(side="bottom", fill="x")

    def _update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def _clean_markdown(self, text):
        return "\n".join(line.rstrip() for line in text.splitlines() if line.strip())

    def fetch_and_convert(self, event=None):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        try:
            self._update_status(f"Fetching from {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            self._update_status("Parsing HTML...")
            soup = BeautifulSoup(response.text, 'html.parser')

            self._update_status("Converting to Markdown...")
            md_text = md(str(soup), heading_style="ATX")
            md_text = self._clean_markdown(md_text)

            self.editor.delete("1.0", tk.END)
            self.editor.insert(tk.END, md_text)
            self.update_preview()
            self._update_status("Conversion successful.")
        except requests.RequestException as e:
            messagebox.showerror("Fetch Error", f"Failed to retrieve URL: {e}")
            self._update_status("Error fetching URL.")
        except Exception as e:
            messagebox.showerror("Conversion Error", f"An unexpected error occurred: {e}")
            self._update_status("Error during conversion.")

    def update_preview(self, event=None):
        md_text = self._clean_markdown(self.editor.get("1.0", tk.END).strip())
        html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'nl2br'])
        html_full = f"<html><body>{html_body}</body></html>"
        self.preview.set_html(html_full)

    def save_file(self):
        content = self.editor.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "There is no content to save.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self._update_status(f"File saved to {os.path.basename(file_path)}")
        except IOError as e:
            messagebox.showerror("Save Error", f"Failed to save file: {e}")
            self._update_status("Error saving file.")

# 実行エントリポイント
if __name__ == "__main__":
    root = tk.Tk()
    app = HtmlToMdConverterApp(root)
    root.mainloop()
