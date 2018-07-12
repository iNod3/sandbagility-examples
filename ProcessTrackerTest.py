from Sandbagility import Helper
from Sandbagility.Core import FDP

from Sandbagility.Plugins import Automation

import sys

if __name__ == '__main__':

    helper = Helper("Windows 10 x64 - 14393", FDP)
    Automation.Parser(helper, sys.argv[1:])
