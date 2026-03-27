import re
import os
import json
from rich.console import Console
from rich.table import Table

console = Console()

# Patterns to detect secrets
patterns = {
    "GitHub Token": r"github_pat_[A-Za-z0-9_]{20,}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "JWT Token": r"eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+",
    "Generic API Key": r"(?i)(api_key|apikey|secret|token)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}[\"']?"
}

def scan_file(filename):
    """Scan a single file for secrets."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        findings = []

        for secret_type, pattern in patterns.items():
            matches = re.findall(pattern, content)
            for match in matches:
                findings.append({"file": filename, "type": secret_type, "match": match})

        return findings

    except FileNotFoundError:
        console.print(f"[red][!] File '{filename}' not found.[/red]")
        return []

def scan_folder(folder_path):
    """Scan all files in a folder."""
    all_findings = []
    for root, _, files in os.walk(folder_path):
        for f in files:
            if f.endswith((".txt", ".py", ".env")):  # scan only relevant files
                filepath = os.path.join(root, f)
                findings = scan_file(filepath)
                all_findings.extend(findings)
    return all_findings

def print_findings(findings):
    """Print findings in a rich table."""
    if findings:
        table = Table(title="Secrets Found", show_lines=True)
        table.add_column("File")
        table.add_column("Secret Type")
        table.add_column("Value")
        for item in findings:
            table.add_row(item["file"], item["type"], item["match"])
        console.print(table)
    else:
        console.print("[green][+] No secrets found.[/green]")

def export_to_json(findings, filename="scan_results.json"):
    """Export findings to a JSON file."""
    if findings:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(findings, f, indent=4)
        console.print(f"[blue][i]Results exported to {filename}[/i][/blue]")

if __name__ == "__main__":
    console.print("[bold yellow]Welcome to Code Secret Finder![/bold yellow]")
    choice = console.input("Scan [f]ile or [d]irectory? (f/d): ").strip().lower()

    findings = []
    if choice == "f":
        filename = console.input("Enter file name to scan: ").strip()
        findings = scan_file(filename)
    elif choice == "d":
        folder = console.input("Enter folder path to scan: ").strip()
        findings = scan_folder(folder)
    else:
        console.print("[red]Invalid choice! Exiting.[/red]")

    print_findings(findings)
    export = console.input("Export results to JSON? (y/n): ").strip().lower()
    if export == "y":
        export_to_json(findings)
