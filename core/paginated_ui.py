#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import os
import sys
import shutil
import re
import random
try:
    import psutil
except ImportError:
    psutil = None

from core.display import Theme, Colorate, Colors, clr, get_config

PAGES = [
    {
        "title": "DISCORD TOOLS",
        "description": "API operations, token utilities, and guild management",
        "tools": [
            ("1", "Webhook Tools", "Spam or delete Discord webhooks"),
            ("2", "Token Tools", "Information, account nuker, token login & rotation"),
            ("3", "Nitro Generator", "Multi-threaded Discord Nitro gift generator"),
            ("4", "Server Info", "Retrieve detailed guild information from invite link"),
            ("5", "Bot Invite Gen", "Generate administrator bot invite links"),
            ("6", "Selfbot", "Launch a custom Discord selfbot menu"),
            ("7", "Server Cloner", "Clone Discord servers using a token"),
            ("8", "Nuke Bot", "Advanced server destruction bot console"),
            ("9", "Username Checker", "Check availability of Discord usernames")
        ]
    },
    {
        "title": "OSINT & NETWORK",
        "description": "IP, DNS, whois, phone tracer, and dox trackers",
        "tools": [
            ("10", "Port Scanner", "Scan target hosts for open ports"),
            ("11", "Whois Lookup", "Retrieve domain registration details"),
            ("12", "DNS Lookup", "Lookup target DNS records (A, MX, TXT...)"),
            ("14", "Dox Tracker", "Lookup dox information database"),
            ("15", "Dox Creator", "Create custom doxing profiles"),
            ("16", "Phone Lookup", "Lookup carrier and location of phone numbers"),
            ("17", "Email Lookup", "Retrieve OSINT data associated with emails")
        ]
    },
    {
        "title": "MALICIOUS TOOLS",
        "description": "DDoS, vulns, wallet scanners, and payload builders",
        "tools": [
            ("20", "Email Bomber", "Send spam emails to target address"),
            ("21", "Crypto Clipper", "Build clipboard-hijacking cryptocurrency clippers"),
            ("22", "Vuln Scanner", "Scan targets for common vulnerabilities"),
            ("23", "DDoS Attack", "Perform high-traffic network stress tests"),
            ("24", "Stealer Builder", "Compile password and token stealing payloads"),
            ("25", "Keylogger Builder", "Build stealth keystroke logging applications"),
            ("26", "IP Grabber", "Generate tracking links to log visitor IPs"),
            ("27", "Rat Builder", "Build Remote Access Trojan stubs"),
            ("28", "Wallet Bruteforce", "Bruteforce mnemonic phrases for crypto wallets")
        ]
    },
    {
        "title": "ROBLOX UTILITIES",
        "description": "Cookie tools, account logins, and group tools",
        "tools": [
            ("40", "User Info", "Retrieve detailed Roblox account information"),
            ("41", "Cookie Info", "Validate and check Roblox account cookie data"),
            ("42", "Cookie Login", "Directly log into Roblox via account cookies"),
            ("43", "Group Info", "Analyze details of target Roblox groups"),
            ("44", "Asset DL", "Download game assets and shirt/pants textures"),
            ("45", "Name History", "Track and display past usernames of a target"),
            ("46", "Username Checker", "Check availability of Roblox usernames"),
            ("47", "Cookie Refresher", "Generate a new cookie from an existing one")
        ]
    },
    {
        "title": "FAKER & SIMULATORS",
        "description": "Phishing tools, web cloners, and visual simulations",
        "tools": [
            ("50", "Faker Tools", "Access 17 simulations like Fake Nitro, Exodus, PayPal OTP"),
            ("34", "Web Cloner", "Clone HTML source code of target websites"),
            ("35", "QR Code Gen", "Generate standard and fake QR codes")
        ]
    },
    {
        "title": "GENERAL & SYSTEM",
        "description": "Codecs, obfuscators, metadata, and app settings",
        "tools": [
            ("30", "Base64 Codec", "Encode or decode strings using Base64"),
            ("31", "System Info", "Inspect local machine hardware specifications"),
            ("32", "IP Pinger", "Ping target IPs to check latency and availability"),
            ("33", "Obfuscator", "Obfuscate Python code to prevent reverse engineering"),
            ("13", "Metadata Scan", "Analyze and remove EXIF metadata from media files"),
            ("60", "App Info", "Display version, license, and developers"),
            ("61", "App Config", "Manage themes, updates, and startup toggles"),
            ("62", "Disable Antivirus", "Add C drive to Defender exclusions to prevent tool interruptions"),
            ("63", "Windows Debloater", "Launch Windows Utility to debloat and optimize OS"),
            ("64", "Proxy Scraper", "Scrape HTTP, SOCKS4, and SOCKS5 proxies"),
            ("65", "Proxy Checker", "Test scraped proxies for latency and validity")
        ]
    }
]

def _strip(_t):
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', _t)

