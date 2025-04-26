import argparse
import re
import sys
from collections import defaultdict
from typing import List, Dict

def analyze_logs(log_files: List[str], report_type: str) -> int:
    
    request_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    total_requests: int = 0

    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                for line in f: 
                    if "django.request" in line:
                        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (?P<level>\w+) django\.request: (?P<method>\w+) (?P<url>[^ ]+)', line)
                        if match:
                            level: str = match.group('level')
                            url: str = match.group('url')
                            request_counts[url][level] += 1
                            total_requests += 1

        except FileNotFoundError:
            print(f"Error: Log file not found: {log_file}", file=sys.stderr)
            return 1

    if report_type == 'handlers':
        generate_handlers_report(request_counts, total_requests)
    else:
        print(f"Error: Unknown report type: {report_type}", file=sys.stderr)
        return 1
    return 0


def generate_report(request_counts: Dict[str, Dict[str, int]], total_requests: int) -> None:

    print(f"Total requests: {total_requests}\n")

    handlers: List[str] = sorted(request_counts.keys())
    levels: List[str] = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    header: str = "HANDLER               \t" + "\t".join(levels) + "\t"
    print(header)

    total_by_level: Dict[str, int] = {level: 0 for level in levels}
    for handler in handlers:
        row: str = f"{handler}               \t"
        for level in levels:
            count: int = request_counts[handler][level]
            row += f"{count:<8}\t"
            total_by_level[level] += count
        print(row)

    total_row: str = "                        \t"
    for level in levels:
        total_row += f"{total_by_level[level]:<8}\t"
    print(total_row)


def main() -> int:
    parser = argparse.ArgumentParser(description='Analyze Django logs and generate reports.')
    parser.add_argument('log_files', nargs='+', help='Path to log files')
    parser.add_argument('--report', required=True, choices=['handlers'], help='Report to generate')

    args = parser.parse_args()

    return analyze_logs(args.log_files, args.report)


if __name__ == "__main__":
    sys.exit(main())
