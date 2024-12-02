"""CSC148 Prep 2: Object Oriented Programming

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 David Liu, Diane Horton, and Sophia Huynh

=== Module Description ===
This module contains a function to be tested in prep2_starter_tests.py



You DO NOT need to modify this file, nor submit it.
"""


def coverage_example(x: int) -> bool:
    """
    Returns a different boolean based on the value of x.
    """
    if x == 0:
        return True
    elif x < 0:
        return False
    elif x in [1, 10, 100]:
        return True
    else:
        return False


if __name__ == '__main__':
    import pytest
    import coverage

    # This creates a Coverage() object and starts recording information
    # about which lines have been run in prep2_coverage_example.py
    cov = coverage.Coverage(include=['prep2_coverage_example.py'])
    cov.start()

    # This line runs the pytest cases in prep2_starter_tests.py
    pytest.main(['prep2_starter_tests.py'])

    # These lines stop recording information and saves it
    cov.stop()
    cov.save()

    # The line below will print the report to the Python Console.
    # You should see something like:
    # Name                         Stmts   Miss  Cover
    # ------------------------------------------------
    # prep2_coverage_example.py       8      5    38%
    # ------------------------------------------------
    # TOTAL                            8      5    38%
    cov.report()

    # The line below will generate a folder called htmlcov
    # Open the index.html page to see the coverage report. You can
    # click on the "prep2_coverage_example.py" module there to see
    # which lines might be missing.
    cov.html_report()
