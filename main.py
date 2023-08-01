#!/usr/bin/env python

from datetime import datetime
import json
import shutil
import subprocess
import sys

from TimeUtil import TimeUtil
from TextUtil import TextUtil


sectionTitles = {
  "engineering_manager": "Engineering Manager",
  "product_manager": "Product Manager",
  "software_engineer": "Software Engineer",
  "technical_product_manager": "Technical Product Manager",
}

def init():
  with open("./data.json") as f:
      document = f.read()
      data = json.loads(document)
      processDocument(data)

def processDocument(data):
  html = ''
  tabs = '<div class=\"tabs\">'

  for key,title in data.items():
    tabs += ('<h2 class=\" {} \">{}</h2>\n'.format(key, sectionTitles[key]))
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
  createHTML(tabs + html)
  
  with open('./sync.sh') as f:
    subprocess.call(f.read().split(" "))

def createHTML(html):
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
  init()