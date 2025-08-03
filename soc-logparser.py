#!/usr/bin/env python
"""
SOC-PythonLogParser
Author: Grigorios Christopoulos
Description:
    This script is for demonstration purposes.
    The script parses Linux auth.log(var/log/auth.log) and Apache HTTP Server access.log(complete mpath) files to detect
    possible SSH and HTTP brute force attacks. It counts failed and successfullogin attempts and outputs a summary of findings. 
    Runs both on Linux and Windows.
Date: 01-08-2025
Requirements:
    - pyfiglet (pip install pyfiglet)
"""

import pyfiglet, os

def clean_path_to_file(path):
    path = path.strip().strip('"').strip("'")
    path = path.replace("\\ ", " ")
    return os.path.expanduser(path)

def parse_auth_log(file):
    if not file.lower().endswith(".log"):
        print("[ERROR] Invalid file type for SSH logs. Please provide a '.log' file.")
        return 0
    try:
        with open(file, encoding='utf-8', errors='ignore') as i:
            lines_list = i.readlines()                
            
        # Look for repeated "Failed password" logins.
        failed_attempts = [line for line in lines_list if "Failed password" in line]
        success_attempts = [line for line in lines_list if "Accepted password" in line]

        if len(failed_attempts) > 3:
            if len(success_attempts) >= 1:
                print(f"[!] Possible SSH brute force detected and was potentially successful: {len(failed_attempts)} failed attempts and {len(success_attempts)} succeeded.")
                return 1
            else:
                print(f"[!] Possible SSH brute force attempt detected: {len(failed_attempts)} failed attempts and NO successes.")
        else:
            print("[✓] No SSH brute force detected.")
    except :
        print("[ERROR!]")
        return 0

def parse_apache_log(file):
    if not file.lower().endswith(".log"):
        print("[ERROR] Invalid file type for HTTP/Apache logs. Please provide a '.log' file.")
        return 0
    try:
        with open(file, encoding='utf-8', errors='ignore') as i:
            lines_list = i.readlines()
        
        # Look for repeated "401" Unauthorized. 401 means unauthorized and 200 means OK -> sucessful response.
        failed_logins = [line for line in lines_list if "401" in line]
        success_logins = [line for line in lines_list if "200" in line]

        if len(failed_logins) > 3:
            if len(success_logins) >= 1:
                print(f"[!] Possible HTTP brute force and was potentially successful: {len(failed_logins)} failed and {len(success_logins)} succeeded.")
                return 1
            else:
                print(f"[!] Possible HTTP brute force attempt detected: {len(failed_logins)} failed, NO successes.")
        else:
            print("[✓] No HTTP brute force detected.")
    except:
        print("[ERROR!]")
        return 0
    

def main():

    ASCII_art_1 = pyfiglet.figlet_format("SOC-PythonLogParser")
    print(ASCII_art_1)
    print("Made by Grigorios Christopoulos")

    auth_compromise_indicator = 0
    apache_compromise_indicator = 0
    total_indicator = 0

    auth_log_file = clean_path_to_file(input("\nDrag and drop the auth.log file here: "))
    apache_log_file = clean_path_to_file(input("Drag and drop the access.log file here: "))
    
    print("\nParsing SSH auth logs...")
    if parse_auth_log(auth_log_file) == 1:
        total_indicator += 1
        auth_compromise_indicator +=1

    print("\nParsing Apache logs...")
    if parse_apache_log(apache_log_file) == 1:
        total_indicator += 1
        apache_compromise_indicator += 1

    if total_indicator == 0:
        print("\n --- Parser didn't detect any anomalies. ---")
    elif total_indicator == 1:
        if auth_compromise_indicator == 1:
            print("\n --- Parser detected a possible SSH Brute force attack! ---\n --- But it did not detect any evidence of HTTP Brute force attacks. ---")
        else:
            print("\n --- Parser detected a possible HTTP Brute force attack! ---\n --- But it did not detect any evidence of SSH Brute force attacks. ---")
    elif total_indicator == 2:
        print("\n\n --- Parser detected that the system is possibly compromised through both SSH and HTTP Brute force attacks! ---")
    else:
        print ("")
    print("\nFinished\n")
    input("\nEnter to exit...")
    
if __name__ == "__main__":
    main()
