pytest-excel
================


pytest-excel is a plugin for `py.test <http://pytest.org>`_ that allows to 
to create excel report for test results.


Requirements
------------

You will need the following prerequisites in order to use pytest-excel:

- Python 2.7, 3.4 or 3.5
- pytest 2.9.0 or newer
- opepyxl


Installation
------------

To install pytest-excel::

    $ pip install pytest-excel

Then run your tests with::

    $ py.test --excelreport=report.xls

If you would like more detailed output (one test per line), then you may use the verbose option::

    $ py.test --verbose

If you would like to run tests without execution to collect test doc string::

    $ py.test --excelreport=report.xls --collect-only
