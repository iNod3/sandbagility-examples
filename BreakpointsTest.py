from Sandbagility import Helper
from Sandbagility.Core import FDP

from Sandbagility.Monitor import KernelGenericMonitor

VM_NAME = "Windows 10 x64 - 14393"

class BreakMe(KernelGenericMonitor):

    _NAME = 'BreakMe'
    _DEPENDENCIES = ['ntoskrnl.exe']

    def __install__(self):

        self.SetHardwareBreakpoint('nt!NtWriteFile', 0)
        return True

    def __post__(self, m):

        Process = m.LastOperation.Process
        Detail = m.LastOperation.Detail

        Data = self.helper.ReadVirtualMemory(Detail.Buffer, Detail.Length)
        
        if Data[:2] == b'MZ':
            print('Handle: %x, Buffer: %#.16x, Length: %#.8x, Filename: %s' %
                    (
                      Detail.FileHandle, 
                      Detail.Buffer, 
                      Detail.Length, 
                      Process.ObReferenceObjectByHandle(Detail.FileHandle)
                    )
                )
            print('Data: %s' % Data[:0x10].hex())
            print(Process)
        
        return True

if __name__ == '__main__':

    ''' log any attempt to write a buffer
        beginning with 'MZ' into a handle
        from any process
    '''
    helper = Helper(VM_NAME, FDP)

    BreakMe(helper)

    helper.Run()
