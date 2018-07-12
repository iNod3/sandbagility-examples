from Sandbagility import Helper
from Sandbagility.Core import FDP

import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Trace a process activity, including its childs .')
    parser.add_argument('--vm', default="Windows 10 x64 - 14393", help='Virtual Machine name')

    args = parser.parse_args()

    helper = Helper(args.vm, FDP)

    for Process in helper.PsEnumProcesses(Detail=True):
        print(Process)

    for Module in helper.PsEnumLoadedModule():
        print('\t', Module)

    helper.dbg.Resume()
