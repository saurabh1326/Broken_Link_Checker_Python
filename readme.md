Python Required - 3.*

Install Dependencies -

pip install -r requirements,txt

usage: broken_link.py [-h] -site SITE -depth DEPTH [-out OUT]

Broken Link Checker

optional arguments:
  -h, --help    show this help message and exit
  -site SITE    Specify the start URL
  -depth DEPTH  Specify the maximium crawler depth
  -out OUT      Specify the output format json or text

Example -  python broken_link.py  -depth 2 -out text -site 'http://www.techradar.com'
It will give you list of broken urls internally in the same base url and externally separately

#Not Added any Unit test and Ci pipline



