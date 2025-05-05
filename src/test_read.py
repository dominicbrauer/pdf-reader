import pdfplumber

def parsePDF():
  """Parses the given PDF's tables"""

  with pdfplumber.open("C:\\Users\\Dominic\\Desktop\\Scan_20250505_162506.pdf") as pdf:
    
    data = []

    for pageIdx, page in enumerate(pdf.pages):
      table = page.extract_table(table_settings={
        "horizontal_strategy": "text",
        "vertical_strategy": "explicit",
        "text_tolerance": 1,
        "explicit_vertical_lines": [40, 100, 410, 550]
      })
# [410, 550]
      data.append(table)
    
    return data[0]

    #   data[pageIdx] = []

    #   if table is not None:
    #     for row in table:
    #       data[pageIdx].append(row)
    # return data[0]

data = parsePDF();
for line in data:
  if line == ['', '', '']: continue
  print(f"{line}\n")