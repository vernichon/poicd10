#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import polib
import urllib
from lxml import html 
from lxml.html import fromstring, tostring
import sys
url_base  = "http://apps.who.int/classifications/icd10/browse/2008/fr/GetConcept?ConceptId="
# load an existing po file
po = polib.pofile('icd10_fr_FR.po')


for entry in po:
    # do something with your entry like:
    code = entry.msgctxt.replace('model:gnuhealth.pathology,name:','').replace('model:gnuhealth.pathology.category,name:','')

    if  "model:gnuhealth.pathology,name:" in entry.msgctxt:
        if len(code) == 4:
            code = code[:3]+"."+code[-1]
        url = url_base +code.strip()
 
        page =  html.fromstring(urllib.urlopen(url).read())
        
        
        #print tostring(page)
     
        try : 
            print code,entry.msgid,
            try:
                entry.msgstr =  page.get_element_by_id(code).getnext().text_content().encode('iso-8859-15')
            except:
                entry.msgstr =  page.get_element_by_id(code).getnext().text_content().encode('iso-8859-1')
            print entry.msgstr
        except:
            print "%s not found" % code
# adding an entry
#entry = polib.POEntry(msgid='Welcome', msgstr='Bienvenue')
#entry.occurrences = [('welcome.py', '12'), ('anotherfile.py', '34')]
#po.append(entry)

# saving the modified po file
po.save()
