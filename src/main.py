import json
from pathlib import Path
import pdfplumber


this_path = Path(__file__).resolve().parent
file_path = this_path / 'config.json'


def parseConfig() -> dict:
  """Parses config.json and returns its data"""
  with open(file_path, 'r', encoding='utf-8') as file:
    return json.load(file)


def parsePDF(file_name: str) -> dict[int, list[list[str]]]:
  """Parses the given PDF's tables"""
  file_path = this_path / "../conversion" / file_name

  with pdfplumber.open(file_path) as pdf:
    data = {}

    for pageIdx, page in enumerate(pdf.pages):
      table = page.extract_table(table_settings={
        "horizontal_strategy": "text"
      })

      data[pageIdx] = []

      if table is not None:
        for row in table:
          if emptyRow(row): continue
          data[pageIdx].append(row)
    return data


def emptyRow(row: list[str]) -> bool:
  """Returns True if the row only contains empty strings"""
  return len(row) == row.count("")


def main():
  print("Running...")
  data = parsePDF('example.pdf')

  with open('example.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()