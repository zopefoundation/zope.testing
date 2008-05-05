##############################################################################
#
# Copyright (c) 2004-2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Output formatting.

$Id: __init__.py 86207 2008-05-03 13:25:02Z ctheune $
"""

import sys
import re
import traceback

from zope.testing import doctest


doctest_template = """
File "%s", line %s, in %s

%s
Want:
%s
Got:
%s
"""


class OutputFormatter(object):
    """Test runner output formatter."""

    # Implementation note: be careful about printing stuff to sys.stderr.
    # It is used for interprocess communication between the parent and the
    # child test runner, when you run some test layers in a subprocess.
    # resume_layer() reasigns sys.stderr for this reason, but be careful
    # and don't store the original one in __init__ or something.

    max_width = 80

    def __init__(self, options):
        self.options = options
        self.last_width = 0
        self.compute_max_width()

    progress = property(lambda self: self.options.progress)
    verbose = property(lambda self: self.options.verbose)

    def compute_max_width(self):
        """Try to determine the terminal width."""
        # Note that doing this every time is more test friendly.
        self.max_width = tigetnum('cols', self.max_width)

    def getShortDescription(self, test, room):
        """Return a description of a test that fits in ``room`` characters."""
        room -= 1
        s = str(test)
        if len(s) > room:
            pos = s.find(" (")
            if pos >= 0:
                w = room - (pos + 5)
                if w < 1:
                    # first portion (test method name) is too long
                    s = s[:room-3] + "..."
                else:
                    pre = s[:pos+2]
                    post = s[-w:]
                    s = "%s...%s" % (pre, post)
            else:
                w = room - 4
                s = '... ' + s[-w:]

        return ' ' + s[:room]

    def info(self, message):
        """Print an informative message."""
        print message

    def info_suboptimal(self, message):
        """Print an informative message about losing some of the features.

        For example, when you run some tests in a subprocess, you lose the
        ability to use the debugger.
        """
        print message

    def error(self, message):
        """Report an error."""
        print message

    def error_with_banner(self, message):
        """Report an error with a big ASCII banner."""
        print
        print '*'*70
        self.error(message)
        print '*'*70
        print

    def profiler_stats(self, stats):
        """Report profiler stats."""
        stats.print_stats(50)

    def import_errors(self, import_errors):
        """Report test-module import errors (if any)."""
        if import_errors:
            print "Test-module import failures:"
            for error in import_errors:
                self.print_traceback("Module: %s\n" % error.module,
                                     error.exc_info),
            print

    def tests_with_errors(self, errors):
        """Report names of tests with errors (if any)."""
        if errors:
            print
            print "Tests with errors:"
            for test, exc_info in errors:
                print "  ", test

    def tests_with_failures(self, failures):
        """Report names of tests with failures (if any)."""
        if failures:
            print
            print "Tests with failures:"
            for test, exc_info in failures:
                print "  ", test

    def modules_with_import_problems(self, import_errors):
        """Report names of modules with import problems (if any)."""
        if import_errors:
            print
            print "Test-modules with import problems:"
            for test in import_errors:
                print "  " + test.module

    def format_seconds(self, n_seconds):
        """Format a time in seconds."""
        if n_seconds >= 60:
            n_minutes, n_seconds = divmod(n_seconds, 60)
            return "%d minutes %.3f seconds" % (n_minutes, n_seconds)
        else:
            return "%.3f seconds" % n_seconds

    def format_seconds_short(self, n_seconds):
        """Format a time in seconds (short version)."""
        return "%.3f s" % n_seconds

    def summary(self, n_tests, n_failures, n_errors, n_seconds):
        """Summarize the results of a single test layer."""
        print ("  Ran %s tests with %s failures and %s errors in %s."
               % (n_tests, n_failures, n_errors,
                  self.format_seconds(n_seconds)))

    def totals(self, n_tests, n_failures, n_errors, n_seconds):
        """Summarize the results of all layers."""
        print ("Total: %s tests, %s failures, %s errors in %s."
               % (n_tests, n_failures, n_errors,
                  self.format_seconds(n_seconds)))

    def list_of_tests(self, tests, layer_name):
        """Report a list of test names."""
        print "Listing %s tests:" % layer_name
        for test in tests:
            print ' ', test

    def garbage(self, garbage):
        """Report garbage generated by tests."""
        if garbage:
            print "Tests generated new (%d) garbage:" % len(garbage)
            print garbage

    def test_garbage(self, test, garbage):
        """Report garbage generated by a test."""
        if garbage:
            print "The following test left garbage:"
            print test
            print garbage

    def test_threads(self, test, new_threads):
        """Report threads left behind by a test."""
        if new_threads:
            print "The following test left new threads behind:"
            print test
            print "New thread(s):", new_threads

    def refcounts(self, rc, prev):
        """Report a change in reference counts."""
        print "  sys refcount=%-8d change=%-6d" % (rc, rc - prev)

    def detailed_refcounts(self, track, rc, prev):
        """Report a change in reference counts, with extra detail."""
        print ("  sum detail refcount=%-8d"
               " sys refcount=%-8d"
               " change=%-6d"
               % (track.n, rc, rc - prev))
        track.output()

    def start_set_up(self, layer_name):
        """Report that we're setting up a layer.

        The next output operation should be stop_set_up().
        """
        print "  Set up %s" % layer_name,
        sys.stdout.flush()

    def stop_set_up(self, seconds):
        """Report that we've set up a layer.

        Should be called right after start_set_up().
        """
        print "in %s." % self.format_seconds(seconds)

    def start_tear_down(self, layer_name):
        """Report that we're tearing down a layer.

        The next output operation should be stop_tear_down() or
        tear_down_not_supported().
        """
        print "  Tear down %s" % layer_name,
        sys.stdout.flush()

    def stop_tear_down(self, seconds):
        """Report that we've tore down a layer.

        Should be called right after start_tear_down().
        """
        print "in %s." % self.format_seconds(seconds)

    def tear_down_not_supported(self):
        """Report that we could not tear down a layer.

        Should be called right after start_tear_down().
        """
        print "... not supported"

    def start_test(self, test, tests_run, total_tests):
        """Report that we're about to run a test.

        The next output operation should be test_success(), test_error(), or
        test_failure().
        """
        self.test_width = 0
        if self.progress:
            if self.last_width:
                sys.stdout.write('\r' + (' ' * self.last_width) + '\r')

            s = "    %d/%d (%.1f%%)" % (tests_run, total_tests,
                                        tests_run * 100.0 / total_tests)
            sys.stdout.write(s)
            self.test_width += len(s)
            if self.verbose == 1:
                room = self.max_width - self.test_width - 1
                s = self.getShortDescription(test, room)
                sys.stdout.write(s)
                self.test_width += len(s)

        elif self.verbose == 1:
            sys.stdout.write('.' * test.countTestCases())

        if self.verbose > 1:
            s = str(test)
            sys.stdout.write(' ')
            sys.stdout.write(s)
            self.test_width += len(s) + 1

        sys.stdout.flush()

    def test_success(self, test, seconds):
        """Report that a test was successful.

        Should be called right after start_test().

        The next output operation should be stop_test().
        """
        if self.verbose > 2:
            s = " (%s)" % self.format_seconds_short(seconds)
            sys.stdout.write(s)
            self.test_width += len(s) + 1

    def test_error(self, test, seconds, exc_info):
        """Report that an error occurred while running a test.

        Should be called right after start_test().

        The next output operation should be stop_test().
        """
        if self.verbose > 2:
            print " (%s)" % self.format_seconds_short(seconds)
        print
        self.print_traceback("Error in test %s" % test, exc_info)
        self.test_width = self.last_width = 0

    def test_failure(self, test, seconds, exc_info):
        """Report that a test failed.

        Should be called right after start_test().

        The next output operation should be stop_test().
        """
        if self.verbose > 2:
            print " (%s)" % self.format_seconds_short(seconds)
        print
        self.print_traceback("Failure in test %s" % test, exc_info)
        self.test_width = self.last_width = 0

    def print_traceback(self, msg, exc_info):
        """Report an error with a traceback."""
        print
        print msg
        print self.format_traceback(exc_info)

    def format_traceback(self, exc_info):
        """Format the traceback."""
        v = exc_info[1]
        if isinstance(v, doctest.DocTestFailureException):
            tb = v.args[0]
        elif isinstance(v, doctest.DocTestFailure):
            tb = doctest_template % (
                v.test.filename,
                v.test.lineno + v.example.lineno + 1,
                v.test.name,
                v.example.source,
                v.example.want,
                v.got,
                )
        else:
            tb = "".join(traceback.format_exception(*exc_info))
        return tb

    def stop_test(self, test):
        """Clean up the output state after a test."""
        if self.progress:
            self.last_width = self.test_width
        elif self.verbose > 1:
            print
        sys.stdout.flush()

    def stop_tests(self):
        """Clean up the output state after a collection of tests."""
        if self.progress and self.last_width:
            sys.stdout.write('\r' + (' ' * self.last_width) + '\r')
        if self.verbose == 1 or self.progress:
            print


def tigetnum(attr, default=None):
    """Return a value from the terminfo database.

    Terminfo is used on Unix-like systems to report various terminal attributes
    (such as width, height or the number of supported colors).

    Returns ``default`` when the ``curses`` module is not available, or when
    sys.stdout is not a terminal.
    """
    try:
        import curses
    except ImportError:
        # avoid reimporting a broken module in python 2.3
        sys.modules['curses'] = None
    else:
        try:
            curses.setupterm()
        except (curses.error, TypeError):
            # You get curses.error when $TERM is set to an unknown name
            # You get TypeError when sys.stdout is not a real file object
            # (e.g. in unit tests that use various wrappers).
            pass
        else:
            return curses.tigetnum(attr)
    return default


def terminal_has_colors():
    """Determine whether the terminal supports colors.

    Some terminals (e.g. the emacs built-in one) don't.
    """
    return tigetnum('colors', -1) >= 8


class ColorfulOutputFormatter(OutputFormatter):
    """Output formatter that uses ANSI color codes.

    Like syntax highlighting in your text editor, colorizing
    test failures helps the developer.
    """

    # These colors are carefully chosen to have enough contrast
    # on terminals with both black and white background.
    colorscheme = {'normal': 'normal',
                   'default': 'default',
                   'info': 'normal',
                   'suboptimal-behaviour': 'magenta',
                   'error': 'brightred',
                   'number': 'green',
                   'slow-test': 'brightmagenta',
                   'ok-number': 'green',
                   'error-number': 'brightred',
                   'filename': 'lightblue',
                   'lineno': 'lightred',
                   'testname': 'lightcyan',
                   'failed-example': 'cyan',
                   'expected-output': 'green',
                   'actual-output': 'red',
                   'character-diffs': 'magenta',
                   'diff-chunk': 'magenta',
                   'exception': 'red'}

    # Map prefix character to color in diff output.  This handles ndiff and
    # udiff correctly, but not cdiff.  In cdiff we ought to highlight '!' as
    # expected-output until we see a '-', then highlight '!' as actual-output,
    # until we see a '*', then switch back to highlighting '!' as
    # expected-output.  Nevertheless, coloried cdiffs are reasonably readable,
    # so I'm not going to fix this.
    #   -- mgedmin
    diff_color = {'-': 'expected-output',
                  '+': 'actual-output',
                  '?': 'character-diffs',
                  '@': 'diff-chunk',
                  '*': 'diff-chunk',
                  '!': 'actual-output',}

    prefixes = [('dark', '0;'),
                ('light', '1;'),
                ('bright', '1;'),
                ('bold', '1;'),]

    colorcodes = {'default': 0, 'normal': 0,
                  'black': 30,
                  'red': 31,
                  'green': 32,
                  'brown': 33, 'yellow': 33,
                  'blue': 34,
                  'magenta': 35,
                  'cyan': 36,
                  'grey': 37, 'gray': 37, 'white': 37}

    slow_test_threshold = 10.0 # seconds

    def color_code(self, color):
        """Convert a color description (e.g. 'lightgray') to a terminal code."""
        prefix_code = ''
        for prefix, code in self.prefixes:
            if color.startswith(prefix):
                color = color[len(prefix):]
                prefix_code = code
                break
        color_code = self.colorcodes[color]
        return '\033[%s%sm' % (prefix_code, color_code)

    def color(self, what):
        """Pick a named color from the color scheme"""
        return self.color_code(self.colorscheme[what])

    def colorize(self, what, message, normal='normal'):
        """Wrap message in color."""
        return self.color(what) + message + self.color(normal)

    def error_count_color(self, n):
        """Choose a color for the number of errors."""
        if n:
            return self.color('error-number')
        else:
            return self.color('ok-number')

    def info(self, message):
        """Print an informative message."""
        print self.colorize('info', message)

    def info_suboptimal(self, message):
        """Print an informative message about losing some of the features.

        For example, when you run some tests in a subprocess, you lose the
        ability to use the debugger.
        """
        print self.colorize('suboptimal-behaviour', message)

    def error(self, message):
        """Report an error."""
        print self.colorize('error', message)

    def error_with_banner(self, message):
        """Report an error with a big ASCII banner."""
        print
        print self.colorize('error', '*'*70)
        self.error(message)
        print self.colorize('error', '*'*70)
        print

    def tear_down_not_supported(self):
        """Report that we could not tear down a layer.

        Should be called right after start_tear_down().
        """
        print "...", self.colorize('suboptimal-behaviour', "not supported")

    def format_seconds(self, n_seconds, normal='normal'):
        """Format a time in seconds."""
        if n_seconds >= 60:
            n_minutes, n_seconds = divmod(n_seconds, 60)
            return "%s minutes %s seconds" % (
                        self.colorize('number', '%d' % n_minutes, normal),
                        self.colorize('number', '%.3f' % n_seconds, normal))
        else:
            return "%s seconds" % (
                        self.colorize('number', '%.3f' % n_seconds, normal))

    def format_seconds_short(self, n_seconds):
        """Format a time in seconds (short version)."""
        if n_seconds >= self.slow_test_threshold:
            color = 'slow-test'
        else:
            color = 'number'
        return self.colorize(color, "%.3f s" % n_seconds)

    def summary(self, n_tests, n_failures, n_errors, n_seconds):
        """Summarize the results."""
        sys.stdout.writelines([
            self.color('info'), '  Ran ',
            self.color('number'), str(n_tests),
            self.color('info'), ' tests with ',
            self.error_count_color(n_failures), str(n_failures),
            self.color('info'), ' failures and ',
            self.error_count_color(n_errors), str(n_errors),
            self.color('info'), ' errors in ',
            self.format_seconds(n_seconds, 'info'), '.',
            self.color('normal'), '\n'])

    def totals(self, n_tests, n_failures, n_errors, n_seconds):
        """Report totals (number of tests, failures, and errors)."""
        sys.stdout.writelines([
            self.color('info'), 'Total: ',
            self.color('number'), str(n_tests),
            self.color('info'), ' tests, ',
            self.error_count_color(n_failures), str(n_failures),
            self.color('info'), ' failures, ',
            self.error_count_color(n_errors), str(n_errors),
            self.color('info'), ' errors in ',
            self.format_seconds(n_seconds, 'info'), '.',
            self.color('normal'), '\n'])

    def print_traceback(self, msg, exc_info):
        """Report an error with a traceback."""
        print
        print self.colorize('error', msg)
        v = exc_info[1]
        if isinstance(v, doctest.DocTestFailureException):
            self.print_doctest_failure(v.args[0])
        elif isinstance(v, doctest.DocTestFailure):
            # I don't think these are ever used... -- mgedmin
            tb = self.format_traceback(exc_info)
            print tb
        else:
            tb = self.format_traceback(exc_info)
            self.print_colorized_traceback(tb)

    def print_doctest_failure(self, formatted_failure):
        """Report a doctest failure.

        ``formatted_failure`` is a string -- that's what
        DocTestSuite/DocFileSuite gives us.
        """
        color_of_indented_text = 'normal'
        colorize_diff = False
        for line in formatted_failure.splitlines():
            if line.startswith('File '):
                m = re.match(r'File "(.*)", line (\d*), in (.*)$', line)
                if m:
                    filename, lineno, test = m.groups()
                    sys.stdout.writelines([
                        self.color('normal'), 'File "',
                        self.color('filename'), filename,
                        self.color('normal'), '", line ',
                        self.color('lineno'), lineno,
                        self.color('normal'), ', in ',
                        self.color('testname'), test,
                        self.color('normal'), '\n'])
                else:
                    print line
            elif line.startswith('    '):
                if colorize_diff and len(line) > 4:
                    color = self.diff_color.get(line[4], color_of_indented_text)
                    print self.colorize(color, line)
                else:
                    print self.colorize(color_of_indented_text, line)
            else:
                colorize_diff = False
                if line.startswith('Failed example'):
                    color_of_indented_text = 'failed-example'
                elif line.startswith('Expected:'):
                    color_of_indented_text = 'expected-output'
                elif line.startswith('Got:'):
                    color_of_indented_text = 'actual-output'
                elif line.startswith('Exception raised:'):
                    color_of_indented_text = 'exception'
                elif line.startswith('Differences '):
                    color_of_indented_text = 'normal'
                    colorize_diff = True
                else:
                    color_of_indented_text = 'normal'
                print line
        print

    def print_colorized_traceback(self, formatted_traceback):
        """Report a test failure.

        ``formatted_traceback`` is a string.
        """
        for line in formatted_traceback.splitlines():
            if line.startswith('  File'):
                m = re.match(r'  File "(.*)", line (\d*), in (.*)$', line)
                if m:
                    filename, lineno, test = m.groups()
                    sys.stdout.writelines([
                        self.color('normal'), '  File "',
                        self.color('filename'), filename,
                        self.color('normal'), '", line ',
                        self.color('lineno'), lineno,
                        self.color('normal'), ', in ',
                        self.color('testname'), test,
                        self.color('normal'), '\n'])
                else:
                    print line
            elif line.startswith('    '):
                print self.colorize('failed-example', line)
            elif line.startswith('Traceback (most recent call last)'):
                print line
            else:
                print self.colorize('exception', line)
        print
