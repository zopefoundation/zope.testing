from zope.testing.stringliterals import ALLOW_BYTES
from zope.testing.stringliterals import ALLOW_UNICODE
from zope.testing.stringliterals import LiteralsOutputChecker
import textwrap
import unittest


class TestLiteralsOutputChecker(unittest.TestCase):
    """Testing .renormalizing.LiteralsOutputChecker."""

    def setUp(self):
        super(TestLiteralsOutputChecker, self).setUp()
        self.checker = LiteralsOutputChecker()

    def test__LiteralsOutputChecker__check_output__1(self):
        """It works with simple strings."""
        want = textwrap.dedent("""\
            'Test string'
            """)
        got = textwrap.dedent("""\
            'Test string'
            """)
        self.assertTrue(self.checker.check_output(want, got, 0))

    def test__LiteralsOutputChecker__check_output__2(self):
        """It fails with simple strings."""
        want = textwrap.dedent("""\
            'Test string'
            """)
        got = textwrap.dedent("""\
            'False test string'
            """)
        self.assertFalse(self.checker.check_output(want, got, 0))

    def test__LiteralsOutputChecker__check_output__3(self):
        """It allows byte literals with option flag."""
        want = textwrap.dedent("""\
            'Test string'
            b'Test bytes'
            """)
        got = textwrap.dedent("""\
            b'Test string'
            'Test bytes'
            """)
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertTrue(self.checker.check_output(want, got, ALLOW_BYTES))

    def test__LiteralsOutputChecker__check_output__4(self):
        """It fails on byte literals with the ALLOW_UNICODE option flag."""
        want = textwrap.dedent("""\
            'Test string'
            b'Test bytes'
            """)
        got = textwrap.dedent("""\
            b'Test string'
            'Test bytes'
            """)
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertFalse(self.checker.check_output(want, got, ALLOW_UNICODE))

    def test__LiteralsOutputChecker__check_output__5(self):
        """It works allows unicode literals with option flag."""
        want = textwrap.dedent("""\
            'Test string'
            u'Test unicode'
            """)
        got = textwrap.dedent("""\
            u'Test string'
            'Test unicode'
            """)
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertTrue(self.checker.check_output(want, got, ALLOW_UNICODE))

    def test__LiteralsOutputChecker__check_output__6(self):
        """It fails on unicode literals with the ALLOW_BYTES option flag."""
        want = textwrap.dedent("""\
            'Test string'
            u'Test unicode'
            """)
        got = textwrap.dedent("""\
            u'Test string'
            'Test unicode'
            """)
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertFalse(self.checker.check_output(want, got, ALLOW_BYTES))

    def test__LiteralsOutputChecker__check_output__7(self):
        """It accepts both flags at the same time."""
        want = textwrap.dedent("""\
            'Test string'
            'Test unicode'
            'Test bytes'
            """)
        got = textwrap.dedent("""\
            'Test string'
            u'Test unicode'
            b'Test bytes'
            """)
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertTrue(self.checker.check_output(
            want, got, ALLOW_UNICODE | ALLOW_BYTES))
