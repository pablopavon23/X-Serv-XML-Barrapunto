#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.archivo = open("contents.html", "w")
        mensaje_html = "<!DOCTYPE html>\n" + "<html>\n" + "\t<head><META http-equiv=Content-Type content=text/html; charset=UTF-8></head>\n" + "\t<body>\n" + "\t\t<ol>\n"
        self.archivo.write(mensaje_html)

        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.line = ""

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
                self.line = "Title: " + self.theContent + "."
                # To avoid Unicode trouble
                print(self.line)
                self.archivo.write(self.line)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = self.theContent
                links = "\t\t\t<li>Link: <a href='" + self.link + "'>" + self.line + "</a></li>\n"
                print(links)
                self.archivo.write(links)
                self.inContent = False
                self.theContent = ""
                self.line = ""
        elif name == 'rdf:RDF':
                mensaje_fin = "\t\t</ol>\n" + "\t</body>\n" + "</html>"
                self.archivo.write(mensaje_fin)

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog
if len(sys.argv)<2:
    print("Usage: python xml-parser-barrapunto.py <document>")
    print()
    print(" <document>: file name of the document to parse")
    sys.exit(1)

# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)

print("Parse complete")
