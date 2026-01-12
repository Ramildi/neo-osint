#!/usr/bin/env python3
# GLOBAL Passive Phone OSINT
# Legal & passive use only

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import json

number = input("📱 Number (+ for example +4915123456789): ").strip()

result = {
    "input": number,
    "valid": False,
    "international_format": None,
    "country": None,
    "country_code": None,
    "operator": None,
    "timezones": [],
    "possible_links": {}
}

try:
    # Parse number (region=None → qlobal)
    parsed = phonenumbers.parse(number, None)

    result["valid"] = phonenumbers.is_valid_number(parsed)

    if result["valid"]:
        result["international_format"] = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

        result["country"] = geocoder.description_for_number(parsed, "en")
        result["country_code"] = f"+{parsed.country_code}"
        result["operator"] = carrier.name_for_number(parsed, "en")
        result["timezones"] = list(timezone.time_zones_for_number(parsed))

        clean_number = number.replace("+", "").replace(" ", "")

        result["possible_links"] = {
            "telegram": f"https://t.me/{clean_number}",
            "whatsapp": f"https://wa.me/{clean_number}",
            "google_dork": f"https://www.google.com/search?q=\"{number}\""
        }

except phonenumbers.NumberParseException as e:
    result["error"] = str(e)

print(json.dumps(result, indent=4, ensure_ascii=False))

output_file = f"phone_osint_{number.replace('+','').replace(' ','')}.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"\n📁 Output saved → {output_file}\n")
