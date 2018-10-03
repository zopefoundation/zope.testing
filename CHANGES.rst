Changes
=======

4.6.3 (unreleased)
------------------

- Added support for Python 3.7.


4.6.2 (2017-06-12)
------------------

- Remove dependencies on ``zope.interface`` and ``zope.exceptions``;
  they're not used here.

- Remove use of 2to3 for outdated versions of PyPy3, letting us build
  universal wheels.


4.6.1 (2017-01-04)
------------------

- Add support for Python 3.6.


4.6.0 (2016-10-20)
------------------

- Introduce option flag ``IGNORE_EXCEPTION_MODULE_IN_PYTHON2`` to normalize
  exception class names in traceback output. In Python 3 they are displayed as
  the full dotted name. In Python 2 they are displayed as "just" the class
  name.  When running doctests in Python 3, the option flag will not have any
  effect, however when running the same test in Python 2, the segments in the
  full dotted name leading up to the class name are stripped away from the
  "expected" string.

- Drop support for Python 2.6 and 3.2.

- Add support for Python 3.5.

- Cleaned up useless 2to3 conversion.

4.5.0 (2015-09-02)
------------------

- Added meta data for test case methods created with
  ``zope.testing.doctestcase``.

  - Reasonable values for ``__name__``, making sure that ``__name__``
    starts with ``test``.

  - For ``doctestfile`` methods, provide ``filename`` and ``filepath``
    attributes.

  The meta data us useful, for example, for selecting tests with the
  nose attribute mechanism.

- Added ``doctestcase.doctestfiles``

  - Define multiple doctest files at once.

  - Automatically assign test class members.  So rather than::

      class MYTests(unittest.TestCase):
          ...
          test_foo = doctestcase.doctestfile('foo.txt')

    You can use::

      @doctestcase.doctestfiles('foo.txt', 'bar.txt', ...)
      class MYTests(unittest.TestCase):
          ...

4.4.0 (2015-07-16)
------------------

- Added ``zope.testing.setupstack.mock`` as a convenience function for
  setting up mocks in tests.  (The Python ``mock`` package must be in
  the path for this to work. The excellent ``mock`` package isn't a
  dependency of ``zope.testing``.)

- Added the base class ``zope.testing.setupstack.TestCase`` to make it
  much easier to use ``zope.testing.setupstack`` in ``unittest`` test
  cases.


4.3.0 (2015-07-15)
------------------

- Added support for creating doctests as methods of
  ``unittest.TestCase`` classes so that they can found automatically
  by test runners, like *nose* that ignore test suites.

4.2.0 (2015-06-01)
------------------

- **Actually** remove long-deprecated ``zope.testing.doctest`` (announced as
  removed in 4.0.0) and ``zope.testing.doctestunit``.

- Add support for PyPy and PyPy3.

4.1.3 (2014-03-19)
------------------

- Add support for Python 3.4.

- Update ``boostrap.py`` to version 2.2.

4.1.2 (2013-02-19)
------------------

- Adjust Trove classifiers to reflect the currently supported Python
  versions. Officially drop Python 2.4 and 2.5. Add Python 3.3.

- LP: #1055720: Fix failing test on Python 3.3 due to changed exception
  messaging.

4.1.1 (2012-02-01)
------------------

- Fix: Windows test failure.

4.1.0 (2012-01-29)
------------------

- Add context-manager support to ``zope.testing.setupstack``

- Make ``zope.testing.setupstack`` usable with all tests, not just
  doctests and added ``zope.testing.setupstack.globs``, which makes it
  easier to write test setup code that workes with doctests and other
  kinds of tests.

- Add the ``wait`` module, which makes it easier to deal with
  non-deterministic timing issues.

- Rename ``zope.testing.renormalizing.RENormalizing`` to
  ``zope.testing.renormalizing.OutputChecker``. The old name is an
  alias.

- Update tests to run with Python 3.

- Label more clearly which features are supported by Python 3.

- Reorganize documentation.

4.0.0 (2011-11-09)
------------------

- Remove the deprecated ``zope.testing.doctest``.

- Add Python 3 support.

- Fix test which fails if there is a file named `Data.fs` in the current
  working directory.


3.10.2 (2010-11-30)
-------------------

- Fix test of broken symlink handling to not break on Windows.


3.10.1 (2010-11-29)
-------------------

- Fix removal of broken symlinks on Unix.


3.10.0 (2010-07-21)
-------------------

- Remove ``zope.testing.testrunner``, which now is moved to zope.testrunner.

- Update fix for LP #221151 to a spelling compatible with Python 2.4.

3.9.5 (2010-05-19)
------------------

- LP #579019: When layers are run in parallel, ensure that each ``tearDown``
  is called, including the first layer which is run in the main
  thread.

