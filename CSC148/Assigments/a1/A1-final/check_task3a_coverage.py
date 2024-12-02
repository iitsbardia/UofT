"""CSC148 Assignment 1

CSC148 Fall 2024
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jonathan Calver, Sophia Huynh

All of the files in this directory are
Copyright (c) 148 Teaching Team.

Module Description:

Run this file to see the code coverage report for Task 3a.
"""

if __name__ == '__main__':
    import coverage
    import pytest

    # This is the basic usage of coverage; include lists which files we
    # want the coverage report for.
    cov = coverage.Coverage(include=['container.py'])
    cov.start()

    # call your code for coverage
    pytest.main(['test_priority_queue.py'])

    cov.stop()
    cov.save()

    # generate the html report (similar to what pyTA does)
    # and print the coverage percentage
    percent_covered = cov.html_report()

    print(f'Code coverage: {percent_covered :.2f}%')

    # code below would open up the detailed report in the browser (like pyTA).
    import webbrowser
    import os.path

    webbrowser.open(f'file://{os.path.dirname(__file__)}/htmlcov/index.html')
