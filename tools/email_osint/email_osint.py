#!/usr/bin/env python3
# Passive Email OSINT

import re
import dns.resolver
import json

email = input("📧 Enter Email: ").strip()

result = {
    "email": email,
    "valid_format": False,
    "domain": None,
    "mx_records": [],
    "possible_services": []
}

pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
if re.match(pattern, email):
    result["valid_format"] = True
    domain = email.split("@")[1]
    result["domain"] = domain

    try:
        answers = dns.resolver.resolve(domain, "MX")
        for r in answers:
            result["mx_records"].append(str(r.exchange))
    except:
        result["mx_records"].append("No MX found")

    if "google" in str(result["mx_records"]).lower():
        result["possible_services"].append("Gmail / Google Workspace")
    if "outlook" in str(result["mx_records"]).lower():
        result["possible_services"].append("Microsoft / Outlook")

print(json.dumps(result, indent=4, ensure_ascii=False))

with open(f"email_osint_{email.replace('@','_')}.json", "w") as f:
    json.dump(result, f, indent=4)

print("\n📁 Results saved ")
