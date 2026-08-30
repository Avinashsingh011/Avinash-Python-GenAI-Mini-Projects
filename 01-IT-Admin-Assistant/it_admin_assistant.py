import os
import platform
import socket
import subprocess
import shutil
import datetime


def show_header():
    print("=" * 60)
    print("        AVINASH PYTHON IT ADMIN ASSISTANT")
    print("=" * 60)
    print(f"Date & Time : {datetime.datetime.now()}")
    print()


def system_information():
    print("\n--- SYSTEM INFORMATION ---")

    print(f"Computer Name : {socket.gethostname()}")
    print(f"Operating System : {platform.system()}")
    print(f"OS Version : {platform.version()}")
    print(f"OS Release : {platform.release()}")
    print(f"Architecture : {platform.machine()}")
    print(f"Processor : {platform.processor()}")
    print(f"Python Version : {platform.python_version()}")


def network_information():
    print("\n--- NETWORK INFORMATION ---")

    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)

        print(f"Hostname : {hostname}")
        print(f"Local IP : {ip_address}")

    except socket.error as error:
        print(f"Unable to retrieve IP address: {error}")


def ping_host():
    print("\n--- PING TEST ---")

    host = input("Enter hostname or IP address: ")

    parameter = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", parameter, "4", host]

    try:
        subprocess.run(command)

    except Exception as error:
        print(f"Ping failed: {error}")


def dns_lookup():
    print("\n--- DNS LOOKUP ---")

    domain = input("Enter domain name (example google.com): ")

    try:
        ip_address = socket.gethostbyname(domain)

        print(f"{domain} resolves to {ip_address}")

    except socket.gaierror:
        print("DNS lookup failed.")


def disk_usage():
    print("\n--- DISK USAGE ---")

    total, used, free = shutil.disk_usage("C:\\")

    gb = 1024 ** 3

    print(f"Total Disk : {total / gb:.2f} GB")
    print(f"Used Disk  : {used / gb:.2f} GB")
    print(f"Free Disk  : {free / gb:.2f} GB")

    usage_percent = (used / total) * 100

    print(f"Disk Usage : {usage_percent:.2f}%")

    if usage_percent > 90:
        print("WARNING: Disk utilization is critical!")

    elif usage_percent > 75:
        print("WARNING: Disk utilization is high.")

    else:
        print("Disk utilization is healthy.")


def running_processes():
    print("\n--- RUNNING PROCESSES ---")

    if platform.system().lower() == "windows":

        subprocess.run(["tasklist"])

    else:

        subprocess.run(["ps", "aux"])


def ip_configuration():
    print("\n--- FULL IP CONFIGURATION ---")

    if platform.system().lower() == "windows":

        subprocess.run(["ipconfig", "/all"])

    else:

        subprocess.run(["ip", "addr"])


def main():

    while True:

        show_header()

        print("""
1. System Information
2. Network Information
3. Ping Host
4. DNS Lookup
5. Disk Usage
6. Running Processes
7. Full IP Configuration
8. Exit
""")

        choice = input("Select option [1-8]: ")

        if choice == "1":
            system_information()

        elif choice == "2":
            network_information()

        elif choice == "3":
            ping_host()

        elif choice == "4":
            dns_lookup()

        elif choice == "5":
            disk_usage()

        elif choice == "6":
            running_processes()

        elif choice == "7":
            ip_configuration()

        elif choice == "8":
            print("\nThank you for using Avinash IT Admin Assistant.")
            break

        else:
            print("\nInvalid option. Please select 1-8.")

        input("\nPress Enter to continue...")

        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main()