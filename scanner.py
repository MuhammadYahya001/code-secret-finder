import re

# Secret patterns
patterns = {
    "GitHub Token": r"github_pat_[A-Za-z0-9_]{20,}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "JWT Token": r"eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+",
    "Generic API Key": r"(?i)(api_key|apikey|secret|token)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}[\"']?"
}

def scan_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        findings = []

        for secret_type, pattern in patterns.items():
            matches = re.findall(pattern, content)
            for match in matches:
                findings.append((secret_type, match))

        if findings:
            print(f"\n[!] Secrets found in {filename}:\n")
            for secret_type, match in findings:
                print(f"Type: {secret_type}")
                print(f"Match: {match}")
                print("-" * 40)
        else:
            print(f"\n[+] No secrets found in {filename}")

    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")

if __name__ == "__main__":
    filename = input("Enter file name to scan: ")
    scan_file(filename)
