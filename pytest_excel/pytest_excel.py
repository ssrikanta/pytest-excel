
import re
from collections import OrderedDict
from openpyxl import Workbook
import pytest
from _pytest.mark.structures import Mark


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
        self.results = []
        self.wbook = Workbook()
        self.rc = 1
        self.excelpath = excelpath


    def append(self, result):
        self.results.append(result)


    def create_sheet(self, column_heading):

        self.wsheet = self.wbook.create_sheet(index=0)

        for heading in column_heading:
            index_value = column_heading.index(heading) + 1
            heading = heading.replace("_", " ").upper()
            self.wsheet.cell(row=self.rc, column=index_value).value = heading
        self.rc = self.rc + 1


    def update_worksheet(self):
        for data in self.results:
            for key, value in data.items():
                self.wsheet.cell(row=self.rc, column=list(data).index(key) + 1).value = value
            self.rc = self.rc + 1


    def save_excel(self):
        self.wbook.save(filename=self.excelpath)


    def build_result(self, report, status, message):

        result = OrderedDict()
        names = mangle_test_address(report.nodeid)

        result['suite_name'] = names[-2]
        result['test_name'] = names[-1]
        if report.test_doc is None:
          result['description'] = report.test_doc
        else:
          result['description'] = report.test_doc.strip()

        result['result'] = status
        result['duration'] = getattr(report, 'duration', 0.0)
        result['message'] = message
        result['file_name'] = report.location[0]
        result['markers'] = report.test_marker
        self.append(result)


    def append_pass(self, report):
        status = "PASSED"
        message = None
        self.build_result(report, status, message)


    def append_failure(self, report):

        if hasattr(report, "wasxfail"):
            status = "XPASSED"
            message = "xfail-marked test passes Reason: %s " % report.wasxfail

        else:
            if hasattr(report.longrepr, "reprcrash"):
                message = report.longrepr.reprcrash.message
            elif isinstance(report.longrepr, (unicode, str)):
                message = report.longrepr
            else:
                message = str(report.longrepr)

            status = "FAILED"

        self.build_result(report, status, message)


    def append_error(self, report):

        message = report.longrepr
        status = "ERROR"
        self.build_result(report, status, message)


    def append_skipped(self, report):

        if hasattr(report, "wasxfail"):
            status = "XFAILED"
            message = "expected test failure Reason: %s " % report.wasxfail

        else:
            status = "SKIPPED"
            _, _, message = report.longrepr
            if message.startswith("Skipped: "):
                message = message[9:]

        self.build_result(report, status, message)


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


    @pytest.mark.hookwrapper
    def pytest_runtest_makereport(self, item, call):

        outcome = yield

        report = outcome.get_result()
        report.test_doc = item.obj.__doc__
        test_marker = []
        for k, v in item.keywords.items():
            if isinstance(v,list):
                for x in v:
                    if isinstance(x,Mark):
                        test_marker.append(x.name)
        report.test_marker = ', '.join(test_marker)


    def pytest_runtest_logreport(self, report):

        if report.passed:
            if report.when == "call":  # ignore setup/teardown
                self.append_pass(report)

        elif report.failed:
            if report.when == "call":
                self.append_failure(report)

            else:
                self.append_error(report)

        elif report.skipped:
            self.append_skipped(report)


    def pytest_sessionfinish(self, session):
        if not hasattr(session.config, 'slaveinput'):
            if self.results:
                fieldnames = list(self.results[0])
                self.create_sheet(fieldnames)
                self.update_worksheet()
                self.save_excel()


    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep("-", "excel report: %s" % (self.excelpath))

