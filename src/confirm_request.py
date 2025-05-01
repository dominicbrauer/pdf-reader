def confirmRequest(userConfig):
  if userConfig["pdf_location"][-4:].lower() != ".pdf" or userConfig["pdf_location"] == "":
    return False
  
  if userConfig["csv_location"][-4:].lower() != ".csv" or userConfig["csv_location"] == "":
    return False
  
  return True