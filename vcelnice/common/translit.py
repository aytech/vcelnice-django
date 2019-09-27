# coding=utf-8
import re
from transliterate.base import TranslitLanguagePack, registry
from transliterate.discover import autodiscover
from transliterate import translit

autodiscover()


class CzechLanguagePack(TranslitLanguagePack):
    language_code = 'cs'
    language_name = 'Czech'
    pre_processor_mapping = {
        u'ch': u'ch'
    }
    mapping = (
        u'aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvwxyýzž',
        u'aabccddeeefghiijklmnnoopqrrssttuuuvwxyyzz'
    )

registry.register(CzechLanguagePack)


class Translit:
    def __init__(self):
        pass

    @staticmethod
    def translit(string):
        # Try CZ
        string = translit(string, 'cs')

        # Normalize for RU chars
        string = translit(string, 'ru', reversed=True)

        # Remove spaces and punctuation
        string = re.sub(r'[\s+\'\"]', '_', string)

        # Remove underscore surplus
        string = re.sub(r'_+', '_', string)

        return string.strip('_')
