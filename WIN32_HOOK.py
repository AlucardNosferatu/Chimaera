import ctypes as c
import time
from ctypes import wintypes as w

pid = 16996  # Minesweeper

k32 = c.windll.kernel32

OpenProcess = k32.OpenProcess
OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
OpenProcess.restype = w.HANDLE

ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = [w.HANDLE, w.LPCVOID, w.LPVOID, c.c_size_t, c.POINTER(c.c_size_t)]
ReadProcessMemory.restype = w.BOOL

GetLastError = k32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = w.DWORD

CloseHandle = k32.CloseHandle
CloseHandle.argtypes = [w.HANDLE]
CloseHandle.restype = w.BOOL

processHandle = OpenProcess(0x10, False, pid)

addr = 0x000002BD2583D090  # Minesweeper.exe module base address
data = c.c_char()
bytesRead = c.c_ulonglong()
while True:
    result = ReadProcessMemory(processHandle, addr, c.byref(data), c.sizeof(data), c.byref(bytesRead))
    e = GetLastError()
    print('result: {}, err code: {}, bytesRead: {}'.format(result, e, bytesRead.value))
    print('data: {}'.format(data.value.decode()))
    time.sleep(1)
