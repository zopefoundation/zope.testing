import unittest
import textwrap
from zope.testing.renormalizing import strip_dottedname_from_traceback


class Exception2To3(unittest.TestCase):

    def test_strip_dottedname(self):
        string = """\
        Traceback (most recent call last):
        foo.bar.FooBarError: requires at least one argument."""
        string = textwrap.dedent(string)
        expected = """\
        Traceback (most recent call last):
        FooBarError: requires at least one argument."""
        expected = textwrap.dedent(expected)
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_no_dots_in_name(self):
        string = """\
        Traceback (most recent call last):
        FooBarError: requires at least one argument."""
        string = textwrap.dedent(string)
        expected = """\
        Traceback (most recent call last):
        FooBarError: requires at least one argument."""
        expected = textwrap.dedent(expected)
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_no_colon_in_first_word(self):
        string = """\
        Traceback (most recent call last):
        foo.bar.FooBarError requires at least one argument."""
        string = textwrap.dedent(string)
        expected = """\
        Traceback (most recent call last):
        foo.bar.FooBarError requires at least one argument."""
        expected = textwrap.dedent(expected)
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_input_empty(self):
        string = ''
        expected = ''
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_input_spaces(self):
        string = '   '
        expected = '   '
        self.assertEqual(expected, strip_dottedname_from_traceback(string))

    def test_last_line_empty(self):
        string = """\
        Traceback (most recent call last):

        """
        string = textwrap.dedent(string)
        expected = """\
        Traceback (most recent call last):

        """
        expected = textwrap.dedent(expected)
        self.assertEqual(expected, strip_dottedname_from_traceback(string))