- Deprecate ``zope.testing.testrunner`` and ``zope.testing.exceptions``.
  They have been moved to a separate zope.testrunner module, and will be
  removed from zope.testing in 4.0.0, together with ``zope.testing.doctest``.

3.9.4 (2010-04-13)
------------------

- LP #560259: Fix subunit output formatter to handle layer setup
  errors.

- LP #399394:  Add a ``--stop-on-error`` / ``--stop`` / ``-x`` option to
  the testrunner.

- LP #498162:  Add a ``--pdb`` alias for the existing ``--post-mortem``
  / ``-D`` option to the testrunner.

- LP #547023:  Add a ``--version`` option to the testrunner.

- Add tests for LP #144569 and #69988.

  https://bugs.launchpad.net/bugs/69988

  https://bugs.launchpad.net/zope3/+bug/144569


3.9.3 (2010-03-26)
------------------

- Remove import of ``zope.testing.doctest`` from ``zope.testing.renormalizer``.

- Suppress output to ``sys.stderr`` in ``testrunner-layers-ntd.txt``.

- Suppress ``zope.testing.doctest`` deprecation warning when running
  our own test suite.


3.9.2 (2010-03-15)
------------------

- Fix broken ``from zope.testing.doctest import *``

3.9.1 (2010-03-15)
------------------

- No changes; reupload to fix broken 3.9.0 release on PyPI.

3.9.0 (2010-03-12)
------------------

- Modify the testrunner to use the standard Python ``doctest`` module instead
  of the deprecated ``zope.testing.doctest``.

- Fix ``testrunner-leaks.txt`` to use the ``run_internal`` helper, so that
  ``sys.exit`` isn't triggered during the test run.

- Add support for conditionally using a subunit-based output
  formatter upon request if subunit and testtools are available. Patch
  contributed by Jonathan Lange.

3.8.7 (2010-01-26)
------------------

- Downgrade the ``zope.testing.doctest`` deprecation warning into a
  PendingDeprecationWarning.

3.8.6 (2009-12-23)
------------------

- Add ``MANIFEST.in`` and reupload to fix broken 3.8.5 release on PyPI.


3.8.5 (2009-12-23)
------------------

- Add back ``DocFileSuite``, ``DocTestSuite``, ``debug_src`` and ``debug``
  BBB imports back into ``zope.testing.doctestunit``; apparently many packages
  still import them from there!

- Deprecate ``zope.testing.doctest`` and ``zope.testing.doctestunit``
  in favor of the stdlib ``doctest`` module.


3.8.4 (2009-12-18)
------------------

- Fix missing imports and undefined variables reported by pyflakes,
  adding tests to exercise the blind spots.

- Cleaned up unused imports reported by pyflakes.

- Add two new options to generate randomly ordered list of tests and to
  select a specific order of tests.

- Allow combining RENormalizing checkers via ``+`` now:
  ``checker1 + checker2`` creates a checker with the transformations of both
  checkers.

- Fix tests under Python 2.7.

3.8.3 (2009-09-21)
------------------

- Fix test failures due to using ``split()`` on filenames when running from a
  directory with spaces in it.

- Fix testrunner behavior on Windows for ``-j2`` (or greater) combined with
  ``-v`` (or greater).

3.8.2 (2009-09-15)
------------------

- Remove hotshot profiler when using Python 2.6. That makes zope.testing
  compatible with Python 2.6


3.8.1 (2009-08-12)
------------------

- Avoid hardcoding ``sys.argv[0]`` as script;
  allow, for instance, Zope 2's `bin/instance test` (LP#407916).

