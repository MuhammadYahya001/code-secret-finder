# code-secret-finder

A simple Python-based cybersecurity tool that scans files for accidentally exposed secrets such as API keys, AWS access keys, GitHub tokens, and JWTs.

## Why this project matters
Leaked secrets in source code are a common security issue and can lead to unauthorized access, account compromise, and cloud abuse.

## Features
- Scan single files or entire folders
- Rich colored output for readability
- Export scan results to JSON
- Supports `.txt`, `.py`, `.env` files
- Detects GitHub tokens
- Detects AWS Access Keys
- Detects JWT tokens
- Detects generic API keys / secrets

## Technologies Used
- Python
- Regex

## How to Run

```bash
python scanner.py
pip install rich
