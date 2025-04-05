# osint_pivot_tool.py - Hail Mary OSINT Pivot Script

import os
import subprocess
import requests
import json
from datetime import datetime

# === USER INPUT ===
DOMAIN = input("Enter target domain (e.g. example.com): ").strip()
OUTPUT_DIR = f"osint_results_{DOMAIN}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
SHODAN_API_KEY = "your_shodan_api_key_here"  # Replace with your actual key
GITHUB_TOKEN = "your_github_token_here"      # Replace with your GitHub token
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"[+] Saving results to {OUTPUT_DIR}\n")

# === 1. Wayback Machine JavaScript ===
print("[1] Fetching JavaScript URLs from Wayback Machine...")
with open(f"{OUTPUT_DIR}/wayback_js.txt", "w") as f:
    subprocess.call(f"waybackurls {DOMAIN} | grep '.js'", shell=True, stdout=f)

# === 2. GitHub Code Search via API ===
print("[2] Searching GitHub for secrets via API...")
github_headers = {"Authorization": f"token {GITHUB_TOKEN}"}
github_dorks = [
    f"filename:.env {DOMAIN}",
    f"filename:config.json {DOMAIN}",
    f"filename:.sh {DOMAIN}",
    f"filename:.yml {DOMAIN}",
    f"{DOMAIN} AWS_ACCESS_KEY_ID"
]

github_results = []
for dork in github_dorks:
    url = f"https://api.github.com/search/code?q={dork.replace(' ', '+')}"
    r = requests.get(url, headers=github_headers)
    if r.status_code == 200:
        for item in r.json().get("items", []):
            github_results.append(f"{item['html_url']} in {item['repository']['full_name']} [HIGH]")

with open(f"{OUTPUT_DIR}/github_api_results.txt", "w") as f:
    f.write("\n".join(github_results))

# === 3. crt.sh Certificate Search ===
print("[3] Gathering certificate data from crt.sh...")
crtsh_url = f"https://crt.sh/?q=%25.{DOMAIN}&output=json"
with open(f"{OUTPUT_DIR}/crtsh_query.txt", "w") as f:
    f.write(crtsh_url + "\n")

# === 4. Archive Bucket Discovery ===
print("[4] Checking archived URLs for cloud buckets...")
with open(f"{OUTPUT_DIR}/bucket_keywords.txt", "w") as f:
    subprocess.call(f"waybackurls {DOMAIN} | grep -Ei 's3|blob|objectstorage'", shell=True, stdout=f)

# === 5. Shodan API Query ===
print("[5] Querying Shodan API...")
shodan_results = []
for query in [f"ssl:{DOMAIN}", f"hostname:{DOMAIN}"]:
    url = f"https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query={query}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        for match in data.get("matches", []):
            host_entry = f"{match.get('ip_str')} - {match.get('hostnames')} - {match.get('org')} [MEDIUM]"
            shodan_results.append(host_entry)

with open(f"{OUTPUT_DIR}/shodan_results.txt", "w") as f:
    f.write("\n".join(shodan_results))

# === 6. Human Layer Recon ===
print("[6] Outputting LinkedIn and job recon queries...")
human_queries = [
    f"site:linkedin.com/in intitle:{DOMAIN}",
    f"site:linkedin.com/jobs {DOMAIN} SCADA",
    f"site:linkedin.com/in {DOMAIN} engineer"
]

with open(f"{OUTPUT_DIR}/human_layer.txt", "w") as f:
    for hq in human_queries:
        f.write(f"https://www.google.com/search?q={hq.replace(' ', '+')}\n")

# === 7. Screenshotting Portals ===
print("[7] Taking screenshots of discovered subdomains (requires gowitness)...")
screenshot_dir = os.path.join(OUTPUT_DIR, "screenshots")
os.makedirs(screenshot_dir, exist_ok=True)
subdomain_file = os.path.join(OUTPUT_DIR, "subdomains.txt")

with open(subdomain_file, "w") as f:
    subprocess.call(f"assetfinder {DOMAIN} | grep {DOMAIN}", shell=True, stdout=f)

subprocess.call(f"gowitness file -f {subdomain_file} -P {screenshot_dir} --no-http", shell=True)

