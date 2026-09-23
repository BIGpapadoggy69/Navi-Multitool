import os, requests, random, threading, time
from core.display import Colors, Colorate, get_inpt, Theme

class Console():        
    def ui(self):
        pass

    def printer(self, color, status, code):
        cl = Theme.get_colors()
        with threading.Lock():
            print(Colorate.Horizontal(color, f" [{status}] ") + Colorate.Horizontal(cl["txt"], f"> discord.gift/{code}"))

class Worker():
    def __init__(self, threads, webhook_url, webhook_username, webhook_avatar, use_proxies, proxy_type, proxies_list):
        self.threads = threads
        self.webhook_url = webhook_url
        self.webhook_username = webhook_username
        self.webhook_avatar = webhook_avatar
        self.use_proxies = use_proxies
        self.proxy_type = proxy_type
        self.proxies_list = proxies_list

    def random_proxy(self):
        if self.proxies_list:
            return random.choice(self.proxies_list)
        return None
    
    def run(self):
        cl = Theme.get_colors()
        while True:
            code = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(16))
            try:
                proxies = None
                if self.use_proxies and self.proxies_list:
                    p = self.random_proxy()
                    proxies = {'http': f'{self.proxy_type}://{p}', 'https': f'{self.proxy_type}://{p}'}
                req = requests.get(f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true', proxies=proxies, timeout=3)
                if req.status_code == 200:
                    Console().printer(cl["head"], "Valid  ", code)
                    if not os.path.exists("results"):
                        os.mkdir("results")
                    with open('results/hit.txt', 'a+') as f:
                        f.write(code + "\n")
                    if self.webhook_url:
                        try:
                            payload = {
                                "content": f"||@here|| **__New Valid Nitro !!__**\n\nhttps://discord.gift/{code}"
                            }
                            if self.webhook_username:
                                payload["username"] = self.webhook_username
                            if self.webhook_avatar:
                                payload["avatar_url"] = self.webhook_avatar
                            requests.post(self.webhook_url, json=payload)
                        except:
                            pass
                elif req.status_code == 404:
                    Console().printer(cl["num"], "Invalid", code)
                elif req.status_code == 429:
                    Console().printer(cl["num"], "RTlimit", code)
                else:
                    pass
            except KeyboardInterrupt:
                pass
            except:
                pass

def start_generator(threads=None):
    cl = Theme.get_colors()
    Console().ui()
    if threads is None:
        threads_inpt = get_inpt("Threads (default 200):")
        threads = int(threads_inpt) if threads_inpt.isdigit() else 1
    webhook_url = get_inpt("Webhook URL (Leave empty to skip):")
    webhook_username = ""
    webhook_avatar = ""
    if webhook_url:
        webhook_username = get_inpt("Webhook Username (default: NitroGen):") or "NitroGen"
        webhook_avatar = get_inpt("Webhook Avatar URL (Leave empty to skip):") 
    use_proxies = get_inpt("Use Proxies? (y/n):").lower() == 'y'
    proxy_type = "http"
    proxies_list = []

    if use_proxies:
        proxy_type = get_inpt("Proxy Type (http/socks4/socks5):").lower() or "http"
        print(Colorate.Horizontal(cl["num"], "  [>] Scraping proxies..."))
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        ]
        if proxy_type == "socks4":
            sources = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=yes&anonymity=all",
                       "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"]
        elif proxy_type == "socks5":
            sources = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=yes&anonymity=all",
                       "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"]        
        for url in sources:
            try:
                resp = requests.get(url, timeout=6)
                if resp.status_code == 200:
                    for line in resp.text.split("\n"):
                        if ":" in line: proxies_list.append(line.strip())
            except: pass
        proxies_list = list(set(proxies_list))
        print(Colorate.Horizontal(cl["head"], f"  [+] Loaded {len(proxies_list)} proxies."))

    worker = Worker(threads, webhook_url, webhook_username, webhook_avatar, use_proxies, proxy_type, proxies_list)
    print(Colorate.Horizontal(cl["head"], f"  [+] Starting {threads} threads... (Ctrl+C to stop)"))
    try:
        pool = []
        for _ in range(threads):
            t = threading.Thread(target=worker.run, daemon=True)
            t.start()
            pool.append(t)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Colorate.Horizontal(cl["num"], "\n  [!] Stopped by User."))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter to return..."))
