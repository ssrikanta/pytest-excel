
import pytest


class Test_Excel_Report(object):
  
    
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


