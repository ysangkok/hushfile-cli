import csv
import os.path
with open(os.path.join(os.path.dirname(__file__), "config")) as f:
    pairs = dict(csv.reader(f, delimiter='=', quotechar='"'))
    endpoint = pairs["ENDPOINT"]
