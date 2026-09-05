#!/usr/bin/env python3
"""Compatibility wrapper for running Iris as `python iris.py`."""

import sys

from iris.cli import main

if __name__ == "__main__":
    sys.exit(main())
