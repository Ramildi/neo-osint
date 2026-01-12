#!/usr/bin/env python3
import os
from colorama import Fore, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + """
 ███╗   ██╗███████╗ ██████╗      ██████╗ ███████╗██╗███╗   ██╗████████╗
 ████╗  ██║██╔════╝██╔═══██╗    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
 ██╔██╗ ██║█████╗  ██║   ██║    ██║   ██║███████╗██║██╔██╗ ██║   ██║   
 ██║╚██╗██║██╔══╝  ██║   ██║    ██║   ██║╚════██║██║██║╚██╗██║   ██║   
 ██║ ╚████║███████╗╚██████╔╝    ╚██████╔╝███████║██║██║ ╚████║   ██║   
 ╚═╝  ╚═══╝╚══════╝ ╚═════╝      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
""")

while True:
    banner()
    print(Fore.GREEN + """
[1] Smart Username OSINT
[2] Metadata Extractor
[3] Email OSINT Analyzer
[4] Phone OSINT (Passive)
[0] Exit
""")

    choice = input("Select → ").strip()

    if choice == "1":
        os.system("python3 tools/smart_username/smart_username.py")
    elif choice == "2":
        path = input("File Path → ")
        os.system(f"python3 tools/metadata_extractor/metadata_extractor.py '{path}'")
    elif choice == "3":
        os.system("python3 tools/email_osint/email_osint.py")
    elif choice == "4":
        os.system("python3 tools/phone_osint/phone_osint.py")
    elif choice == "0":
        break
    else:
        print("WRONG!!!!")
