from Sandbagility import Helper
from Sandbagility.Core import FDP

import argparse

from Sandbagility.Plugins import ProcessTracker

import os
import sys

from Sandbagility.Plugins import Automation
from Sandbagility.Plugins import PsWaitForSingleProcessAsync
from Sandbagility.Plugins import HyperWin32Api as HyperApi
from Sandbagility.Monitors import AvailableMonitors

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Trace a process activity, including its childs .')
    parser.add_argument('--process', type=str, default='explorer.exe', help='Process name to trace')
    parser.add_argument('--entrypoint', action='store_true', help='Break at the entrpoint of the target process')
    parser.add_argument('--vm', default="Windows 10 x64 - 14393", help='Virtual Machine name')
    parser.add_argument('--output', default='D:\\Jail\\DroppedFiles\\', help='Output directory for dumped files')
    parser.add_argument('--monitor', default=[], nargs='+', help='...')
    parser.add_argument('--upload', type=str, help='File to upload')
    parser.add_argument('--download', type=str, nargs='+', help='File to download')
    parser.add_argument('--execute', type=str, nargs='+', help='File to download')
    parser.add_argument('--save', action='store_true', help='Save the running state')
    parser.add_argument('--restore', action='store_true', help='Restore previous state')
    parser.add_argument('--run', action='store_true', help='Run the virtual machine')
    parser.add_argument('--swap', type=str, help='Change the current process for the given one')
    parser.add_argument('--breakon', type=str, nargs='+', help='Change the current process for the given one')

    args = parser.parse_args()
    helper = Helper(args.vm, FDP)
    Process = args.process

    if args.save: 
        helper.logger.info('Saving %s' % args.vm)
        helper.dbg.Save()
        helper.dbg.Resume()
        helper.logger.info('Success')
        exit(0)

    elif args.restore: 
        helper.logger.info('Restoring %s' % args.vm)
        helper.dbg.Restore()
        helper.dbg.Resume()
        helper.logger.info('Success')

    if args.swap:
        ActiveProcess = helper.SwapContext(args.swap)
        print(ActiveProcess)
        exit(0)

    if args.upload:
        Status = Automation.Upload(helper, args.upload)

        if Status: 
            helper.logger.info('Upload %s successeeded' % args.upload)
            Process = os.path.basename(args.upload)
            print(Process)
        else: 
            helper.logger.info('Upload %s failed' % args.upload)
            exit(0)

        helper.UnsetAllBreakpoints()
        helper.dbg.Resume()

    if args.download:
        Automation.__download__(helper, args.download, output=args.output)
        helper.dbg.Resume()
        exit(0)

    if args.run:
        helper.UnsetAllBreakpoints()
        helper.dbg.Resume()
        exit(0)

    if args.entrypoint: 
        PsWaitForSingleProcessAsync(helper, Process)
        helper.Run()
        
        Process = helper.PsGetCurrentProcess()
        print(Process)

    ProcessTracker(helper, Process=Process, Output=args.output, Monitors=args.monitor, BreakOnActions=args.breakon)
    helper.Run()
