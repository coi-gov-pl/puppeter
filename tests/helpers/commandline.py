import sys
from contextlib import contextmanager
from io import BytesIO, StringIO


@contextmanager
def captured_output():
    if sys.version_info >= (3, 0):
        new_out, new_err = StringIO(), StringIO()
    else:
        new_out, new_err = BytesIO(), BytesIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
