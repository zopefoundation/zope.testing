import sys
import textwrap
import unittest

from zope.testing.renormalizing import (
    is_dotted_name,
    strip_dottedname_from_traceback,
)


class Exception2To3(unittest.TestCase):

    def test_is_dotted_name_ascii_no_dots(self):
        self.assertTrue(is_dotted_name('FooBarError'))

    def test_is_dotted_name_ascii_dots(self):
        self.assertTrue(is_dotted_name('foo.bar.FooBarError'))

    def test_is_dotted_name_unicode_no_dots(self):
        result = is_dotted_name(u'FooB\xe1rError')
        if sys.version_info[0] >= 3:  # pragma: PY3
            self.assertTrue(result)
        else:  # pragma: PY2
            self.assertFalse(result)

    def test_is_dotted_name_unicode_dots(self):
        result = is_dotted_name(u'foo.b\xe1r.FooB\xe1rError')
        if sys.version_info[0] >= 3:  # pragma: PY3
            self.assertTrue(result)
        else:  # pragma: PY2
            self.assertFalse(result)

    def test_is_dotted_name_ellipsis(self):
        self.assertFalse(is_dotted_name('...'))

    def test_is_dotted_name_not_identifier(self):
        self.assertFalse(is_dotted_name('foo=bar'))

    def test_strip_dottedname(self):
        string = textwrap.dedent("""\
            Traceback (most recent call last):
            foo.bar.FooBarError: requires at least one argument.""")
        expected = textwrap.dedent("""\
            Traceback (most recent call last):
            FooBarError: requires at least one argument.""")
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_strip_dottedname_without_exception_arguments(self):
        string = textwrap.dedent("""\
            Traceback (most recent call last):
            foo.bar.FooBarError""")
        expected = textwrap.dedent("""\
            Traceback (most recent call last):
            FooBarError""")
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_no_dots_in_name(self):
        string = textwrap.dedent("""\
            Traceback (most recent call last):
            FooBarError: requires at least one argument.""")
        expected = textwrap.dedent("""\
            Traceback (most recent call last):
            FooBarError: requires at least one argument.""")
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_no_colon_in_first_word(self):
        string = textwrap.dedent("""\
            Traceback (most recent call last):
            foo.bar.FooBarError requires at least one argument.""")
        expected = textwrap.dedent("""\
            Traceback (most recent call last):
            foo.bar.FooBarError requires at least one argument.""")
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_input_empty(self):
        string = ''
        expected = ''
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_input_spaces(self):
        string = '   '
        expected = '   '
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_input_ellipsis(self):
        string = '...'
        expected = '...'
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_input_last_line_not_dotted_name(self):
        string = 'foo=bar'
        expected = 'foo=bar'
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_last_line_empty(self):
        string = textwrap.dedent("""\
            Traceback (most recent call last):

            """)
        expected = textwrap.dedent("""\
            Traceback (most recent call last):

            """)
        self.assertEqual(expected, strip_dottedname_from_traceback(string))
