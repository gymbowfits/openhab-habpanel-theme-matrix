
import json
import requests
import time
import urlparse
import sys
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET

t1 = time.time()

symbols = { 'line-visuals',
			'connection-arw-l', 
			'controal-4',
			'double-arrow',
			'down-arrow-2',
			'reload',
			'volume-close',
			'volume-increase',
			'volume',
			'right-arrow-2',
			'right-play',
			'left-arrow-2',
			'stop_1_',
			'top-arrow-2',
			'battery',
			'box',
			'charging-2',
			'charging-3',
			'charging-1',
			'drive-3',
			'drive',
			'flat-tv',
			'floppy',
			'plug',
			'processor',
			'sim-card',
			'window',
			'globe',
			'navigate',
			'clock',
			'direction-n',
			'drop',
			'drops',
			'half-moon',
			'half-light',
			'shade',
			'stars',
			'sun',
			'thermometer-3',
			'wind',
			'umberla',
			'sun-nwave',
			'tree-3' }

symbol_count = 0
mypath = '/etc/openhab2/html/matrix-theme/original-svgs'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

ET.register_namespace("","http://www.w3.org/2000/svg")
top = ET.Element('svg', attrib = { 'version':'1.1', 'xmlns:xlink':'http://www.w3.org/1999/xlink', 'x':"0px", 'y':"0px", 'viewBox':"0 0 48 48", 'enable-background':"new 0 0 48 48", 'xml:space':"preserve"})
comment = ET.Comment('Generated by SVG-Combiner')
top.append(comment)

for file in onlyfiles:
	if(file[:1] != '.'):
		print "Processing file: " + file

		r = requests.get('http://127.0.0.1:8080/static/matrix-theme/original-svgs/' + file)
		print len(r.status_code)
		if(len(r.text)>0):
			xml = ET.fromstring(r.text)
			for child in xml:
				if(len(child.getchildren())>0 and 'id' in child.attrib):
					if(child.attrib['id'] in symbols):
						for node in child.findall('.//*[@fill]'):
							if ('stroke' in node.attrib): node.attrib.pop('stroke')
							if ('stroke-width' in node.attrib): node.attrib.pop('stroke-width')
						#print child.attrib['id'], ET.tostring(child,encoding='utf8', method='xml')
						top.append(child)
						symbol_count = symbol_count + 1
						print " --> added " + child.attrib['id']
		else:
			print "Error processing file: HTTP Response " + str(r.status_code)

f = open('/etc/openhab2/html/matrix-theme/squidink.svg', 'w')
f.write(ET.tostring(top,encoding='utf8', method='xml'))
f.close()


t2 = time.time()
print "Done in " + str(t2-t1) + " seconds " + str(symbol_count) + " symbols created"    



