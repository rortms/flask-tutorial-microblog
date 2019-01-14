####################################
# Automate translation of po file
# Note: imperfect, strings containing code like, %(username)s, get translated.
# Easily corrected with a text editor replace, 90% of the work gets done.

import os
import requests
import json
import re

fpath = "./microblog/app/translations/es/LC_MESSAGES/messages.po"

with open("yandex_key") as keyf:
    YANDEX_TRANSLATOR_KEY = keyf.readlines()[0]

with open(fpath, 'r') as pof:
    lines = pof.readlines()

########################
# Translate with Yandex

# Extract relevant text
def extractText(line):
    text_index = line.find('"')
    return line[text_index:].strip()

## Translationg GET request
def translate(text, source_language, dest_language):
    
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json'
                     '/translate?key={}&text={}&lang={}-{}'.format(
                         
                         YANDEX_TRANSLATOR_KEY,
                         text,
                         source_language,
                         dest_language))
    return json.loads(r.content)['text'][0]

##
def pyfmtTranslate(l, from_lang, to_lang):
    """
    deal with lines with python formating, e.g.;
    
    msgid "User %(username)s not found." 

    """
    # l = extractText(l)
    # print(l)
    text2ommitp = re.compile('%\([a-zA-Z]+\)s')
    iterator = text2ommitp.finditer(l)
    start, low, high = 0, 0, 0
    result = ''

    for match in iterator:
        # print (match.span())
        low, high = match.span()

        text = l[start:low]
        result += translate(text, from_lang, to_lang) + l[low:high]        
        # result += text.upper() + l[low:high]

        start = high
        
    result += translate(l[high:], from_lang, to_lang)
    # result += l[high:].upper()    
    
    return result

    
# pyfmtTranslate('msgid "%(username)s said: %(when)s"')

###########################
# Populate map
# Key is line number containing text to translate
# Note: Key + 1 is the line number for translated text
text2translate_map = dict()

for i, l in enumerate(lines):
    # If its a msgid line and translation, msgstr is empty
    if l.find("msgid") != -1 and lines[i+1] == 'msgstr ""\n':
        text2translate_map[i] = extractText(l)
        
    # if l[:len('msgid')] == 'msgid' 
        # line_number, text_index = i, l.find('"')


        
##############################
## Get translations and write to file
with open('./test_translated.po', 'w') as result:
    
    for i in range(len(lines)):
        
        if text2translate_map.get(i):
            print(lines[i])

            #
            text2translate = text2translate_map[i]

            if lines[i].find('%') != -1: # If there is special python formatting
                translation = pyfmtTranslate(text2translate, 'en', 'es')
            else:
                translation = translate(text2translate, 'en', 'es')


            # Constructing po line
            lines[i+1] = lines[i+1].replace('""',  translation)
            
            print(lines[i+1])                
            print("----------")

        result.write(lines[i])

        
# tests = [ 'This is a sentence',
#           'Hello, how are you?',
#           'Yellow beatles battle and bellow',
#           ]

# for t in tests:
#     print(t)
#     print(translate(t, 'en', 'es'))
#     print()
# tr = translate("yellow", 'en', 'es')
# for i in range(len(lines)):
#     if text2translate_map.get(i):
#         text2translate = text2translate_map[i]
#         print(lines[i+1].replace('""', '"' + tr + '"' ))
