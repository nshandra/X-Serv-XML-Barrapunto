#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib.request
import sys

class myContentHandler(ContentHandler):

    title = ""
    output = ""

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                print("<a href=" + self.theContent +">" + self.title + "</a><br>")
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

stdout = sys.stdout
sys.stdout = open('body.html',"w", encoding='iso-8859-1')
print('<h1>X-Serv-XML-Barrapunto</h1>')
    
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
if len(sys.argv)<2:
    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
else:
    print("Parsing", sys.argv[1], file=stdout)
    xmlFile = open(sys.argv[1], "r")

theParser.parse(xmlFile)
sys.stdout = stdout

print('Parse done')
