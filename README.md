# 🛰️ OSINT Pivot Tool (Hail Mary Edition, because you do be desperate sometimes...)

A full-spectrum, automated cloud recon and pivot generation tool for nerds.

> This Dockerized version runs everything inside a self-contained OSINT box, with optional Shodan and GitHub integrations.

---

## Quickstart (Docker)

### Build the image
```bash
docker build -t osintpivotbox .
```

### 🧪 Run the tool
```bash
docker run -it --rm \
  -v $(pwd):/app \
  -e SHODAN_API_KEY=your_shodan_key \
  -e GITHUB_TOKEN=your_github_token \
  osintpivotbox
```
You’ll be prompted for a domain. Results are zipped in `osint_results_<domain>_<timestamp>.zip`

---

## 🔍 What It Does

1.  **Wayback JS**: Enumerates JavaScript files from Wayback
2.  **GitHub Dorks**: Searches for exposed secrets via API
3.  **crt.sh**: Generates cert search links
4.  **Bucket Keywords**: Filters for cloud keywords in archived URLs
5.  **Shodan API Queries**: Searches for live hosts, SSL, ports
6.  **Human Layer Recon**: LinkedIn + job postings + SCADA keywords
7.  **Screenshot Capture**: Uses gowitness to snapshot exposed portals
8.  **Markdown + PDF Reporting**: Includes MITRE ATT&CK mapping
9.  **ZIP Packaging**: Bundles all output

---

## Why It Is FRESH TO DEATH
- No external tools needed — just Docker + your API keys
- MITRE technique references and remediation notes
- Hands-off automation: launch it and go fall down an unrelated rabbit hole

---

## Output Structure
```
osint_results_<domain>_<timestamp>/
├── github_api_results.txt
├── wayback_js.txt
├── bucket_keywords.txt
├── crtsh_query.txt
├── human_layer.txt
├── shodan_results.txt
├── subdomains.txt
├── screenshots/
│   ├── *.png
│   └── index.html
├── osint_summary.md
├── osint_summary.pdf
└── osint_results_<...>.zip
```

---

## If you don't love it you can always:
- Add more GitHub dorks or Shodan queries to the script
- Use in workshops, tabletop exercises, or threat reports
- Pair with `deep_recon` for domain → subdomain → pivot chaining

---

## 🛡️ Disclaimer
This tool is for **authorized security research and educational purposes only**. Misuse could violate laws, maybe?

---

##Pulls by invite only


