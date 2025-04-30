from pathlib import Path
import json

this_path = Path(__file__).resolve().parent

def parseConfig() -> dict:
  """Parses config.json and returns its data"""
  with open(this_path / 'lib/config.json', 'r', encoding='utf-8') as file:
    return json.load(file)