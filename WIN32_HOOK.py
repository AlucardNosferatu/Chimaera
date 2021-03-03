import ctypes as c
import win32con as wcon
import time
from ctypes import wintypes as w
import win32process as wproc


class MODULEINFO(c.Structure):
    _fields_ = [
        ("lpBaseOfDll", c.c_void_p),
        ("SizeOfImage", w.DWORD),
        ("EntryPoint", c.c_void_p),
    ]


pid = 268  # Minesweeper

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

get_module_information_func_name = "GetModuleInformation"
GetModuleInformation = getattr(c.WinDLL("kernel32"), get_module_information_func_name, getattr(c.WinDLL("psapi"), get_module_information_func_name))
GetModuleInformation.argtypes = [w.HANDLE, w.HMODULE, c.POINTER(MODULEINFO), w.DWORD]
GetModuleInformation.restype = w.BOOL

processHandle = OpenProcess(wcon.PROCESS_ALL_ACCESS, False, pid)
module_info = MODULEINFO()
module_handles = wproc.EnumProcessModules(processHandle)
for i in range(len(module_handles)):
    module_handle = module_handles[i]
    res = GetModuleInformation(processHandle, module_handle, c.byref(module_info), c.sizeof(module_info))
    module_file_name = wproc.GetModuleFileNameEx(processHandle, module_handle)
    print("ModuleName: {}".format(module_file_name))
    print("EntryPoint: {}".format(module_info.EntryPoint))
    print("SizeOfImage: {}".format(module_info.SizeOfImage))
    print("lpBaseOfDll: {}".format(module_info.lpBaseOfDll))
    print()
addr = 0x00000253F2653CB0  # Minesweeper.exe module base address
data = c.c_char()
bytesRead = c.c_ulonglong()
while True:
    result = ReadProcessMemory(processHandle, addr, c.byref(data), c.sizeof(data), c.byref(bytesRead))
    e = GetLastError()
    print('result: {}, err code: {}, bytesRead: {}'.format(result, e, bytesRead.value))
    print('data: {}'.format(data.value.decode()))
    time.sleep(1)
