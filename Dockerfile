# Dockerfile for osint_pivot_tool.py

FROM python:3.11-slim

WORKDIR /app

# Copy script and requirements
COPY osint_pivot_tool.py .

# Install required CLI tools manually (Waybackurls, Assetfinder, Gowitness, Pandoc)
RUN apt-get update && \
    apt-get install -y git curl wget zip pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Go and CLI OSINT tools
RUN apt-get update && \
    apt-get install -y golang && \
    go install github.com/tomnomnom/waybackurls@latest && \
    go install github.com/tomnomnom/assetfinder@latest && \
    curl -Lo gowitness https://github.com/sensepost/gowitness/releases/latest/download/gowitness-linux-amd64 && \
    chmod +x gowitness && mv gowitness /usr/local/bin/ && \
    cp /root/go/bin/waybackurls /usr/local/bin/ && \
    cp /root/go/bin/assetfinder /usr/local/bin/ && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python libraries (only requests needed)
RUN pip install requests

ENTRYPOINT ["python3", "osint_pivot_tool.py"]
