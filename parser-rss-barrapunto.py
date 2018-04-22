#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib.request
import sys


class myContentHandler(ContentHandler):

    title = ""
    output = ""

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                print("<a href=" + self.theContent +
                      ">" + self.title + "</a><br>")
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Process argv
if len(sys.argv) < 2:
    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
else:
    print("Parsing:", sys.argv[1])
    xmlFile = open(sys.argv[1], "r")

# get XML encoding
line = str(xmlFile.readline())
if "encoding=" in line:
    xml_encoding = line.split(' ')[2].split('\"')[1]
    print("Encoding:", xml_encoding)
else:
    xml_encoding = 'utf-8'

# Redir stdout
stdout = sys.stdout
sys.stdout = open('links.html', "w", encoding=xml_encoding)

# Add HTML title
print('<h1>X-Serv-XML-Barrapunto</h1>')

# Parse
theParser.parse(xmlFile)

# Restore stdout
sys.stdout = stdout

print('Parse done')
