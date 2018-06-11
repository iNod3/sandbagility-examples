from Sandbagility import Helper
from Sandbagility.Core import FDP

from Sandbagility.Plugins import HyperWin32Api as HyperApi

VM_NAME = "Windows 10 x64 - 14393"

if __name__ == '__main__':

    helper = Helper(VM_NAME, FDP, debug=['HyperApi'])

    helper.SwapContext('winlogon.exe', Userland=True)
    ActiveProcess = helper.PsGetCurrentProcess(loadLdr=True)
    print(ActiveProcess)

    api = HyperApi(helper)

    api.AcquireContext(ActiveProcess)

    hFile = api.CreateFile(b'C:\\Users\\User\\Desktop\\test.bat')
    helper.logger.info('CreateFile: %x', hFile)

    Status = api.WriteFile(hFile, b'c:\\windows\\syswow64\\cmd.exe')
    helper.logger.info('WriteFile: %x', Status)

    Status = api.CloseHandle(hFile)
    helper.logger.info('CloseHandle: %x', Status)

    Status = api.WinExec(b'C:\\Users\\User\\Desktop\\test.bat')
    helper.logger.info('WinExec: %x', Status)

    api.ReleaseContext()