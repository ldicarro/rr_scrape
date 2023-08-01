#!/usr/bin/env python

import shutil

print("start")

with open('html/index.html') as f:
    first_line = f.readline().strip('<!-- ').strip(' -->\n')
    print(first_line)
    shutil.copy('html/index.html',f"html/{first_line}.html")