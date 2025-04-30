import json
from pathlib import Path
import pdfplumber
import re
import math


class Tile():
  def __init__(self, date, heading, description, amount):
    self.date: str = date
    self.heading: str = heading
    self.description: list[str] = description
    self.amount: list[str] = amount


def parseConfig() -> dict:
  """Parses config.json and returns its data"""
  with open(Path(__file__).resolve().parent / '../src/lib/config.json', 'r', encoding='utf-8') as file:
    return json.load(file)


def parsePDF(file_path: str) -> dict[int, list[list[str]]]:
  """Parses the given PDF's tables"""

  with pdfplumber.open(file_path) as pdf:
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


def parseData(data: list[list[str]]):
  regex = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$" # detects date DD.MM.YYYY
  tiles = []

  for table in data.values():
    if len(table) < 1: continue
    currentTile = Tile("", "", [], []) # default empty tile for the beginning of reading

    for idx, row in enumerate(table):
      if idx == 0: continue # the first row contains the headings, therefore we skip it

      if re.match(regex, row[0]):
        tiles.append(currentTile)
        currentTile = Tile(row[0], row[1], [], [row[2], row[3]])
        continue

      currentTile.description.append(row[1])

    tiles.append(currentTile)
  return tiles


def getDescriptionOnly(description: list[str]):
  """Returns the bank statement description without the unnecessary parts"""
  return " ".join(description).rsplit("BIC / IBAN")[0]


def assembleTable(config, tiles):
  lines = []

  for tile in tiles:
    if tile.date == "": continue

    amount = "".join(tile.amount)
    if amount[0] == '-':
      sh = 'H'
      amount = amount[1:]
    else:
      sh = 'S'
    date = tile.date
    description = getDescriptionOnly(tile.description)

    lines.append(config["seperator"].join([amount, sh, config["wanted_error"] + config["contra_account"], date, config["account"], description]))
  
  return lines


def overwriteConfig(config, userConfig):
  if userConfig["account"] != "":
    config["account"] = userConfig["account"]
  
  if userConfig["contra_account"] != "":
    config["contra_account"] = userConfig["contra_account"]

  if userConfig["wanted_error"] == "off":
    config["wanted_error"] = ""

  return config


def main(userConfig):
  data = parsePDF(userConfig["pdf_location"])
  config = parseConfig()
  config = overwriteConfig(config, userConfig)

  tiles = parseData(data)

  lines = assembleTable(config, tiles)

  with open(userConfig["csv_location"], 'w', encoding='utf-8') as file:
    headings = config["seperator"].join(config["format"])
    file.write(headings)
    file.write('\n')
    for line in lines:
      file.write(line.strip())
      file.write('\n')
