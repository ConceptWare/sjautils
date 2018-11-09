import time

perDay = 24 * 60 * 60
perYear = perDay * 365.25

def _scaledEpoch(scale, e = None):
  e = e or time.time()
  return e / scale

def dayNum(e = None):
  return _scaledEpoch(perDay, e)

def yearNum(e = None):
  return _scaledEpoch(perYear, e)
