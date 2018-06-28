from Sandbagility import Helper
from Sandbagility.Core import FDP

from Sandbagility.Plugins import PsWaitForSingleProcessAsync
from Sandbagility.Monitors import VirtualMemoryMonitor, DynamicCodeMonitor, SyscallMonitor

import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Trace a process activity, including its childs .')
    parser.add_argument(
        '--vm', default="Windows 10 x64 - 14393", help='Virtual Machine name')
    parser.add_argument(
        'process', help='Process name to unpack'
    )

    args = parser.parse_args(['upx.exe'])

    helper = Helper(args.vm, FDP, debug=[''])

    PsWaitForSingleProcessAsync(helper, args.process, Entrypoint=False)
    helper.Run()

    ActiveProcess = helper.PsGetCurrentProcess()
    print(ActiveProcess)
    print('%x' % ActiveProcess.ImageBaseAddress)

    # address = 0xfffff801a2e60c34
    # symbol = helper.symbol.LookupByAddr(address)
    # print('%x: %s' % (address, symbol))

    # symbol = 'nt!NtOpenProcess'
    # address = helper.SymLookupByName(symbol)
    # print('%x: %s' % (address, symbol))

    def h(m):

        if m.LastOperation.Action in ['NtProtectVirtualMemory', 'NtAllocateVirtualMemory']:
            if ActiveProcess.ImageBaseAddress < m.LastOperation.Detail.BaseAddress < ( ActiveProcess.ImageBaseAddress + helper.MoGetImageSize(ActiveProcess.ImageBaseAddress)):
                print('%x' % m.LastOperation.Detail.BaseAddress)

    m = SyscallMonitor(helper, ActiveProcess, verbose=False)
    m.RegisterPostCallback(h)

    # m.RegisterPostCallback(lambda x: not x.LastOperation.Action == 'NtTerminateProcess')

    # print('%x' % helper.MoGetEntryPoint(ActiveProcess.ImageBaseAddress))
    # Entrypoint = helper.MoGetEntryPoint(ActiveProcess.ImageBaseAddress)
    # print(helper.SetHardwareBreakpoint(Entrypoint, 'e', lambda: print('alzej'), dr=0, cr3=ActiveProcess.DirectoryTableBase))

    # VirtualMemoryMonitor(helper, Process=ActiveProcess, verbose=True)
    # DynamicCodeMonitor(helper, Process=ActiveProcess, verbose=True)

    # print(helper.PsGetCurrentProcess())

    helper.Run()
