import json
import requests

from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    # Yandex
    if 'YANDEX_TRANSLATOR_KEY' not in current_app.config or \
       not current_app.config['YANDEX_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {'Ocp-Apim-Subcription-Key': current_app.config['YANDEX_TRANSLATOR_KEY']}
    
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json'
                     '/translate?key={}&text={}&lang={}-{}'.format(
                         current_app.config['YANDEX_TRANSLATOR_KEY'],
                         text,
                         source_language,
                         dest_language)
    )

    # # Azure
    # if 'MS_TRANSLATOR_KEY' not in current_app.config or \
    #    not current_app.config['MS_TRANSLATOR_KEY']:
    #     return _('Error: the translation service is not configured.')
    # auth = {'Ocp-Apim-Subcription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    # r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
    #                  '/Translate?text={}&from={}&to={}'.format(
    #                      text, source_language, dest_language),
    #                  headers=auth)
    
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content)['text'][0]

# translate("Hey man, how's everything?", 'en', 'es')
