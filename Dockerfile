# Dockerfile for osint_pivot_tool.py

FROM python:3.11-slim

WORKDIR /app

# Copy script and requirements
COPY osint_pivot_tool.py .
COPY run_this_like_a_boss.sh .

# Install required CLI tools and dependencies
RUN apt-get update && \
    apt-get install -y git curl wget zip pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils && \
    apt-get install -y golang && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install OSINT CLI tools
RUN go install github.com/tomnomnom/waybackurls@latest && \
    go install github.com/tomnomnom/assetfinder@latest && \
    curl -Lo gowitness https://github.com/sensepost/gowitness/releases/latest/download/gowitness-linux-amd64 && \
    chmod +x gowitness && mv gowitness /usr/local/bin/ && \
    cp /root/go/bin/waybackurls /usr/local/bin/ && \
    cp /root/go/bin/assetfinder /usr/local/bin/

# Make launcher executable
RUN chmod +x run_this_like_a_boss.sh

# Install Python packages
RUN pip install requests

ENTRYPOINT ["./run_this_like_a_boss.sh"]

