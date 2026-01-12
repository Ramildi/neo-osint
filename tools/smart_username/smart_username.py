#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import json
import time

init(autoreset=True)

# ================= GLOBAL CONFIG ================= #

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# ================= SITE DATABASE ================= #

SITES = {
    "GitHub": {
        "url": "https://github.com/{}",
        "error": ["not found"],
        "positive": ["repositories", "followers"]
    },
    "Instagram": {
        "url": "https://www.instagram.com/{}/",
        "error": ["sorry, this page isn't available"],
        "positive": ["profile", "posts"]
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{}",
        "error": ["page not found"],
        "positive": ["karma", "cake day"]
    },
    "Twitter/X": {
        "url": "https://x.com/{}",
        "error": ["this account doesn’t exist", "account suspended"],
        "positive": ["followers", "posts"]
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/{}/",
        "error": ["profile not found"],
        "positive": ["experience", "education", "skills"]
    },
    "TryHackMe": {
        "url": "https://tryhackme.com/p/{}",
        "error": ["page not found", "user not found"],
        "positive": ["rank", "badges", "rooms"]
    },
    "GitLab": {
        "url": "https://gitlab.com/{}",
        "error": ["404"],
        "positive": ["projects", "followers"]
    }
}

# ===== TELEGRAM & FORUM MODULE (INTEGRATED) ===== #

TELEGRAM_FORUM = {
    "Telegram Profile": {
        "url": "https://t.me/{}",
        "error": ["user not found", "if you have telegram"],
        "positive": ["view in telegram", "send message"]
    },
    "Telegram Channel": {
        "url": "https://t.me/s/{}",
        "error": ["not found", "private"],
        "positive": ["subscribers", "members"]
    },
    "HackTheBox Forum": {
        "url": "https://forum.hackthebox.com/u/{}",
        "error": ["not found"],
        "positive": ["activity", "topics"]
    },
    "StackOverflow": {
        "url": "https://stackoverflow.com/users/{}",
        "error": ["page not found"],
        "positive": ["reputation", "answers"]
    }
}

# ================= CORE ENGINE ================= #

def status_score(code):
    if code == 200:
        return 40
    if code in (301, 302):
        return 20
    if code in (401, 403, 999):
        return 10
    return -30

def scan_site(name, data, username):
    url = data["url"].format(username)
    score = 0

    try:
        r = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        html = r.text.lower()
        soup = BeautifulSoup(r.text, "html.parser")

        score += status_score(r.status_code)

        for word in data["positive"]:
            if word in html:
                score += 20

        for word in data["error"]:
            if word in html:
                score -= 60

        title = soup.title.string.strip() if soup.title else "No Title"
        if username.lower() in title.lower():
            score += 10

        return {
            "site": name,
            "url": url,
            "status": r.status_code,
            "title": title,
            "score": max(score, 0)
        }

    except Exception as e:
        return {
            "site": name,
            "url": url,
            "error": str(e),
            "score": 0
        }

# ================= MAIN ================= #

def main():
    print(Fore.CYAN + """
 ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗
 ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
 ███████╗██╔████╔██║███████║██████╔╝   ██║   
 ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
 ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
 ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   

   SMART OSINT TOOL – Sherlock++ + Telegram
    """)

    username = input(Fore.YELLOW + "🔍 Enter Username: ").strip()
    print(Fore.CYAN + "\n[ Scaning...]\n")

    results = []

    print(Fore.MAGENTA + "🌐 Social / Dev Platforms\n")
    for site, data in SITES.items():
        res = scan_site(site, data, username)
        results.append(res)

        color = Fore.GREEN if res["score"] >= 70 else Fore.YELLOW if res["score"] >= 35 else Fore.RED
        print(color + f"[{res['score']}%] {site}")
        time.sleep(0.8)

    print(Fore.MAGENTA + "\n💬 Telegram & Forum OSINT\n")
    for site, data in TELEGRAM_FORUM.items():
        res = scan_site(site, data, username)
        results.append(res)

        color = Fore.GREEN if res["score"] >= 70 else Fore.YELLOW if res["score"] >= 35 else Fore.RED
        print(color + f"[{res['score']}%] {site}")
        time.sleep(0.8)

    with open(f"osint_{username}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(Fore.CYAN + f"\n📁 Results saved → osint_{username}.json\n")
    print(Style.RESET_ALL)

if __name__ == "__main__":
    main()
