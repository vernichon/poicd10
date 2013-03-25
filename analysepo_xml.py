#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import polib
import urllib
from lxml import html 
from lxml.html import fromstring, tostring
from xml.dom.minidom import parse
import sys
url_base  = "http://apps.who.int/classifications/icd10/browse/2008/fr/GetConcept?ConceptId="
# load an existing po file
po = polib.pofile('icd10_fr_FR.po')

doc = parse('data/fr.xml')
data = {}
#print dir(doc)

for ligne in doc.getElementsByTagName('fr'):
    if ligne.nodeType == ligne.ELEMENT_NODE:
        code =  ligne.getElementsByTagName('code')[0].childNodes[0].nodeValue
        text_fr = ligne.getElementsByTagName('FR_OMS')[0].childNodes[0].nodeValue
        data[code] = text_fr 
        
for entry in po:
    
    if not entry.msgstr:
        code = entry.msgctxt.replace('model:gnuhealth.pathology,name:','').replace('model:gnuhealth.pathology.category,name:','')
        if "model:gnuhealth.pathology.category,name" in entry.msgctxt:
            
            code =  entry.msgid.split(' ')
            code = code[0].replace('(','').replace(')','')
            if data.has_key(code):
                entry.msgstr =  data[code]
                print "ok"
#            url = url_base +code.strip()
#            
#            page =  html.fromstring(urllib.urlopen(url).read())
#            try : 
#                print code,entry.msgid,
#                try:
#                    entry.msgstr =  page.get_element_by_id(code).text_content().encode('iso-8859-15').replace('\t','').replace('\r','').replace('\n','')
#                except:
#                    entry.msgstr =  page.get_element_by_id(code).text_content().encode('iso-8859-1').replace('\t','').replace('\r','').replace('\n','')
#                print entry.msgstr
#            except:
#                print "%s not found" % code
        elif  "model:gnuhealth.pathology,name:"  in entry.msgctxt:
            if len(code) == 4:
                code = code[:3]+"."+code[-1]
            if data.has_key(code):
                entry.msgstr =  data[code]
                print "ok"
            else:
                print code
                 
            
                           
#            url = url_base +code.strip()
#            page =  html.fromstring(urllib.urlopen(url).read())
#            try : 
#                print code,entry.msgid,
#                try:
#                    entry.msgstr =  page.get_element_by_id(code).getnext().text_content().encode('iso-8859-15')
#                except:
#                    entry.msgstr =  page.get_element_by_id(code).getnext().text_content().encode('iso-8859-1')
#                print entry.msgstr
#            except:
#                print "%s not found" % code
#        else:
#            print entry.msgctxt,code,entry.msgid
#            entry.msgctxt
## adding an entry
##entry = polib.POEntry(msgid='Welcome', msgstr='Bienvenue')
##entry.occurrences = [('welcome.py', '12'), ('anotherfile.py', '34')]
##po.append(entry)
#
## saving the modified po file
po.save()
