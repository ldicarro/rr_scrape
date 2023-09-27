import csv
import json

"""
read json from data file

Parameters
----------
none

Returns
-------
object: json
"""
def getJsonData():
  with open("./data.json") as f:
    document = f.read()
    return json.loads(document)

"""
read companies from csv data file

Parameters
----------
none

Returns
-------
list of dictionaries
"""  
def getCompaniesData():
  with open('./companies.csv') as data:
    dict_reader = csv.DictReader(data)
    list_of_dict = list(dict_reader)
    return list_of_dict