# === 8. Generate Markdown Report ===
print("[8] Generating Markdown Report with Risk Scores...")
report_path = os.path.join(OUTPUT_DIR, "osint_summary.md")
with open(report_path, "w") as report:
    report.write(f"# OSINT Recon Summary for {DOMAIN}\n\n")
    report.write("## Discovered Artifacts with Risk Levels\n")
    report.write("- JavaScript URLs: wayback_js.txt [LOW]\n")
    report.write("- GitHub Secrets: github_api_results.txt [HIGH]\n")
    report.write("- Certificates: crtsh_query.txt [INFO]\n")
    report.write("- Bucket Mentions: bucket_keywords.txt [MEDIUM]\n")
    report.write("- Shodan Data: shodan_results.txt [MEDIUM]\n")
    report.write("- Human Intel Queries: human_layer.txt [LOW]\n")
    report.write("- Screenshots: screenshots/index.html [INFO]\n")

# === 9. Screenshot Viewer (HTML Index) ===
html_path = os.path.join(screenshot_dir, "index.html")
with open(html_path, "w") as html:
    html.write("<html><head><title>Screenshot Viewer</title></head><body>\n")
    html.write("<h1>Captured Screenshots</h1>\n")
    for img in os.listdir(screenshot_dir):
        if img.endswith(".png"):
            html.write(f"<div><img src='{img}' width='600'><p>{img}</p></div><hr>\n")
    html.write("</body></html>")

# === 10. MITRE ATT&CK Mapping and Recommendations ===
mitre_mapping = {
    "GitHub Secrets": {
        "technique": "T1552 - Unsecured Credentials",
        "recommendation": "Implement secret scanning pre-commit hooks and rotate exposed keys."
    },
    "JavaScript URLs": {
        "technique": "T1592.002 - Gather Victim Identity Information: Email Addresses",
        "recommendation": "Minimize exposed metadata and obfuscate internal endpoints in JS."
    },
    "Bucket Mentions": {
        "technique": "T1530 - Data from Cloud Storage",
        "recommendation": "Apply strict IAM roles and audit access to all cloud buckets."
    },
    "Shodan Data": {
        "technique": "T1595.002 - Active Scanning: Vulnerability Scanning",
        "recommendation": "Use firewalls, TLS, and VPNs to limit surface. Monitor exposed ports."
    },
    "Human Intel Queries": {
        "technique": "T1589 - Gather Victim Identity Info",
        "recommendation": "Limit oversharing in resumes, job descriptions, and public posts."
    }
}

with open(report_path, "a") as report:
    report.write("\n\n## MITRE ATT&CK Mapping and Recommendations\n")
    for key, val in mitre_mapping.items():
        report.write(f"\n**{key}**\n- Technique: {val['technique']}\n- Recommendation: {val['recommendation']}\n")

# === 11. Convert Markdown to PDF ===
pdf_path = os.path.join(OUTPUT_DIR, "osint_summary.pdf")
pandoc_cmd = f"pandoc {report_path} -o {pdf_path} --from markdown --pdf-engine=pdflatex"
os.system(pandoc_cmd)

# === 12. Zip the Folder ===
print("[12] Zipping project folder for easy transfer...")
subprocess.call(f"zip -r {OUTPUT_DIR}.zip {OUTPUT_DIR}", shell=True)

# === 13. Launcher Script ===
print("[13] Creating idiot-proof launcher.sh file...")
with open("run_this_like_a_boss.sh", "w") as launcher:
    launcher.write("#!/bin/bash\n")
    launcher.write("echo '[+] Starting automated OSINT recon mission!'\n")
    launcher.write("python3 osint_pivot_tool.py\n")
    launcher.write("echo '[✔] Done. Look in the .zip file for results!'\n")
os.chmod("run_this_like_a_boss.sh", 0o755)

print("""
To exfiltrate results:
1. Use this magical bash script:
   ./run_this_like_a_boss.sh

2. When done, transfer the .zip:
   scp osint_results_*.zip youruser@yourhost:/path/to/your/folder

3. Or drag it from the VM to your desktop using shared folders.

YOU ARE NOW A RECON WIZARD 
""")
