# -*- coding: utf-8 -*-

from os.path import (abspath, dirname, isdir)
import pep8

CURRENT_DIR = dirname(abspath(__file__))
BASE_DIR = dirname(CURRENT_DIR)


def test_pep8():
    arglist = [
        "--statistics",
        "--filename=*.py",
        "--show-source",
        "--repeat",
        "--exclude=SVGdraw.py",
        "--ignore=E302,E701",
        #"--show-pep8",
        #"-qq",
        #"-v",
        BASE_DIR,
    ]

    options, args = pep8.process_options(arglist)
    runner = pep8.input_file

    for path in args:
        if isdir(path):
            pep8.input_dir(path, runner=runner)
        elif not pep8.excluded(path):
            options.counters["files"] += 1
            runner(path)

    pep8.print_statistics()
    errors = pep8.get_count("E")
    warnings = pep8.get_count("W")
    message = "pep8: %d errors / %d warnings" % (errors, warnings)
    print(message)
    assert errors + warnings == 0, message