class PaginatedUI:
    ACTIVE_LOGO = None
    @staticmethod
    def get_layout_width():
        tw = shutil.get_terminal_size().columns
        return max(74, min(100, tw - 4))
    @staticmethod
    def get_margin(box_w):
        tw = shutil.get_terminal_size().columns
        return " " * max(0, (tw - box_w) // 2)
    @staticmethod
    def draw_tabs(active_idx, colors, box_w, margin):
        inner = box_w - 2
        sep = " │ "
        tab_names = ["DISCORD", "OSINT", "MALICIOUS", "ROBLOX", "FAKER", "SYS/GEN"]
        short_names = ["DISC", "OSINT", "MALIC", "RBLX", "FAKER", "SYS"]
        def build_tab_line(names):
            labels = []
            for idx, name in enumerate(names):
                if idx == active_idx:
                    labels.append(f"► {name} ◄")
                else:
                    labels.append(f" {name} ")
            return sep.join(labels)
        tab_line = build_tab_line(tab_names)
        if len(tab_line) > inner:
            tab_line = build_tab_line(short_names)
        if len(tab_line) > inner:
            labels = []
            for idx in range(len(tab_names)):
                if idx == active_idx:
                    labels.append(f"►{idx+1}◄")
                else:
                    labels.append(f"[{idx+1}]")
            tab_line = sep.join(labels)
        pad = max(0, (inner - len(tab_line)) // 2)
        extra = max(0, inner - len(tab_line) - pad * 2)
        pad_str = " " * pad
        extra_str = " " * extra
        top = "╔" + "═" * inner + "╗"
        bot = "╚" + "═" * inner + "╝"
        parts = tab_line.split(sep)
        colored_content = ""
        for idx, part in enumerate(parts):
            if "►" in part:
                colored_content += Colorate.Horizontal(colors["banner"], part)
            else:
                colored_content += Colorate.Horizontal(colors["txt"], part)
            if idx < len(parts) - 1:
                colored_content += Colorate.Horizontal(colors["num"], sep)
        print(margin + Colorate.Horizontal(colors["num"], top))
        print(margin + "║" + pad_str + colored_content + pad_str + extra_str + "║")
        print(margin + Colorate.Horizontal(colors["num"], bot))
    @staticmethod
    def draw_page_content(active_idx, colors, box_w, margin):
        page = PAGES[active_idx]
        inner = box_w - 2
        title = f" {page['title']} - {page['description']} "
        if len(title) > inner:
            title = f" {page['title']} "
        border_len = max(2, (inner - len(title)) // 2)
        extra_dash = "─" if (inner - len(title)) % 2 != 0 else ""
        top = "┌" + "─" * border_len + title + "─" * border_len + extra_dash + "┐"
        print(margin + Colorate.Horizontal(colors["head"], top))
        print(margin + Colorate.Horizontal(colors["num"], "│" + " " * inner + "│"))
        name_col_w = max(15, min(22, inner // 4))
        opt_w = 9 
        for num, name, desc in page["tools"]:
            opt = f"  [{num.zfill(2)}] "
            name_pad = " " * max(1, name_col_w - len(name))
            sep_str = "─  "
            max_desc = inner - len(opt) - name_col_w - len(sep_str) - 2
            disp_desc = desc[:max_desc - 3] + "..." if len(desc) > max_desc else desc
            plain = f"{opt}{name}{name_pad}{sep_str}{disp_desc}"
            pad_right = " " * max(0, inner - len(plain))
            line = (
                Colorate.Horizontal(colors["num"], "│") +
                Colorate.Horizontal(colors["num"], opt) +
                Colorate.Horizontal(colors["txt"], name) +
                Colorate.Horizontal(colors["num"], name_pad + sep_str) +
                Colorate.Horizontal(colors["txt"], disp_desc) +
                pad_right +
                Colorate.Horizontal(colors["num"], "│")
            )
            print(margin + line)
        print(margin + Colorate.Horizontal(colors["num"], "│" + " " * inner + "│"))
        print(margin + Colorate.Horizontal(colors["head"], "└" + "─" * inner + "┘"))

    @staticmethod
    def draw_footer(colors, box_w, margin):
        inner = box_w - 2
        nav_str = " [P/N] Prev/Next Page  │  [60] Info  │  [61] Settings  │  [99] Exit "

        if len(nav_str) > inner:
            nav_str = " [P/N] Pg  │  [60] Info  │  [61] Set  │  [99] Exit "
        pad = max(0, (inner - len(nav_str)) // 2)
        extra = max(0, inner - len(nav_str) - pad * 2)
        mid = "│" + " " * pad + nav_str + " " * pad + " " * extra + "│"
        print(margin + Colorate.Horizontal(colors["num"], "┌" + "─" * inner + "┐"))
        print(margin + Colorate.Horizontal(colors["txt"], mid))
        print(margin + Colorate.Horizontal(colors["num"], "└" + "─" * inner + "┘"))
        cfg = get_config()
        user = os.environ.get('USERNAME') or os.environ.get('USER') or 'User'
        ver = cfg.get("version", "2.0.0")
        stats_str = ""
        if psutil:
            try:
                cpu = int(psutil.cpu_percent())
                ram = int(psutil.virtual_memory().percent)
                stats_str = f" │ cpu: {cpu}% │ ram: {ram}%"
            except:
                pass
        
        small_info = f"v{ver}{stats_str}"
        tw = shutil.get_terminal_size().columns
        print(Colorate.Horizontal(colors["num"], small_info.center(tw)))

    @classmethod
    def draw_logo(cls, colors):
        if cls.ACTIVE_LOGO is None:
            banners = [
                [
                    r"   _   _               _  ",
                    r"  | \ | |             (_) ",
                    r"  |  \| |  __ _ __ __ _   ",
                    r"  | . ` | / _` |\ \ / /| |",
                    r"  | |\  || (_| | \ V / | |",
                    r"  |_| \_| \__,_|  \_/  |_|",
                ],
                [
                    r"      ::::    :::     :::     :::     ::: ::::::::::: ",
                    r"     :+:+:   :+:   :+: :+:   :+:     :+:     :+:      ",
                    r"    :+:+:+  +:+  +:+   +:+  +:+     +:+     +:+       ",
                    r"   +#+ +:+ +#+ +#++:++#++: +#+     +:+     +#+        ",
                    r"  +#+  +#+#+# +#+     +#+  +#+   +#+      +#+         ",
                    r" #+#   #+#+# #+#     #+#   #+#+#+#       #+#          ",
                    r"###    #### ###     ###     ###     ###########       ",
                ],
                [
                    r"  _   _    _ __     _____ ",
                    r" | \ | |  / \ \   / /_ _|",
                    r" |  \| | / _ \ \ / / | | ",
                    r" | |\  |/ ___ \ V /  | | ",
                    r" |_| \_/_/   \_\_/  |___|",
                ]
            ]
            cls.ACTIVE_LOGO = random.choice(banners)
            
        logo_lines = cls.ACTIVE_LOGO
        tw = shutil.get_terminal_size().columns
        max_w = max(len(l) for l in logo_lines)
        offset = max(0, (tw - max_w) // 2)
        margin = " " * offset
        for line in logo_lines:
            print(Colorate.Horizontal(colors["banner"], margin + line))
        
        print()
        print(Colorate.Horizontal(colors["sub"], "~ Present Day, Present Time ~".center(tw)))
        print()

    @classmethod
    def draw_dashboard(cls, active_idx):
        clr()
        colors = Theme.get_colors()
        box_w = cls.get_layout_width()
        margin = cls.get_margin(box_w)
        cls.draw_logo(colors)
        print()
        cls.draw_tabs(active_idx, colors, box_w, margin)
        print()
        cls.draw_page_content(active_idx, colors, box_w, margin)
        print()
        cls.draw_footer(colors, box_w, margin)

    @staticmethod
    def draw_card_box(title, items, theme_colors=None):
        colors = theme_colors or Theme.get_colors()
        tw = shutil.get_terminal_size().columns
        box_w = max(50, min(80, tw - 6))
        inner = box_w - 2
        margin = " " * max(0, (tw - box_w) // 2)

        border_len = max(2, (inner - len(title)) // 2)
        extra_dash = "─" if (inner - len(title)) % 2 != 0 else ""
        top_line = "┌" + "─" * border_len + title + "─" * border_len + extra_dash + "┐"
        if len(top_line) > box_w:
            top_line = top_line[:box_w - 1] + "┐"

        print()
        print(margin + Colorate.Horizontal(colors["head"], top_line))
        print(margin + Colorate.Horizontal(colors["num"], "│" + " " * inner + "│"))

        _items = list(items.items())
        col_w = (inner - 2) // 2 

        for i in range(0, len(_items), 2):
            k1, v1 = _items[i]
            k2, v2 = _items[i + 1] if i + 1 < len(_items) else ("", "")

            max_v = col_w - len(k1) - 5 
            val1 = (v1[:max_v - 3] + "...") if len(v1) > max_v else v1
            cell1 = f"  [{k1}] {val1:<{max_v}}"

            if k2:
                max_v2 = col_w - len(k2) - 5
                val2 = (v2[:max_v2 - 3] + "...") if len(v2) > max_v2 else v2
                cell2 = f"  [{k2}] {val2:<{max_v2}}"
            else:
                cell2 = " " * col_w

            plain_row = cell1 + cell2
            pad_right = max(0, inner - len(plain_row))
            colored_row = (
                Colorate.Horizontal(colors["num"], "│") +
                Colorate.Horizontal(colors["num"], f"  [{k1}]") +
                " " +
                Colorate.Horizontal(colors["txt"], f"{val1:<{max_v}}") +
                (
                    Colorate.Horizontal(colors["num"], f"  [{k2}]") +
                    " " +
                    Colorate.Horizontal(colors["txt"], f"{val2:<{max_v2}}")
                    if k2 else " " * col_w
                ) +
                " " * pad_right +
                Colorate.Horizontal(colors["num"], "│")
            )
            print(margin + colored_row)
        print(margin + Colorate.Horizontal(colors["num"], "│" + " " * inner + "│"))
        print(margin + Colorate.Horizontal(colors["head"], "└" + "─" * inner + "┘"))
