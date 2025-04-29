import json
from pathlib import Path
import pdfplumber
import re


this_path = Path(__file__).resolve().parent


class Tile():
  def __init__(self, date, heading, description, amount):
    self.date: str = date
    self.heading: str = heading
    self.description: list[str] = description
    self.amount: list[str] = amount


def parseConfig() -> dict:
  """Parses config.json and returns its data"""
  with open(this_path / 'config.json', 'r', encoding='utf-8') as file:
    return json.load(file)


def parsePDF(file_name: str) -> dict[int, list[list[str]]]:
  """Parses the given PDF's tables"""

  with pdfplumber.open(this_path / "../conversion" / file_name) as pdf:
    data = {}

    for pageIdx, page in enumerate(pdf.pages):
      table = page.extract_table(table_settings={
        "horizontal_strategy": "text",
        "text_tolerance": 2
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


def assembleTable(config, data: list[list[str]]):
  regex = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$"
  tiles = []

  for table in data.values():
    if len(table) < 1: continue
    currentTile = Tile("", "", [], [])

    for idx, row in enumerate(table):
      if idx == 0: continue # the first row contains the headings, therefore we skip it

      if re.match(regex, row[0]):
        tiles.append(currentTile)
        currentTile = Tile(row[0], row[1], [], [row[2], row[3]])
        continue

      currentTile.description.append(row[1])

    tiles.append(currentTile)
  return tiles


def main():
  data = parsePDF('example.pdf')
  config = parseConfig()
  
  # with open(this_path / 'example.json', 'w', encoding='utf-8') as file:
  #   json.dump(data, file, ensure_ascii=False, indent=2)

  tiles = assembleTable(config, data)
  print(tiles[4].amount)


if __name__ == "__main__":
    main()