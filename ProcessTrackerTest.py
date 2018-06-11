from Sandbagility import Helper
from Sandbagility.Core import FDP

import argparse

from Sandbagility.Plugins import ProcessTracker

import os
from Sandbagility.Plugins import Automation
from Sandbagility.Plugins import HyperWin32Api as HyperApi

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Trace a process activity, including its childs .')
    parser.add_argument('--process', type=str, default='explorer.exe', help='Process name to trace')
    parser.add_argument('--vm', default="Windows 10 x64 - 14393", help='Virtual Machine name')
    parser.add_argument('--output', default='D:\\Jail\\DroppedFiles\\', help='Output directory for dumped files')
    parser.add_argument('--monitor', default=[], nargs='+', help='...')
    parser.add_argument('--upload', type=argparse.FileType('rb'), help='File to upload')
    parser.add_argument('--save', action='store_true', help='Save the running state')
    parser.add_argument('--restore', action='store_true', help='Restore previous state')
    parser.add_argument('--run', action='store_true', help='Run the virtual machine')

    args = parser.parse_args()

    helper = Helper(args.vm, FDP)

    if args.save: 
        helper.logger.info('Saving %s' % args.vm)
        helper.dbg.Save()
        helper.dbg.Resume()
        helper.logger.info('Success')
    elif args.restore: 
        helper.logger.info('Restoring %s' % args.vm)
        helper.dbg.Restore()
        helper.dbg.Resume()
        helper.logger.info('Success')
        
    if args.run:
        helper.dbg.Resume()
        exit(0)

    if args.upload:
        RemoteFilename = Automation.Upload(helper, args.upload)
        if RemoteFilename: 
            helper.logger.info('Upload %s successeeded' % args.upload.name)
        else: 
            helper.logger.info('Upload %s failed' % args.upload.name)

    ProcessTracker(helper, Process=args.process, Output=args.output, Monitors=args.monitor)
    helper.Run()
