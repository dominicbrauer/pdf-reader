import pdfplumber
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
conversion_dir = BASE_DIR / "../conversion"

rows = []

with pdfplumber.open(f"{conversion_dir}/example.pdf") as pdf:
  first_page = pdf.pages[0]
  table = first_page.extract_table(table_settings={
    "horizontal_strategy": "text"
  })
  for row in table:
    rows.append(row)

with open(f"{conversion_dir}/test.txt", 'w', encoding='utf-8') as f:
  for row in rows:
    f.writelines(f"{row}\n")