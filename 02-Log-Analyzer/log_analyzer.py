import re
from collections import Counter
from pathlib import Path
from datetime import datetime


def read_log_file(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"\nERROR: File not found: {file_path}")
        return []

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as file:
            return file.readlines()
    except Exception as error:
        print(f"\nERROR reading file: {error}")
        return []


def analyze_logs(lines):
    total_lines = len(lines)

    error_lines = []
    warning_lines = []
    info_lines = []

    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ips = []

    for line in lines:
        upper_line = line.upper()

        if "ERROR" in upper_line:
            error_lines.append(line.strip())

        elif "WARNING" in upper_line or "WARN" in upper_line:
            warning_lines.append(line.strip())

        elif "INFO" in upper_line:
            info_lines.append(line.strip())

        found_ips = re.findall(ip_pattern, line)
        ips.extend(found_ips)

    ip_counter = Counter(ips)

    return {
        "total_lines": total_lines,
        "errors": error_lines,
        "warnings": warning_lines,
        "info": info_lines,
        "ips": ip_counter
    }


def show_summary(results):
    print("\n" + "=" * 65)
    print("              AVINASH PYTHON LOG ANALYZER")
    print("=" * 65)

    print(f"\nTotal Log Entries : {results['total_lines']}")
    print(f"Errors            : {len(results['errors'])}")
    print(f"Warnings          : {len(results['warnings'])}")
    print(f"Info Messages     : {len(results['info'])}")

    print("\n--- TOP IP ADDRESSES ---")

    if results["ips"]:
        for ip, count in results["ips"].most_common(10):
            print(f"{ip:<20} {count} occurrence(s)")
    else:
        print("No IP addresses found.")

    print("\n--- SAMPLE ERRORS ---")

    if results["errors"]:
        for error in results["errors"][:5]:
            print(error)
    else:
        print("No errors found.")

    print("\n--- SAMPLE WARNINGS ---")

    if results["warnings"]:
        for warning in results["warnings"][:5]:
            print(warning)
    else:
        print("No warnings found.")


def generate_report(results):
    report_name = "log_analysis_report.txt"

    with open(report_name, "w", encoding="utf-8") as report:
        report.write("=" * 65 + "\n")
        report.write("AVINASH PYTHON LOG ANALYZER REPORT\n")
        report.write("=" * 65 + "\n")

        report.write(f"Generated: {datetime.now()}\n\n")

        report.write(f"Total Log Entries : {results['total_lines']}\n")
        report.write(f"Errors            : {len(results['errors'])}\n")
        report.write(f"Warnings          : {len(results['warnings'])}\n")
        report.write(f"Info Messages     : {len(results['info'])}\n")

        report.write("\nTOP IP ADDRESSES\n")
        report.write("-" * 30 + "\n")

        for ip, count in results["ips"].most_common(10):
            report.write(f"{ip}: {count}\n")

        report.write("\nERROR DETAILS\n")
        report.write("-" * 30 + "\n")

        for error in results["errors"]:
            report.write(error + "\n")

        report.write("\nWARNING DETAILS\n")
        report.write("-" * 30 + "\n")

        for warning in results["warnings"]:
            report.write(warning + "\n")

    print(f"\nReport generated successfully: {report_name}")


def main():
    print("=" * 65)
    print("              AVINASH PYTHON LOG ANALYZER")
    print("=" * 65)

    file_path = input("\nEnter log file path: ").strip('"')

    lines = read_log_file(file_path)

    if not lines:
        return

    results = analyze_logs(lines)

    show_summary(results)

    generate_report(results)


if __name__ == "__main__":
    main()