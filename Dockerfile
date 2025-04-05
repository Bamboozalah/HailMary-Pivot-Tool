# Dockerfile for OSINT Pivot Tool (Hail Mary Edition)

FROM python:3.11-slim

# Install system utilities and OSINT tools
RUN apt-get update && apt-get install -y \
    git curl wget zip unzip build-essential \
    pandoc texlive-xetex \
    dnsutils jq gnupg gosu \
    && rm -rf /var/lib/apt/lists/*

# Install golang-based tools (waybackurls, assetfinder, gowitness)
RUN apt-get update && apt-get install -y golang-go && \
    go install github.com/tomnomnom/waybackurls@latest && \
    go install github.com/tomnomnom/assetfinder@latest && \
    go install github.com/sensepost/gowitness@latest && \
    cp /root/go/bin/* /usr/local/bin/

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY osint_pivot_tool.py run_this_like_a_boss.sh ./
RUN chmod +x run_this_like_a_boss.sh

ENTRYPOINT ["./run_this_like_a_boss.sh"]
