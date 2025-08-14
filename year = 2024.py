def year_uru():
  year = 1999
  if year % 400 == 0:
    print(f"{year}年はうるう年です")

  elif year % 100 == 0:
    print(f"{year}年は平年です")

  elif year % 4 == 0:
    print(f"{year}年はうるう年です")

  else:
    print(f"{year}年は平年です")

year_uru()

