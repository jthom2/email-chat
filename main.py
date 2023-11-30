import time
from colorama import Fore, Style
import os
import platform
import sys


for i in range(5):
    time.sleep(0.3
    print(f"""{Fore.RED}You get 500 error codes onna daily\n""")

def shutdown_computer():
    operating_system = platform.system()

    if operating_system == "Windows":
        os.system("shutdown /s /t 1")
    elif operating_system == "Darwin":
        os.system("sudo shutdown -h now")
    elif operating_system == "Linux":
        os.system("sudo shutdown -h now")
    else:
        print("Unsupported operating system.")
        sys.exit(1)

time.sleep(3)
shutdown_computer()
