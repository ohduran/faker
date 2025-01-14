import re
import string

from collections import OrderedDict

from faker.utils.distribution import choices_distribution, choices_distribution_unique

_re_hash = re.compile(r'#')
_re_perc = re.compile(r'%')
_re_excl = re.compile(r'!')
_re_at = re.compile(r'@')
_re_qm = re.compile(r'\?')
_re_cir = re.compile(r'\^')


class BaseProvider:

    __provider__ = 'base'
    __lang__ = None

    # Locales supported by Linux Mint from `/usr/share/i18n/SUPPORTED`
    language_locale_codes = {
        'aa': ('DJ', 'ER', 'ET'), 'af': ('ZA',), 'ak': ('GH',), 'am': ('ET',),
        'an': ('ES',), 'apn': ('IN',),
        'ar': ('AE', 'BH', 'DJ', 'DZ', 'EG', 'EH', 'ER', 'IL', 'IN',
               'IQ', 'JO', 'KM', 'KW', 'LB', 'LY', 'MA', 'MR', 'OM',
               'PS', 'QA', 'SA', 'SD', 'SO', 'SS', 'SY', 'TD', 'TN',
               'YE'),
        'as': ('IN',), 'ast': ('ES',), 'ayc': ('PE',), 'az': ('AZ', 'IN'),
        'be': ('BY',), 'bem': ('ZM',), 'ber': ('DZ', 'MA'), 'bg': ('BG',),
        'bhb': ('IN',), 'bho': ('IN',), 'bn': ('BD', 'IN'), 'bo': ('CN', 'IN'),
        'br': ('FR',), 'brx': ('IN',), 'bs': ('BA',), 'byn': ('ER',),
        'ca': ('AD', 'ES', 'FR', 'IT'), 'ce': ('RU',), 'ckb': ('IQ',),
        'cmn': ('TW',), 'crh': ('UA',), 'cs': ('CZ',), 'csb': ('PL',),
        'cv': ('RU',), 'cy': ('GB',), 'da': ('DK',),
        'de': ('AT', 'BE', 'CH', 'DE', 'LI', 'LU'), 'doi': ('IN',),
        'dv': ('MV',), 'dz': ('BT',), 'el': ('GR', 'CY'),
        'en': ('AG', 'AU', 'BW', 'CA', 'DK', 'GB', 'HK', 'IE', 'IN', 'NG',
               'NZ', 'PH', 'SG', 'US', 'ZA', 'ZM', 'ZW'),
        'eo': ('US',),
        'es': ('AR', 'BO', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'ES', 'GT',
               'HN', 'MX', 'NI', 'PA', 'PE', 'PR', 'PY', 'SV', 'US', 'UY', 'VE',
               ), 'et': ('EE',), 'eu': ('ES', 'FR'), 'fa': ('IR',),
        'ff': ('SN',), 'fi': ('FI',), 'fil': ('PH',), 'fo': ('FO',),
        'fr': ('CA', 'CH', 'FR', 'LU'), 'fur': ('IT',), 'fy': ('NL', 'DE'),
        'ga': ('IE',), 'gd': ('GB',), 'gez': ('ER', 'ET'), 'gl': ('ES',),
        'gu': ('IN',), 'gv': ('GB',), 'ha': ('NG',), 'hak': ('TW',),
        'he': ('IL',), 'hi': ('IN',), 'hne': ('IN',), 'hr': ('HR',),
        'hsb': ('DE',), 'ht': ('HT',), 'hu': ('HU',), 'hy': ('AM',),
        'ia': ('FR',), 'id': ('ID',), 'ig': ('NG',), 'ik': ('CA',),
        'is': ('IS',), 'it': ('CH', 'IT'), 'iu': ('CA',), 'iw': ('IL',),
        'ja': ('JP',), 'ka': ('GE',), 'kk': ('KZ',), 'kl': ('GL',),
        'km': ('KH',), 'kn': ('IN',), 'ko': ('KR',), 'kok': ('IN',),
        'ks': ('IN',), 'ku': ('TR',), 'kw': ('GB',), 'ky': ('KG',),
        'lb': ('LU',), 'lg': ('UG',), 'li': ('BE', 'NL'), 'lij': ('IT',),
        'ln': ('CD',), 'lo': ('LA',), 'lt': ('LT',), 'lv': ('LV',),
        'lzh': ('TW',), 'mag': ('IN',), 'mai': ('IN',), 'mg': ('MG',),
        'mhr': ('RU',), 'mi': ('NZ',), 'mk': ('MK',), 'ml': ('IN',),
        'mn': ('MN',), 'mni': ('IN',), 'mr': ('IN',), 'ms': ('MY',),
        'mt': ('MT',), 'my': ('MM',), 'nan': ('TW',), 'nb': ('NO',),
        'nds': ('DE', 'NL'), 'ne': ('NP',), 'nhn': ('MX',),
        'niu': ('NU', 'NZ'), 'nl': ('AW', 'BE', 'NL'), 'nn': ('NO',),
        'nr': ('ZA',), 'nso': ('ZA',), 'oc': ('FR',), 'om': ('ET', 'KE'),
        'or': ('IN',), 'os': ('RU',), 'pa': ('IN', 'PK'),
        'pap': ('AN', 'AW', 'CW'), 'pl': ('PL',), 'ps': ('AF',),
        'pt': ('BR', 'PT'), 'quz': ('PE',), 'raj': ('IN',), 'ro': ('RO',),
        'ru': ('RU', 'UA'), 'rw': ('RW',), 'sa': ('IN',), 'sat': ('IN',),
        'sc': ('IT',), 'sd': ('IN', 'PK'), 'se': ('NO',), 'shs': ('CA',),
        'si': ('LK',), 'sid': ('ET',), 'sk': ('SK',), 'sl': ('SI',),
        'so': ('DJ', 'ET', 'KE', 'SO'), 'sq': ('AL', 'ML'), 'sr': ('ME', 'RS'),
        'ss': ('ZA',), 'st': ('ZA',), 'sv': ('FI', 'SE'), 'sw': ('KE', 'TZ'),
        'szl': ('PL',), 'ta': ('IN', 'LK'), 'tcy': ('IN',), 'te': ('IN',),
        'tg': ('TJ',), 'th': ('TH',), 'the': ('NP',), 'ti': ('ER', 'ET'),
        'tig': ('ER',), 'tk': ('TM',), 'tl': ('PH',), 'tn': ('ZA',),
        'tr': ('CY', 'TR'), 'ts': ('ZA',), 'tt': ('RU',), 'ug': ('CN',),
        'uk': ('UA',), 'unm': ('US',), 'ur': ('IN', 'PK'), 'uz': ('UZ',),
        've': ('ZA',), 'vi': ('VN',), 'wa': ('BE',), 'wae': ('CH',),
        'wal': ('ET',), 'wo': ('SN',), 'xh': ('ZA',), 'yi': ('US',),
        'yo': ('NG',), 'yue': ('HK',), 'zh': ('CN', 'HK', 'SG', 'TW'),
        'zu': ('ZA',),
    }

    def __init__(self, generator):
        self.generator = generator

    def locale(self):
        """Generate a random underscored i18n locale code (e.g. en_US).

        :sample:
        """
        language_code = self.language_code()
        return language_code + '_' + self.random_element(
            BaseProvider.language_locale_codes[language_code],
        )

    def language_code(self):
        """Generate a random i18n language code (e.g. en).

        :sample:
        """
        return self.random_element(BaseProvider.language_locale_codes.keys())

    def random_int(self, min=0, max=9999, step=1):
        """Generate a random integer between two integers ``min`` and ``max`` inclusive
        while observing the provided ``step`` value.

        This method is functionally equivalent to randomly sampling an integer
        from the sequence ``range(min, max + 1, step)``.

        :sample:
        :sample size=10: min=0, max=15
        :sample size=10: min=0, max=15, step=3
        """
        return self.generator.random.randrange(min, max + 1, step)

    def random_digit(self):
        """Generate a random digit (0 to 9).

        :sample:
        """
        return self.generator.random.randint(0, 9)

    def random_digit_not_null(self):
        """Generate a random non-zero digit (1 to 9).

        :sample:
        """
        return self.generator.random.randint(1, 9)

    def random_digit_or_empty(self):
        """Generate a random digit (0 to 9) or an empty string.

        This method will return an empty string 50% of the time,
        and each digit has a 1/20 chance of being generated.

        :sample size=10:
        """
        if self.generator.random.randint(0, 1):
            return self.generator.random.randint(0, 9)
        else:
            return ''

    def random_digit_not_null_or_empty(self):
        """Generate a random non-zero digit (1 to 9) or an empty string.

        This method will return an empty string 50% of the time,
        and each digit has a 1/18 chance of being generated.

        :sample size=10:
        """
        if self.generator.random.randint(0, 1):
            return self.generator.random.randint(1, 9)
        else:
            return ''

    def random_number(self, digits=None, fix_len=False):
        """Generate a random integer according to the following rules:

        - If ``digits`` is ``None`` (default), its value will be set to a random
          integer from 1 to 9.
        - If ``fix_len`` is ``False`` (default), all integers that do not exceed
          the number of ``digits`` can be generated.
        - If ``fix_len`` is ``True``, only integers with the exact number of
          ``digits`` can be generated.

        :sample: fix_len=False
        :sample: fix_len=True
        :sample: digits=3
        :sample: digits=3, fix_len=False
        :sample: digits=3, fix_len=True
        """
        if digits is None:
            digits = self.random_digit_not_null()
        if digits < 0:
            raise ValueError("The digit parameter must be greater than or equal to 0.")
        if fix_len:
            if digits > 0:
                return self.generator.random.randint(
                    pow(10, digits - 1), pow(10, digits) - 1)
            else:
                raise ValueError("A number of fixed length cannot have less than 1 digit in it.")
        else:
            return self.generator.random.randint(0, pow(10, digits) - 1)

    def random_letter(self):
        """Generate a random ASCII letter (a-z and A-Z).

        :sample:
        """
        return self.generator.random.choice(
            getattr(string, 'letters', string.ascii_letters))

    def random_letters(self, length=16):
        """Generate a list of random ASCII letters (a-z and A-Z) of the specified ``length``.

        :sample:
        :sample: length=10
        """
        return self.random_choices(
            getattr(string, 'letters', string.ascii_letters),
            length=length,
        )

    def random_lowercase_letter(self):
        """Generate a random lowercase ASCII letter (a-z).

        :sample:
        """
        return self.generator.random.choice(string.ascii_lowercase)

    def random_uppercase_letter(self):
        """Generate a random uppercase ASCII letter (A-Z).

        :sample:
        """
        return self.generator.random.choice(string.ascii_uppercase)

    def random_elements(self, elements=('a', 'b', 'c'), length=None, unique=False):
        """Generate a list of randomly sampled objects from ``elements``.

        Set ``unique`` to ``False`` for random sampling with replacement, and set ``unique`` to
        ``True`` for random sampling without replacement.

        If ``length`` is set to ``None`` or is omitted, ``length`` will be set to a random
        integer from 1 to the size of ``elements``.

        The value of ``length`` cannot be greater than the number of objects
        in ``elements`` if ``unique`` is set to ``True``.

        The value of ``elements`` can be any sequence type (``list``, ``tuple``, ``set``,
        ``string``, etc) or an ``OrderedDict`` type. If it is the latter, the keys will be
        used as the objects for sampling, and the values will be used as weighted probabilities
        if ``unique`` is set to ``False``. For example:

        .. code-block:: python

            # Random sampling with replacement
            fake.random_elements(
                elements=OrderedDict([
                    ("variable_1", 0.5),        # Generates "variable_1" 50% of the time
                    ("variable_2", 0.2),        # Generates "variable_2" 20% of the time
                    ("variable_3", 0.2),        # Generates "variable_3" 20% of the time
                    ("variable_4": 0.1),        # Generates "variable_4" 10% of the time
                ]), unique=False
            )

            # Random sampling without replacement (defaults to uniform distribution)
            fake.random_elements(
                elements=OrderedDict([
                    ("variable_1", 0.5),
                    ("variable_2", 0.2),
                    ("variable_3", 0.2),
                    ("variable_4": 0.1),
                ]), unique=True
            )

        :sample: elements=('a', 'b', 'c', 'd'), unique=False
        :sample: elements=('a', 'b', 'c', 'd'), unique=True
        :sample: elements=('a', 'b', 'c', 'd'), length=10, unique=False
        :sample: elements=('a', 'b', 'c', 'd'), length=4, unique=True
        :sample: elements=OrderedDict([
                        ("a", 0.45),
                        ("b", 0.35),
                       ("c", 0.15),
                       ("d", 0.05),
                   ]), length=20, unique=False
        :sample: elements=OrderedDict([
                       ("a", 0.45),
                       ("b", 0.35),
                       ("c", 0.15),
                       ("d", 0.05),
                   ]), unique=True
        """
        if isinstance(elements, dict) and not isinstance(elements, OrderedDict):
            raise ValueError("Use OrderedDict only to avoid dependency on PYTHONHASHSEED (See #363).")

        fn = choices_distribution_unique if unique else choices_distribution

        if length is None:
            length = self.generator.random.randint(1, len(elements))

        if unique and length > len(elements):
            raise ValueError(
                "Sample length cannot be longer than the number of unique elements to pick from.")

        if isinstance(elements, dict):
            choices = elements.keys()
            probabilities = elements.values()
        else:
            if unique:
                # shortcut
                return self.generator.random.sample(elements, length)
            choices = elements
            probabilities = [1.0 for _ in range(len(choices))]

        return fn(
            list(choices),
            list(probabilities),
            self.generator.random,
            length=length,
        )

    def random_choices(self, elements=('a', 'b', 'c'), length=None):
        """Generate a list of objects randomly sampled from ``elements`` with replacement.

        For information on the ``elements`` and ``length`` arguments, please refer to
        :meth:`random_elements() <faker.providers.BaseProvider.random_elements>` which
        is used under the hood with the ``unique`` argument explicitly set to ``False``.

        :sample: elements=('a', 'b', 'c', 'd')
        :sample: elements=('a', 'b', 'c', 'd'), length=10
        :sample: elements=OrderedDict([
                     ("a", 0.45),
                     ("b", 0.35),
                     ("c", 0.15),
                     ("d", 0.05),
                 ])
        :sample: elements=OrderedDict([
                     ("a", 0.45),
                     ("b", 0.35),
                     ("c", 0.15),
                     ("d", 0.05),
                 ]), length=20
        """
        return self.random_elements(elements, length, unique=False)

    def random_element(self, elements=('a', 'b', 'c')):
        """Generate a randomly sampled object from ``elements``.

        For information on the ``elements`` argument, please refer to
        :meth:`random_elements() <faker.providers.BaseProvider.random_elements>` which
        is used under the hood with the ``unique`` argument set to ``False`` and the
        ``length`` argument set to ``1``.

        :sample: elements=('a', 'b', 'c', 'd')
        :sample size=10: elements=OrderedDict([
                     ("a", 0.45),
                     ("b", 0.35),
                     ("c", 0.15),
                     ("d", 0.05),
                 ])
        """

        return self.random_elements(elements, length=1)[0]

    def random_sample(self, elements=('a', 'b', 'c'), length=None):
        """Generate a list of objects randomly sampled from ``elements`` without replacement.

        For information on the ``elements`` and ``length`` arguments, please refer to
        :meth:`random_elements() <faker.providers.BaseProvider.random_elements>` which
        is used under the hood with the ``unique`` argument explicitly set to ``True``.

        :sample: elements=('a', 'b', 'c', 'd', 'e', 'f')
        :sample: elements=('a', 'b', 'c', 'd', 'e', 'f'), length=3
        """
        return self.random_elements(elements, length, unique=True)

    def randomize_nb_elements(
            self,
            number=10,
            le=False,
            ge=False,
            min=None,
            max=None):
        """Generate a random integer near ``number`` according to the following rules:

        - If ``le`` is ``False`` (default), allow generation up to 140% of ``number``.
          If ``True``, upper bound generation is capped at 100%.
        - If ``ge`` is ``False`` (default), allow generation down to 60% of ``number``.
          If ``True``, lower bound generation is capped at 100%.
        - If a numerical value for ``min`` is provided, generated values less than ``min``
          will be clamped at ``min``.
        - If a numerical value for ``max`` is provided, generated values greater than
          ``max`` will be clamped at ``max``.
        - If both ``le`` and ``ge`` are ``True``, the value of ``number`` will automatically
          be returned, regardless of the values supplied for ``min`` and ``max``.

        :sample: number=100
        :sample: number=100, ge=True
        :sample: number=100, ge=True, min=120
        :sample: number=100, le=True
        :sample: number=100, le=True, max=80
        :sample: number=79, le=True, ge=True, min=80
        """
        if le and ge:
            return number
        _min = 100 if ge else 60
        _max = 100 if le else 140
        nb = int(number * self.generator.random.randint(_min, _max) / 100)
        if min is not None and nb < min:
            nb = min
        if max is not None and nb > max:
            nb = max
        return nb

    def numerify(self, text='###'):
        """Generate a string with each placeholder in ``text`` replaced according
        to the following rules:

        - Number signs ('#') are replaced with a random digit (0 to 9).
        - Percent signs ('%') are replaced with a random non-zero digit (1 to 9).
        - Exclamation marks ('!') are replaced with a random digit or an empty string.
        - At symbols ('@') are replaced with a random non-zero digit or an empty string.

        Under the hood, this method uses :meth:`random_digit() <faker.providers.BaseProvider.random_digit>`,
        :meth:`random_digit_not_null() <faker.providers.BaseProvider.random_digit_not_null>`,
        :meth:`random_digit_or_empty() <faker.providers.BaseProvider.random_digit_or_empty>`,
        and :meth:`random_digit_not_null_or_empty() <faker.providers.BaseProvider.random_digit_not_null_or_empty>`
        to generate the random values.

        :sample: text='Intel Core i%-%%##K vs AMD Ryzen % %%##X'
        :sample: text='!!! !!@ !@! !@@ @!! @!@ @@! @@@'
        """
        text = _re_hash.sub(
            lambda x: str(self.random_digit()),
            text)
        text = _re_perc.sub(
            lambda x: str(self.random_digit_not_null()),
            text)
        text = _re_excl.sub(
            lambda x: str(self.random_digit_or_empty()),
            text)
        text = _re_at.sub(
            lambda x: str(self.random_digit_not_null_or_empty()),
            text)
        return text

    def lexify(self, text='????', letters=string.ascii_letters):
        """Generate a string with each question mark ('?') in ``text``
        replaced with a random character from ``letters``.

        By default, ``letters`` contains all ASCII letters, uppercase and lowercase.

        :sample: text='Random Identifier: ??????????'
        :sample: text='Random Identifier: ??????????', letters='ABCDE'
        """
        return _re_qm.sub(lambda x: self.random_element(letters), text)

    def bothify(self, text='## ??', letters=string.ascii_letters, upper=False):
        """Generate a string with each placeholder in ``text`` replaced according
        to the following rules:

        - Number signs ('#') are replaced with a random digit (0 to 9).
        - Question marks ('?') are replaced with a random character from ``letters``.

        By default, ``letters`` contains all ASCII letters, uppercase and lowercase.

        Under the hood, this method uses :meth:`numerify() <faker.providers.BaseProvider.numerify>` and
        and :meth:`lexify() <faker.providers.BaseProvider.lexify>` to generate random values for number
        signs and question marks respectively.

        :sample: letters='ABCDE'
        :sample: text='Product Number: ????-########'
        :sample: text='Product Number: ????-########', letters='ABCDE'
        """
        result = self.lexify(self.numerify(text), letters=letters)
        return result.upper() if upper else result

    def hexify(self, text='^^^^', upper=False):
        """Generate a string with each circumflex ('^') in ``text``
        replaced with a random hexadecimal character.

        By default, ``upper`` is set to False. If set to ``True``, output
        will be formatted using uppercase hexadecimal characters.

        :sample: text='MAC Address: ^^:^^:^^:^^:^^:^^'
        :sample: text='MAC Address: ^^:^^:^^:^^:^^:^^', upper=True
        """
        letters = string.hexdigits[:-6]
        if upper:
            letters = letters.upper()
        return _re_cir.sub(lambda x: self.random_element(letters), text)
