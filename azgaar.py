def getHeight(settings, h, abs):
  unit = float(settings["heightUnit"])
  return getRawHeight(settings, h, abs) + " " + unit


def getRawHeight(settings, h, abs):
  unit = settings["heightUnit"]
  unitRatio = 3.281 # default calculations are in feet
  if unit == "m":
      unitRatio = 1 # if meter
  elif unit == "f":
      unitRatio = 0.5468 # if fathom

  height = -990
  if h >= 20:
      height = pow(h - 18, float(settings["heightExponentInput"]))
  elif h < 20 and h > 0:
      height = (h - 20) / h * 50

  if abs:
      height = abs(height)
  return round(height * unitRatio)
  