import doctest
import re

ALLOW_UNICODE = doctest.register_optionflag('ALLOW_UNICODE')
ALLOW_BYTES = doctest.register_optionflag('ALLOW_BYTES')


class LiteralsOutputChecker(doctest.OutputChecker):
    """A checker with support for u/b literals.

    Use the option flags from this module to get the desired effects:
        ALLOW_UNICODE removes u/U prefixes
        ALLOW_BYTES   removes b/B prefixes

    This version was copied from pytest
        https://github.com/pytest-dev/pytest/blob/master/_pytest/doctest.py
    which commented:

    Copied from doctest_nose_plugin.py from the nltk project:
        https://github.com/nltk/nltk
    Further extended to also support byte literals.
    """

    _unicode_literal_re = re.compile(r"(\W|^)[uU]([rR]?[\'\"])", re.UNICODE)
    _bytes_literal_re = re.compile(r"(\W|^)[bB]([rR]?[\'\"])", re.UNICODE)

    def check_output(self, want, got, optionflags):
        res = doctest.OutputChecker.check_output(self, want, got,
                                                 optionflags)
        if res:
            return True

        allow_unicode = optionflags & ALLOW_UNICODE
        allow_bytes = optionflags & ALLOW_BYTES
        if not allow_unicode and not allow_bytes:
            return False

        else:
            def remove_prefixes(regex, txt):
                return re.sub(regex, r'\1\2', txt)

            if allow_unicode:
                want = remove_prefixes(self._unicode_literal_re, want)
                got = remove_prefixes(self._unicode_literal_re, got)
            if allow_bytes:
                want = remove_prefixes(self._bytes_literal_re, want)
                got = remove_prefixes(self._bytes_literal_re, got)
            res = doctest.OutputChecker.check_output(self, want, got,
                                                     optionflags)
            return res