- Produce a clear error message when a subprocess doesn't follow the
  ``zope.testing.testrunner`` protocol (LP#407916).

- Avoid unnecessarily squelching verbose output in a subprocess when there are
  not multiple subprocesses.

- Avoid unnecessarily batching subprocess output, which can stymie automated
  and human processes for identifying hung tests.

- Include incremental output when there are multiple subprocesses and a
  verbosity of ``-vv`` or greater is requested.  This again is not batched,
  supporting automated processes and humans looking for hung tests.


3.8.0 (2009-07-24)
------------------

- Allow testrunner to include descendants of ``unittest.TestCase`` in test
  modules, which no longer need to provide ``test_suite()``.


3.7.7 (2009-07-15)
------------------

- Clean up support for displaying tracebacks with supplements by turning it
  into an always-enabled feature and making the dependency on
  ``zope.exceptions`` explicit.

- Fix #251759: prevent the testrunner descending into directories that
  aren't Python packages.

- Code cleanups.


3.7.6 (2009-07-02)
------------------

- Add zope-testrunner ``console_scripts`` entry point. This exposes a
  ``zope-testrunner`` script with default installs allowing the testrunner
  to be run from the command line.

3.7.5 (2009-06-08)
------------------

- Fix bug when running subprocesses on Windows.

- The option ``REPORT_ONLY_FIRST_FAILURE`` (command line option "-1") is now
  respected even when a doctest declares its own ``REPORTING_FLAGS``, such as
  ``REPORT_NDIFF``.

- Fix bug that broke readline with pdb when using doctest
  (see http://bugs.python.org/issue5727).

- Make tests pass on Windows and Linux at the same time.


3.7.4 (2009-05-01)
------------------

- Filenames of doctest examples now contain the line number and not
  only the example number. So a stack trace in pdb tells the exact
  line number of the current example. This fixes
  https://bugs.launchpad.net/bugs/339813

- Colorization of doctest output correctly handles blank lines.


3.7.3 (2009-04-22)
------------------

- Improve handling of rogue threads:  always exit with status so even
  spinning daemon threads won't block the runner from exiting. This deprecated
  the ``--with-exit-status`` option.


3.7.2 (2009-04-13)
------------------

- Fix test failure on Python 2.4 due to slight difference in the way
  coverage is reported (__init__ files with only a single comment line are now
  not reported)

- Fix bug that caused the test runner to hang when running subprocesses (as a
  result Python 2.3 is no longer supported).

- Work around a bug in Python 2.6 (related to
  http://bugs.python.org/issue1303673) that causes the profile tests to fail.

- Add explanitory notes to ``buildout.cfg`` about how to run the tests with
  multiple versions of Python


3.7.1 (2008-10-17)
------------------

- The ``setupstack`` temporary directory support now properly handles
  read-only files by making them writable before removing them.


3.7.0 (2008-09-22)
------------------

- Add alterate setuptools / distutils commands for running all tests
  using our testrunner.  See 'zope.testing.testrunner.eggsupport:ftest'.

- Add a setuptools-compatible test loader which skips tests with layers:
  the testrunner used by ``setup.py test`` doesn't know about them, and those
  tests then fail.  See ``zope.testing.testrunner.eggsupport:SkipLayers``.

- Add support for Jython, when a garbage collector call is sent.

- Add support to bootstrap on Jython.

- Fix NameError in StartUpFailure.

- Open doctest files in universal mode, so that packages released on Windows
  can be tested on Linux, for example.


3.6.0 (2008-07-10)
------------------

- Add ``-j`` option to parallel tests run in subprocesses.

- RENormalizer accepts plain Python callables.

- Add ``--slow-test`` option.

- Add ``--no-progress`` and ``--auto-progress`` options.

- Complete refactoring of the test runner into multiple code files and a more
  modular (pipeline-like) architecture.

- Unify unit tests with the layer support by introducing a real unit test
  layer.

- Add a doctest for ``zope.testing.module``. There were several bugs
  that were fixed:

  * ``README.txt`` was a really bad default argument for the module
    name, as it is not a proper dotted name. The code would
    immediately fail as it would look for the ``txt`` module in the
    ``README`` package. The default is now ``__main__``.

  * The ``tearDown`` function did not clean up the ``__name__`` entry in the
    global dictionary.

- Fix a bug that caused a SubprocessError to be generated if a subprocess
  sent any output to stderr.

- Fix a bug that caused the unit tests to be skipped if run in a subprocess.


3.5.1 (2007-08-14)
------------------

- Invoke post-mortem debugging for layer-setup failures.

3.5.0 (2007-07-19)
------------------

- Ensure that the test runner works on Python 2.5.

- Add support for ``cProfile``.

- Add output colorizing (``-c`` option).

- Add ``--hide-secondary-failures`` and ``--show-secondary-failures`` options
  (https://bugs.launchpad.net/zope3/+bug/115454).

- Fix some problems with Unicode in doctests.

- Fix "Error reading from subprocess" errors on Unix-like systems.

3.4 (2007-03-29)
----------------

- Add ``exit-with-status`` support (supports use with buildbot and
  ``zc.recipe.testing``)

- Add a small framework for automating set up and tear down of
  doctest tests. See ``setupstack.txt``.

- Allow ``testrunner-wo-source.txt`` and ``testrunner-errors.txt`` to run
  within a read-only source tree.

3.0 (2006-09-20)
----------------

- Update the doctest copy with text-file encoding support.

- Add logging-level support to the ``loggingsuppport`` module.

- At verbosity-level 1, dots are not output continuously, without any
  line breaks.

- Improve output when the inability to tear down a layer causes tests
  to be run in a subprocess.

- Make ``zope.exception`` required only if the ``zope_tracebacks`` extra is
  requested.

- Fix the test coverage. If a module, for example `interfaces`, was in an
  ignored directory/package, then if a module of the same name existed in a
  covered directory/package, then it was also ignored there, because the
  ignore cache stored the result by module name and not the filename of the
  module.

2.0 (2006-01-05)
----------------

- Release a separate project corresponding to the version of ``zope.testing``
  shipped as part of the Zope 3.2.0 release.
