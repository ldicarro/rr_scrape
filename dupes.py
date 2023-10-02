"""
compares current id with dictionary of ids.
returns message string if found or empty string

Parameters
----------
ids: dictionary
id: string
currentKey: string

Returns
-------
string
"""
def findDupes(ids, id, currentKey):
  dupes = []
  s = ""
  for key in ids:
    if key == currentKey:
      continue
    for checkId in ids[key]:
      if id == checkId:
        dupes.append(key)

  if len(dupes) > 0:
    s += "Also found in: "
    for i,st in enumerate(dupes):
      s += st.replace('_', ' ').title()
      if i + 1 < len(dupes):
        s += ", "
  
  return s


"""
compares current company name with list of companies.
returns message string if found or empty string

Parameters
----------
companies: list
companyName: string

Returns
-------
string
"""
def findCompanyDupes(companies, companyName):
  s = ''

  for company in companies:
    if companyName == company['company']:
      s += 'You have applied to this company before. (' + company['count'] + ')'
      break
  
  return s