#!/bin/bash

DOMAIN="${DOMAIN:-}"  # optional override
if [ -z "$DOMAIN" ]; then
  read -p "Enter target domain (e.g. example.com): " DOMAIN
fi

export SHODAN_API_KEY=${SHODAN_API_KEY:-your_shodan_api_key_here}
export GITHUB_TOKEN=${GITHUB_TOKEN:-your_github_token_here}

echo "[+] Starting OSINT Pivot Tool on: $DOMAIN"
python3 osint_pivot_tool.py <<< "$DOMAIN"
echo "[✔] OSINT pivot complete. Results saved in osint_results_*.zip"
