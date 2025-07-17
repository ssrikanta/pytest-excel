import pytest

# Example hook to add a link to the Excel report
def add_example_link(item, call, report):
    # Add a link for a specific test
    if 'test_excel_report_with_link' in report.nodeid:
        return 'https://example.com/test-details/{}'.format(report.nodeid)
    return None

def pytest_configure(config):
    if not hasattr(config, 'excel_extra_link_hooks'):
        config.excel_extra_link_hooks = []
    config.excel_extra_link_hooks.append(add_example_link)

class Test_Excel_Report:
    def test_excel_report_with_link(self):
        """
        Scenario: test_excel_report_with_link
        """
        assert True

    def test_excel_report_01(self):
        """
        Scenario: test_excel_report_01
        """
        assert True

    @pytest.mark.xfail(reason="passed Simply")
    def test_excel_report_02(self):
        """
        Scenario: test_excel_report_02
        """
        assert True

    @pytest.mark.skip(reason="Skip for No Reason")
    def test_excel_report_03(self):
        """
        Scenario: test_excel_report_01
        """
        assert True

    @pytest.mark.xfail(reason="Failed Simply")
    def test_excel_report_04(self):
        """
        Scenario: test_excel_report_05
        """
        assert False

    def test_excel_report_05(self):
        """
        Scenario: test_excel_report_06
        """
        assert True is False


