#Python program to reduce VRAM usage when running MSFS with multiple external applications, by forcing applications to use the iGPU instead of the dGPU.
#This is done by disabling the dGPU, launching all external MSFS applications, and then re-enabling the dGPU.
import subprocess
import time
import ctypes, sys

#UAC elevation
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    print("Admin rights not detected, program may run incorrectly")

#DGPU_pnpID = r"PCI\VEN_10DE&DEV_2206&SUBSYS_38853842&REV_A1\4&1B844C37&0&0008" #3080
#DGPU_pnpID = r"PCI\VEN_10DE&DEV_24A0&SUBSYS_13201462&REV_A1\4&19F98689&0&0008" #3070ti


def loadGPU_pnpID():
    with open("pnpID.txt", "r") as file:
        DGPU_pnpID = file.read().strip()
    return DGPU_pnpID
DGPU_pnpID = loadGPU_pnpID()

def loadApplications():
    with open("applicationList.txt", "r") as file:
        applicationList = file.readlines()
    return applicationList
applicationList = loadApplications()

def launchApplications(applicationList):
    for application in applicationList:
        subprocess.Popen(application)

def main():
    subprocess.run([r"C:\Windows\System32\pnputil.exe", "/disable-device", DGPU_pnpID])
    launchApplications(applicationList)
    time.sleep(2)
    subprocess.run([r"C:\Windows\System32\pnputil.exe", "/enable-device", DGPU_pnpID])
    print("Apps launched on iGPU, ready to launch sim")


gpuList = subprocess.check_output(['wmic', 'PATH', 'Win32_VideoController', 'GET', 'Description,PNPDeviceID']).decode('utf-8').strip().split('\n')
print(gpuList[1])
print(gpuList[2])

