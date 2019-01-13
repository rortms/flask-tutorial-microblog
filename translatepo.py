####################################
# Automate translation of po file
# Note: imperfect, strings containing code like, %(username)s, get translated.
# Easily corrected with a text editor replace, 90% of the work gets done.

import os
import requests
import json


fpath = "/home/krolik/ProjProg/Flask/microblog_tut/microblog/app/translations/es/LC_MESSAGES/messages.po"
with open("yandex_key") as keyf:
    YANDEX_TRANSLATOR_KEY = keyf.readlines()[0]

with open(fpath, 'r') as pof:
    lines = pof.readlines()

###########################
# Key is line number containing text to translate
# Note: Key + 1 is the line number for translated text
text2translate_map = dict()

# Populate map
for i, l in enumerate(lines):
    if l.find("msgid") != -1:
        line_number, text_index = i, l.find('"')
        text2translate_map[line_number] = l[text_index:].strip()
##

########################
# Translate with Yandex

## Translationg GET request
def translate(text, source_language, dest_language):
    
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json'
                     '/translate?key={}&text={}&lang={}-{}'.format(
                         
                         YANDEX_TRANSLATOR_KEY,
                         text,
                         source_language,
                         dest_language))
    return json.loads(r.content)['text'][0]

# tests = [ 'This is a sentence',
#           'Hello, how are you?',
#           'Yellow beatles battle and bellow',
#           ]

# for t in tests:
#     print(t)
#     print(translate(t, 'en', 'es'))
#     print()


## Get translations and write to file
with open('./test_translated.po', 'w') as result:
    
    for i in range(len(lines)):
        if text2translate_map.get(i):
            text2translate = text2translate_map[i]
            
            #
            print("Translating: ", text2translate)
            translation = translate(text2translate, 'en', 'es')
            print("Translation is: ", translation)
            #
            
            # Constructing po line
            lines[i+1] = 'msgstr ' + translation + '\n'

        result.write(lines[i])
        
