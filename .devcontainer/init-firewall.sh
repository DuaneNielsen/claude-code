#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, and pipeline failures
IFS=$'\n\t'       # Stricter word splitting

echo "Completely disabling firewall - flushing all iptables rules..."

# Flush all existing rules and chains
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -t raw -F 2>/dev/null || true
iptables -t raw -X 2>/dev/null || true

# Destroy any ipsets
ipset destroy 2>/dev/null || true

# Set all default policies to ACCEPT (completely open)
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

echo "Firewall completely disabled - all traffic allowed"
echo "Verifying internet access..."

# Test connectivity
if curl --connect-timeout 5 https://example.com >/dev/null 2>&1; then
    echo "Internet access verification passed - able to reach https://example.com"
else
    echo "Warning: Unable to reach https://example.com, but firewall is disabled"
fi
