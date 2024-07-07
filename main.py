import subprocess
import time
import ctypes
import sys

# UAC elevation prompt
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    print("Admin rights not detected, program may run incorrectly")

# Read configuration file
config = {}
with open("config.txt", "r") as file:
    for line in file:
        key, value = line.strip().split(' = ')
        config[key] = value

DGPU_pnpID = config.get("DGPU_pnpID")
print("PNPID = ", DGPU_pnpID)

delayFactor = float(config.get("delayFactor", 1))  # Default delayFactor to 1 if not found
print("Delay Factor = ", delayFactor)

# Read application list
with open("applicationList.txt", "r") as file:
    applicationList = [line.strip() for line in file.readlines()]
    applicationCount = len(applicationList)

print("Application List: ", applicationList)
print("Application Count: ", applicationCount)

# --- Main program below ---#

# subprocess.run([r"C:\Windows\System32\pnputil.exe", "/disable-device", DGPU_pnpID])
for index, application in enumerate(applicationList, start=1):
    print(f"Launching [{index}/{applicationCount}]: {application}")
    try:
        application_path = f'"{application}"' if ' ' in application else application  # Use raw string literal for paths and ensure paths with spaces are quoted
        subprocess.Popen(application_path, shell=True)
    except FileNotFoundError:
        print(f"Error: File not found for application: {application}")
    except Exception as e:
        print(f"Error launching {application}: {e}")

time.sleep(applicationCount * delayFactor)
# subprocess.run([r"C:\Windows\System32\pnputil.exe", "/enable-device", DGPU_pnpID])

# gpuList = subprocess.check_output(['wmic', 'PATH', 'Win32_VideoController', 'GET', 'Description,PNPDeviceID']).decode('utf-8').strip().split('\n')
# print(gpuList[1])
# print(gpuList[2])
