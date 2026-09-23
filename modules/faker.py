#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import time, random, string, threading, os, base64, re, requests, json
from pystyle import Colors, Center, System
from core.display import Colorate, get_inpt, Theme, print_banner

def _cls(title):
    os.system('cls' if os.name == 'nt' else 'clear')
    System.Title(f"Navi - {title}")

def fake_token_gen():
    _cls("Token Generator")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  _______  _        _______  _        _______  _______ 
 (  ____ \( (    /|(  ____ \( (    /|(  ____ \(  ____ )
 | (    \/|  \  ( || (    \/|  \  ( || (    \/| (    |)
 | (__    |   \ | || (__    |   \ | || (__    | (____)|
 |  __)   | (\ \) ||  __)   | (\ \) ||  __)   |     __)
 | (      | | \   || (      | | \   || (      | (\ (   
 | (____/\| )  \  || (____/\| )  \  || (____/\| ) \ \__
 (_______/|/    )_)(_______/|/    )_)(_______/|/   \__/
    """))
    print(Colorate.Horizontal(cl["head"], "  [+] Initializing Token Generation..."))
    amt = int(get_inpt("Amount to generate:") or 5)
    
    for i in range(amt):
        u = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        em = f"{u}@atomicmail.io"
        print(f"\n  {Colorate.Horizontal(cl['num'], '[1]')} Using Email: {Colorate.Horizontal(cl['txt'], em)}")
        time.sleep(0.8)
        print(f"  {Colorate.Horizontal(cl['num'], '[2]')} Connecting to Discord Gateway...")
        time.sleep(1.2)
        print(f"  {Colorate.Horizontal(cl['num'], '[3]')} Solving HCaptcha {Colorate.Horizontal(cl['txt'], '(Enterprise Mode)')}...")
        time.sleep(random.uniform(1.5, 3.0))
        print(f"  {Colorate.Horizontal(cl['num'], '[4]')} Account Created. Verifying Email...")
        time.sleep(1.0)
        
        p1 = base64.b64encode(str(random.randint(100000000000000000, 999999999999999999)).encode()).decode().rstrip("=")
        p2 = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        p3 = ''.join(random.choices(string.ascii_letters + string.digits + "-_", k=27))
        tk = f"{p1}.{p2}.{p3}"
        
        print(Colorate.Horizontal(cl["head"], f"  [SUCCESS] Token: {tk}"))
        if not os.path.exists("output"): os.makedirs("output")
        with open("output/fake_tokens.txt", "a") as f: f.write(f"{tk}\n")
    
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_exodus():
    _cls("Exodus Larp")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [+] Generating fake seed file for larping..."))    
    content = f"""
EXODUS WALLET RECOVERY - BACKUP
-------------------------------
DATE: {time.strftime("%Y-%m-%d %H:%M:%S")}
TYPE: 12-WORD MNEMONIC

RECOVERY PHRASE 1:
critic draw oak hood reward bunker next old spy about clown notice


-------------------------------
[!] Keep in mind that this is a larp. You are not able to move the funds.
[!] Navi Multitool - Faker mode
"""
    
    path = "output/exodus_seed.txt"
    if not os.path.exists("output"): os.makedirs("output")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(Colorate.Horizontal(cl["head"], f"  [>] Success! File created: {path}"))
    print(Colorate.Horizontal(cl["num"], "  [>] Opening file..."))
    
    try:
        os.startfile(os.path.abspath(path))
    except:
        print(Colorate.Horizontal(cl["num"], "  [!] Could not auto-open. Please open output/exodus_seed.txt manually."))
    
    time.sleep(1)
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_mail_gen():
    _cls("Mail Generator")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  __  __   _   ___ _    
 |  \/  | /_\ |_ _| |   
 | |\/| |/ _ \ | || |__ 
 |_|  |_/_/ \_\___|____|
    """))
    print(Colorate.Horizontal(cl["head"], "  [+] Initializing Fake Mail Generator..."))
    amt = int(get_inpt("Amount to generate:") or 10)
    doms = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com", "hotmail.com"]
    for i in range(amt):
        u = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12)))
        m = f"{u}@{random.choice(doms)}"
        print(Colorate.Horizontal(cl["num"], f"  [>] Created: ") + Colorate.Horizontal(cl["txt"], m))
        time.sleep(0.05)
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_identity_gen():
    _cls("Identity Generator")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  ___ ___  ___ _  _ _____ ___ _______   __
 |_ _|   \| __| \| |_   _|_ _|_   _\ \ / /
  | || |) | _|| .` | | |  | |  | |  \ V / 
 |___|___/|___|_|\_| |_| |___| |_|   |_|  
    """))
    print(Colorate.Horizontal(cl["head"], "  [+] Generating Fake Identity..."))
    fnames = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda"]
    lnames = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]
    
    id_data = [
        ("Full Name", f"{random.choice(fnames)} {random.choice(lnames)}"),
        ("DOB", f"{random.randint(1970, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"),
        ("Address", f"{random.randint(100, 999)} {random.choice(lnames)} St, {random.choice(cities)}"),
        ("SSN", f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"),
        ("Phone", f"+1 ({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}")
    ]
    
    print(Colorate.Horizontal(cl["head"], "  " + "─" * 40))
    for k, v in id_data:
        print(Colorate.Horizontal(cl["num"], f"  [>] {k:<15}: ") + Colorate.Horizontal(cl["txt"], v))
        time.sleep(0.2)
    print(Colorate.Horizontal(cl["head"], "  " + "─" * 40))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_nitro_gen():
    _cls("Nitro Generator")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  _  _ ___ _____ ___  ___ 
 | \| |_ _|_   _| _ \/ _ \
 | .` || |  | | |   / (_) |
 |_|\_|___| |_| |_|_\\___/ 
    """))
    print(Colorate.Horizontal(cl["head"], "  [+] Starting Fake Nitro Gen (Visual Mode)..."))
    count = 0
    try:
        while True:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            is_hit = random.random() < 0.01
            if is_hit:
                print(Colorate.Horizontal(cl["head"], f"  [HIT] discord.gift/{code}"))
                count += 1
            else:
                print(Colorate.Horizontal(cl["num"], f"  [BAD] discord.gift/{code}"), end="\r")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print(Colorate.Horizontal(cl["head"], f"\n  [=] Session ended. Hits: {count}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_ddos():
    _cls("DDoS Simulator")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["num"], """
  ____  ____  ____  ____ 
 |  _ \|  _ \/ __ \/ ___|
 | | | | | | | | | \___ \
 | |_| | |_| | |_| |___) |
 |____/|____/ \____/|____/ 
    """))
    target = get_inpt("Target IP:")
    port = get_inpt("Port (80):") or "80"
    print(Colorate.Horizontal(cl["head"], f"  [+] Launching simulated DDoS on {target}:{port}..."))
    time.sleep(1)
    try:
        while True:
            bytes_sent = random.randint(500, 1500)
            print(Colorate.Horizontal(cl["num"], f"  [>] Sent {bytes_sent} bytes to {target} via UDP..."), end="\r")
            time.sleep(0.02)
    except KeyboardInterrupt:
        print(Colorate.Horizontal(cl["head"], "\n  [!] Attack stopped."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_cc_gen():
    _cls("Credit Card Gen")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
   ____ ____ ____ ____ ____ ____ 
  / ___|  _ \ ___|  _ \_ _|  _ \
 | |   | |_) |__ | | | | || | | |
 | |___|  _ <|___| |_| | || |_| |
  \____|_| \_\   |____/___|____/ 
    """))
    print(Colorate.Horizontal(cl["head"], "  [+] Generating Fake Credit Cards (Luhn Valid)..."))
    amt = int(get_inpt("Amount:") or 5)
    for _ in range(amt):
        prefix = random.choice(["4", "51", "52", "53", "54", "55", "34", "37"])
        body = ''.join(random.choices(string.digits, k=13 if prefix.startswith("3") else 14))
        cc = f"{prefix}{body}"
        exp = f"{random.randint(1, 12):02d}/{random.randint(24, 30)}"
        cvv = random.randint(100, 999)
        print(Colorate.Horizontal(cl["num"], f"  [>] {cc} | EXP: {exp} | CVV: {cvv}"))
        time.sleep(0.1)
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_wallet_miner():
    _cls("Wallet Miner")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  __  __ ___ _  _ ___ ___ 
 |  \/  |_ _| \| | __| _ \\
 | |\/| || || .` | _||   /
 |_|  |_|___|_|\_|___|_|_\\
    """))
    wallet = get_inpt("Wallet Address:")
    print(Colorate.Horizontal(cl["head"], f"  [+] Connecting to pool for {wallet[:10]}..."))
    balance = 0.0
    try:
        while True:
            hashrate = random.uniform(45.5, 98.2)
            earned = random.uniform(0.0001, 0.0005)
            balance += earned
            print(Colorate.Horizontal(cl["txt"], f"  [~] Mining... {hashrate:.2f} MH/s | Balance: {balance:.6f} BTC"), end="\r")
            time.sleep(0.1)
            if random.random() < 0.05:
                print(Colorate.Horizontal(cl["head"], f"\n  [!] Block found! Reward: {earned*10:.6f} BTC"))
    except KeyboardInterrupt:
        print(Colorate.Horizontal(cl["head"], f"\n  [=] Final Balance: {balance:.6f} BTC"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def social_botter():
    _cls("Social Botter")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  ___  ___ _____ _____ ___ ___ 
 | _ )/ _ \_   _|_   _| __| _ \\
 | _ \ (_) || |   | | | _||   /
 |___/\___/ |_|   |_| |___|_|_\\
    """))
    platform = get_inpt("Platform (IG/TikTok/YT):")
    user = get_inpt("Username:")
    amt = int(get_inpt("Followers amount:") or 1000)
    print(Colorate.Horizontal(cl["head"], f"  [+] Booting {platform} bots for {user}..."))
    for i in range(1, amt + 1, random.randint(5, 20)):
        print(Colorate.Horizontal(cl["num"], f"  [>] Adding followers... {i}/{amt}"), end="\r")
        time.sleep(0.05)
    print(Colorate.Horizontal(cl["head"], f"\n  [=] Successfully added {amt} followers to {user}."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_paypal_otp():
    _cls("PayPal OTP Bypass")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  ___   _ __   __ ___  _   _    
 | _ \ /_\\ \ / /| _ \/_\ | |   
 |  _// _ \\ V / |  _/ _ \| |__ 
 |_| /_/ \_\|_|  |_|/_/ \_\____|
    """))
    email = get_inpt("Target Email:")
    print(Colorate.Horizontal(cl["head"], f"  [+] Requesting OTP bypass for {email}..."))
    time.sleep(1.5)
    print(Colorate.Horizontal(cl["num"], "  [>] Intercepting SMS gateway..."))
    time.sleep(2)
    otp = ''.join(random.choices(string.digits, k=6))
    print(Colorate.Horizontal(cl["head"], f"  [!] OTP FOUND: {otp}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_account_gen():
    _cls("Account Gen")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
    _   ___ ___ ___  _   _ _  _ _____ 
   /_\ / __/ __/ _ \| | | | \| |_   _|
  / _ \ (_| (_| (_) | |_| | .` | | |  
 /_/ \_\___\___\___/ \___/|_|\_| |_|  
    """))
    service = get_inpt("Service (Steam/Epic/etc):")
    amt = int(get_inpt("Amount:") or 5)
    print(Colorate.Horizontal(cl["head"], f"  [+] Generating {service} accounts..."))
    for _ in range(amt):
        u = ''.join(random.choices(string.ascii_lowercase, k=8))
        p = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        print(Colorate.Horizontal(cl["num"], f"  [>] {u}:{p}"))
        time.sleep(0.1)
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_fortnite_checker():
    _cls("Fortnite Checker")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  ___ ___  ___ _____ _  _ ___ _____ ___ 
 | __/ _ \| _ \_   _| \| |_ _|_   _| __|
 | _| (_) |   / | | | .` || |  | | | _| 
 |_| \___/|_|_\ |_| |_|\_|___| |_| |___|
    """))
    print(Colorate.Horizontal(cl["head"], "  [+] Starting Fortnite Checker (Visual)..."))
    try:
        while True:
            u = ''.join(random.choices(string.ascii_lowercase, k=6))
            skins = random.randint(0, 200)
            is_rare = skins > 150 or random.random() < 0.05
            if is_rare:
                print(Colorate.Horizontal(cl["head"], f"  [RARE] {u}@gmail.com | Skins: {skins} | OG: Yes"))
            else:
                print(Colorate.Horizontal(cl["num"], f"  [SKIPPED] {u}@gmail.com | Skins: {skins}"), end="\r")
            time.sleep(0.05)
    except KeyboardInterrupt: pass
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def fake_hacker_typer():
    _cls("Hacker Terminal")
    _cl = Theme.get_colors()
    print(Colorate.Horizontal(_cl["head"], "  [!] Press CTRL+C to stop hacking..."))
    time.sleep(1)
    try:
        while 1:
            _s = "".join(random.choices("0123456789ABCDEF", k=random.randint(16, 64)))
            print(Colorate.Horizontal(_cl["head" if random.random() < 0.1 else "num"], f"  {_s}"))
            time.sleep(0.01)
    except KeyboardInterrupt: pass

def fake_ransomware():
    _cl = Theme.get_colors()
    _cls("Critical System Failure")
    print(Colorate.Horizontal(Colors.red, Center.XCenter(r"""
    
    [!] YOUR FILES HAVE BEEN ENCRYPTED [!]
    
    To decrypt your files, send 0.5 BTC to:
    bc1pqdsuxtmgx5ds6c0xf6nydfwxj5hzdkterv9v02sc5js67sgs8w7qj6373f
    
    Time remaining: 23:59:59
    
    """)))
    input(Colorate.Horizontal(Colors.red, " "))

def fake_qr_gen():
    _cls("QR Code Generator")
    _cl = Theme.get_colors()
    _d = get_inpt("text/url:")
    if not _d: return
    print(Colorate.Horizontal(_cl["head"], "  [+] Generating QR code..."))
    try:
        import qrcode
        _qr = qrcode.make(_d)
        if not os.path.exists("output"): os.makedirs("output")
        _safe = re.sub(r'[\\/:*?"<>|]', '_', _d[:30])
        _p = os.path.join("output", f"qr_{_safe}.png")
        _qr.save(_p)
        print(Colorate.Horizontal(_cl["head"], f"  [+] Saved to: {_p}"))
        try: os.startfile(os.path.abspath(_p))
        except: pass
    except ImportError:
        os.system("pip install qrcode[pil] -q")
        print(Colorate.Horizontal(_cl["num"], "  [!] Installed qrcode, re-run to generate."))
    except Exception as _e: print(Colorate.Horizontal(_cl["num"], f"  [!] Error: {_e}"))
    input(Colorate.Horizontal(_cl["head"], "\n  Press Enter..."))

def fake_bruteforcer():
    _cls("Account Bruteforcer")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], """
  ____  _____  _    _ _______ ______ 
 |  _ \|  __ \| |  | |__   __|  ____|
 | |_) | |__) | |  | |  | |  | |__   
 |  _ <|  _  /| |  | |  | |  |  __|  
 | |_) | | \ \| |__| |  | |  | |____ 
 |____/|_|  \_\\\\____/   |_|  |______|
    """))
    
    platform = get_inpt("Platform (IG/TikTok/Twitch):")
    target = get_inpt("Target Username:")
    threads = int(get_inpt("Threads (1-500):") or 100)
    
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Initializing attack on {target} ({platform})..."))
    time.sleep(1)
    print(Colorate.Horizontal(cl["num"], "  [>] Loading proxies from 'proxies.txt' (Scraped 5,204 HTTP/S)..."))
    time.sleep(1.5)
    print(Colorate.Horizontal(cl["num"], "  [>] Loading combo list from 'passwords.txt' (1.2M entries)..."))
    time.sleep(2)
    
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Brute-force attack started with {threads} threads.\n"))
    
    attempts = 0
    start_time = time.time()
    
    try:
        while attempts < 10000:
            for _ in range(random.randint(5, 15)):
                pw = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 14)))
                status = random.choice([
                    f"{Colorate.Horizontal(cl['num'], '[FAILED]')} {pw:<20} | Proxy: {random.randint(1,255)}.{random.randint(1,255)}:8080",
                    f"{Colorate.Horizontal(cl['num'], '[RETRY] ')} {pw:<20} | Rate Limited - Switching Proxy...",
                    f"{Colorate.Horizontal(cl['num'], '[ERROR] ')} {pw:<20} | Connection Timeout",
                ])
                print(f"  {status}")
                attempts += 1
                
                if random.random() < 0.05:
                    time.sleep(0.1)
                
            time.sleep(0.01)
            
            if random.random() < 0.02:
                print(Colorate.Horizontal(cl["head"], f"  [!] Rotating proxy pool... (Active: {random.randint(400, 5000)})"))
                time.sleep(0.5)

            if attempts > 500: # After some "real" looking attempts, show the message
                break
                
    except KeyboardInterrupt:
        pass

    print("\n" + "─" * 60)
    print(Colorate.Horizontal(cl["head"], f"  [!] BRUTEFORCE STATUS: {Colorate.Horizontal(cl['txt'], 'IN PROGRESS...')}"))
    print(Colorate.Horizontal(cl["head"], f"  [!] NOTICE: {Colorate.Horizontal(cl['txt'], 'Bruteforcing passwords this will take time, but the engine is bypasssing 2FA and Rate-limits.')}"))
    print(Colorate.Horizontal(cl["head"], f"  [!] INFO: {Colorate.Horizontal(cl['txt'], 'Navi Multitool - Advanced Simulation Engine.')}"))
    print("─" * 60)
    
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def faker_explanation():
    _cls("Explanation")
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [ EXPLANATION ]"))
    print(Colorate.Horizontal(cl["txt"], "  The Faker section is designed for aesthetic and \n  demonstration purposes. All tools here are \n  SIMULATED and do not perform real actions.\n  \n  Use them to inject ur stealer or just to larp."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
