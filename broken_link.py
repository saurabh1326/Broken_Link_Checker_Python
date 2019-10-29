import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import argparse


parser = argparse.ArgumentParser(description='Broken Link Checker')
parser.add_argument('-site' ,dest = 'site' , required=True , help = "Specify the start URL")
parser.add_argument('-depth' , dest = 'depth' ,type =int ,required=True, help = "Specify the maximium crawler depth")
parser.add_argument('-out' ,dest = 'out' , default='json' , help = "Specify the output format json or text")
args = parser.parse_args()
# Get base links

Max_depth = args.depth
format = args.out

#site = 'http://www.techradar.com'
site = args.site
base = urlparse(site).netloc

to_visit = [site]
depth = [1]
outlinks = []
visited = {}
external_visited = {}

while to_visit :
    l = to_visit.pop()
    d = depth.pop()
    if d >=Max_depth:
        break
    print(l)
    url = urljoin(site, l)

    try:
        r = requests.get(url)
        visited[l] = r.status_code

    except:
        visited[l] = None

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html5lib')
        links = [l['href'] for l in soup.find_all('a', href=True)]
        for link in links:
            parsed_link = urlparse(link)
            loc = parsed_link.netloc
            path = parsed_link.path
            joined_url = urljoin(site, link)

            if loc == '':
                if joined_url not in to_visit and joined_url not in visited.keys():
                    to_visit.append(joined_url)
                    depth.append(d+1)

            elif loc == base:
                if link not in to_visit and link not in visited.keys():
                    to_visit.append(link)
                    depth.append(d+1)


            else:
                if link not in outlinks and link not in visited.keys():
                    outlinks.append(link)

# check the status of external links
while outlinks:
    l = outlinks.pop()

    try:
        r = requests.get(l)
        external_visited[l] = r.status_code

    except:
        external_visited[l] = None
error_internal = {k:v for  k,v in visited.items() if v<200 or v>=300}
error_external = {k:v for  k,v in external_visited.items() if v<200 or v>=300}

def create_output(format , error_internal , error_external):

    if format.upper() == "JSON":
            out_dict = {'Internal_links' : error_internal , 'External_links' : error_external}
            print (out_dict)

    if format.upper() == "TEXT":
        print ("Internal Error Links - ")
        if len(error_internal.keys())  == 0:
            print ("Nothing Found")
        for key in error_internal:
            print (key  , error_internal[key])
        print ("External Error Links - ")
        if len(error_external) == 0:
            print ("Nothing Found")
        for key in error_external:
            print (key, error_external[key])

create_output(format, error_internal, error_external)
