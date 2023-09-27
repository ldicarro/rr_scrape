#!/usr/bin/env python

from datetime import datetime
import json
import shutil
import subprocess
import shutil

import dupes
import files

from TimeUtil import TimeUtil
from TextUtil import TextUtil


def getJobIDs(data):
  ids = {}

  # loop through top level
  for key,item in data.items():
    # create list for each item at top level
    ids[key] = []

    # loop through each job in the current item
    for job in item:
      #append the id to the list
      ids[key].append(job['id'])

  return ids


"""
create html string while filtering 
and processing the json passed in.

Parameters
----------
data: object (json)

Returns
-------
string: html
"""
def processDocument(data):
  global ids, companies

  html = ''
  tabs = '<div class=\"tabs\">'

  for key,title in data.items():
    tabs += ('<h2 class=\" {} \">{}</h2>\n'.format(key, key.replace('_',' ').title()))
    html += ('<div class=\"posts__content posts__content--{}\">'.format(key))
    count = 0
    for post in title:
      timediff = TimeUtil().getHourDiff(post['created_at'])
      if timediff < 24:

        try:
          minSalary = ("$%" % post['salaryRange']['min'])
        except:
          minSalary = 'No salary listed'

        try:
          maxSalary = (" - $%" % post['salaryRange']['max'])
        except:
          maxSalary = ''

        if maxSalary != '' and int(post['salaryRange']['max']) < 130000:
          continue
        
        count += 1

        jobDupes = dupes.findDupes(ids, post['id'], key)
        companyDupes = dupes.findCompanyDupes(companies, post['company']['name'])


        html += f"""
        <div class="post" data-visible="false">
          <div class="post__headline">
            <div class="post__headline--link">
              <a href="{post['url']}" target="_blank">
                <h3>{post['roleTitle']}</h3>
              </a>
              <span class="close">X</span>
            </div>
            <h4>{post['company']['name']}</h4>
          </div>
          <div class="post__info">
            <span>{timediff} hours</span>
            <span>{minSalary}{maxSalary}</span>
          </div>
          <div class="post__dupes">
            <div class="dupes">{jobDupes}</div>
            <div class="dupes">{companyDupes}</div>
          </div>
          <div class="post__description">
            <p>{TextUtil().formatRawText(post['roleDescription'])}</p>
            <p>{TextUtil().formatRawText(post['roleRequirements'])}</p>
          </div>
          <div class="post__buttonbar">
            <button class="getSSText">Spreadsheet</button>
            <button class="getGPTText">GPT</button>
          </div>
          <div class="post__buttonbar--secondary">
            <button class="getGPTRes">Resume</button>
            <button class="getGPTLtr">Letter</button>
            <button class="getGPTInt">Intent</button>
          </div>
          <table>
            <tr>
              <td>{post['company']['name']}</td>
              <td>{post['roleTitle']}</td>
              <td>{minSalary}{maxSalary}</td>
              <td>{post['url']}</td>
            </tr>
          </table>
        </div>
        """
    
    if count == 0:
      html += "<div class=\"post\" data-visible=\"false\"><h3>No posts available.</h3></div>"
    html += "</div>"
  tabs += "</div>"

  return tabs + html

"""
create html document and write to file.

Parameters
----------
data: string (html)

Returns
-------
nothing
"""
def createHTMLDocument(html):
  with open('html/index.html') as f:
    first_line = f.readline().strip('<!-- ').strip(' -->\n')
    shutil.copy('html/index.html',"html/{}index_.html".format(first_line))

  with open('./index_template.html') as f:
    template = f.read()
    
    currDate = datetime.now().strftime("%y%m%d_%H%M")    
    newTemplate = template.replace("{{content}}",html).replace("{{filename}}",currDate)

    out = open("./html/index.html","w")
    out.write(newTemplate)
    out.close

  


if __name__ == "__main__":
  global ids, companies

  data = files.getJsonData()
  ids = getJobIDs(data)
  companies = files.getCompaniesData()

  htmlString = processDocument(data)
  createHTMLDocument(htmlString)
  
  
  # push html to server
  with open('./sync.sh') as f:
    subprocess.call(f.read().split(" "))

  # clearing the json file for next run
  shutil.copyfile('data.template.json','data.json')