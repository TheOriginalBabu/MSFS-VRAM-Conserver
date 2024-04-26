#Python program to reduce VRAM usage when running MSFS with multiple external applications
import subprocess
import time
import ctypes, sys

if ctypes.windll.shell32.IsUserAnAdmin() == 0:  #if not an admin, run as admin
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

print("Hello World!")

# Define the command with the correct path and arguments
disablecommand = [
    r"C:\Windows\System32\pnputil.exe",
    "/disable-device",
    r"PCI\VEN_10DE&DEV_2206&SUBSYS_38853842&REV_A1\4&1B844C37&0&0008"
]
enablecommand = [
    r"C:\Windows\System32\pnputil.exe",
    "/enable-device",
    r"PCI\VEN_10DE&DEV_2206&SUBSYS_38853842&REV_A1\4&1B844C37&0&0008"
]

def flushDGPU():
    subprocess.run(disablecommand)
    time.sleep(4)
    subprocess.run(enablecommand)
    time.sleep(4)

#flushDGPU()
print(disablecommand)
print(enablecommand)

