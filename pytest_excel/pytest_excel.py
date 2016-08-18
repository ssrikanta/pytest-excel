
import re
from collections import OrderedDict
from openpyxl import Workbook
import pytest



_py_ext_re = re.compile(r"\.py$")



def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption('--excelreport', '--excel-report',
                    action="store",
                    dest="excelpath",
                    metavar="path",
                    default=None,
                    help="create excel report file at given path.")


def pytest_configure(config):
    excelpath = config.option.excelpath
    # prevent opening excel log on slave nodes (xdist)
    if excelpath:
        config._excel = ExcelReporter(excelpath)
        config.pluginmanager.register(config._excel)


def pytest_unconfigure(config):
    excel = getattr(config, '_excel', None)
    if excel:
        del config._excel
        config.pluginmanager.unregister(excel)


def mangle_test_address(address):
    path, possible_open_bracket, params = address.partition('[')
    names = path.split("::")
    try:
        names.remove('()')
    except ValueError:
        pass

    names[0] = names[0].replace("/", '.')
    names[0] = _py_ext_re.sub("", names[0])
    names[-1] += possible_open_bracket + params
    return names



class ExcelReporter(object):

    def __init__(self, excelpath):

        self.excelpath = excelpath
        self.results = []
        self.wbook = Workbook()
        self.rc = 1


    def append(self, result):
        print self.results
        self.results.append(result)

    @classmethod
    def create_sheet(cls, column_heading):

        cls.wsheet = cls.wbook.create_sheet(index=0)

        for heading in column_heading:
            index_value = column_heading.index(heading) + 1
            heading = heading.replace("_", " ").upper()
            cls.wsheet.cell(row=cls.rc, column=index_value).value = heading
        cls.rc = cls.rc + 1


    @classmethod
    def update_worksheet(cls):

        for data in cls.results:
            for key, value in data.iteritems():
                cls.wsheet.cell(row=cls.rc, column=data.keys().index(key) + 1).value = value
            cls.rc = cls.rc + 1

    @classmethod
    def save_excel(cls):
        cls.wbook.save(filename=cls.excelpath)


    def build_result(self, item, call, status, message):

        result = OrderedDict()
        names = mangle_test_address(item.nodeid)

        result['suite_name'] = names[-2]
        result['test_name'] = names[-1]
        if item.obj.__doc__ is None:
          result['description'] = item.obj.__doc__
        else:
          result['description'] = item.obj.__doc__.strip()

        result['result'] = status
        result['duration'] = call.stop - call.start
        result['message'] = message
        result['file_name'] = item.location[0]
        print
        self.append(result)


    def append_pass(self, item, call):
        if 'xfail' in item.keywords:
            status = "XPASSED"
            message = "xfail-marked test passes unexpectedly"
        else:
            status = "PASSED"
            message = None

        self.build_result(item, call, status, message)


    def append_failure(self, item, call):

        if 'xfail' in item.keywords:
            status = "XFAILED"
            message = "expected test failure "

        else:
            status = "FAILED"
            message = str(call.excinfo)

        self.build_result(item, call, status, message)


    def append_error(self, item, call):

        message = call.excinfo.getrepr(style='native')
        status = "ERROR"
        self.build_result(item, call, status, message)


    def append_skipped(self, item, call):

        if 'xfail' in item.keywords:
            status = "XFAILED"
            message = "expected test failure "

        else:
            status = "SKIPPED"
            r = call.excinfo._getreprcrash()
            message = str(r.message)

        self.build_result(item, call, status, message)


    def build_tests(self, item):

        result = OrderedDict()
        names = mangle_test_address(item.nodeid)

        result['suite_name'] = names[-2]
        result['test_name'] = names[-1]
        if item.obj.__doc__ is None:
          result['description'] = item.obj.__doc__
        else:
          result['description'] = item.obj.__doc__.strip()
        result['file_name'] = item.location[0]
        self.append(result)


    def append_tests(self, item):

        self.build_tests(item)


    @pytest.mark.trylast
    def pytest_collection_modifyitems(self, session, config, items):
        """ called after collection has been performed, may filter or re-order
        the items in-place."""
        if session.config.option.collectonly:
            for item in items:
                self.append_tests(item)


    def pytest_runtest_makereport(self, item, call):
        when = call.when
        excinfo = call.excinfo

        if when == 'call':
            if not call.excinfo:
                self.append_pass(item, call)
            else:
              self.append_failure(item, call)

        elif when == 'setup':

            if excinfo is not None:
                if excinfo.errisinstance(pytest.skip.Exception):
                    self.append_skipped(item, call)
                else:
                    self.append_error(item, call)

        else:
            if excinfo is not None:
                self.append_error(item, call)


    def pytest_sessionfinish(self):
        if self.results:
            fieldnames = self.results[0].keys()
            self.create_sheet(fieldnames)
            self.update_worksheet()
            self.save_excel()


    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep("-", "excel report: %s" % (self.excelpath))



