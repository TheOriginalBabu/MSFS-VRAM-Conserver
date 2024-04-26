#Python program to reduce VRAM usage when running MSFS with multiple external applications, by forcing applications to use the iGPU instead of the dGPU.
#This is done by disabling the dedicated GPU, launching all external MSFS applications, and then re-enabling the dGPU.
#Because the dedicated GPU is disabled, the applications will not see the dedicated GPU, thus the only option is to use the iGPU.
import subprocess
import time
import ctypes, sys

#UAC elevation
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

#if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    #print("Please run this script as an administrator")
    #print("Input anything to exit")
    #input()
    #sys.exit()

print("MSFS VRAM conserver by Babu")

DGPU_pnpID = r"PCI\VEN_10DE&DEV_2206&SUBSYS_38853842&REV_A1\4&1B844C37&0&0008" #3080
#DGPU_pnpID = r"PCI\VEN_10DE&DEV_24A0&SUBSYS_13201462&REV_A1\4&19F98689&0&0008" #3070ti

#load application list from applicationList.txt
applicationList = []
with open("applicationList.txt", "r") as file:
    for line in file:
        applicationList.append(line.strip())
print(applicationList)

def launchApplications(applicationList):
    for application in applicationList:
        subprocess.Popen(application)

#subprocess.run([r"C:\Windows\System32\pnputil.exe", "/disable-device", DGPU_pnpID])
launchApplications(applicationList)
#time.sleep(2)
#subprocess.run([r"C:\Windows\System32\pnputil.exe", "/enable-device", DGPU_pnpID])
