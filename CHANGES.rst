Release Notes
-------------


**0.1.1 (2016-08-04)**

* Initial release

**1.0.0 (2016-08-18)**

* Added support for Xdist plugin feature.


**1.0.1 (2016-08-18)**

* Added fix for excel file path


**1.1.0 (2016-08-18)**

* Added support to capture xfail and xpass reasons

**1.2.0 (2016-09-14)**

* Added support to include markers in the excel report

**1.2.1 (2017-01-31)**

* Fix for the issue obserevd on python3.6
* Fix for unicode related issues in python3.6


**1.2.2 (2017-02-01)**

* Fixes issue with report update method in python3.6


**1.2.3 (2018-06-14)**

* Fixes issue with marker information

**1.4.0 (2020-06-14)**

* Fixes issue with installation

**1.4.1 (2020-06-14)**

* Fixes issue with terminal reporting when no cases gets executed

**1.4.2 (2020-10-06)**

* Fixes license details

**1.5.2 (2023-17-20)**

* Fixes typo error

**1.6.0 (2023-09-14)**

* Replaced openpyexcel with Pandas

**1.8.0 (2025-07-16)**

* Support for Python 3.11 and above only
* Excel report file name can be set via pytest config or CLI (CLI overrides config)
* Warning row added to end of Excel report after session
* Refactored marker handling for compatibility with latest pytest
* Removed deprecated hook annotations and fixed lint errors


**1.8.1 (2025-07-22)**

* Fix issue with Excel report file name setting
