#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import time
import os
import requests
import threading
from core.display import Theme, Colorate, get_inpt, print_banner

def scrape_proxies_menu():
    cl = Theme.get_colors()
    print_banner()
    print(Colorate.Horizontal(cl["head"], "  [ PROXY SCRAPER ]\n"))
    print(Colorate.Horizontal(cl["num"], "  [1] ") + Colorate.Horizontal(cl["txt"], "Scrape HTTP Proxies"))
    print(Colorate.Horizontal(cl["num"], "  [2] ") + Colorate.Horizontal(cl["txt"], "Scrape SOCKS4 Proxies"))
    print(Colorate.Horizontal(cl["num"], "  [3] ") + Colorate.Horizontal(cl["txt"], "Scrape SOCKS5 Proxies"))
    print(Colorate.Horizontal(cl["num"], "  [4] ") + Colorate.Horizontal(cl["txt"], "Scrape All (HTTP, SOCKS4, SOCKS5)"))
    print(Colorate.Horizontal(cl["num"], "  [5] ") + Colorate.Horizontal(cl["txt"], "Return"))
    
    choice = get_inpt("navi@proxyscraper:~# ").strip()
    
    if choice == "5":
        return
        
    protocols = []
    if choice == "1":
        protocols = ["http"]
    elif choice == "2":
        protocols = ["socks4"]
    elif choice == "3":
        protocols = ["socks5"]
    elif choice == "4":
        protocols = ["http", "socks4", "socks5"]
    else:
        print(Colorate.Horizontal(cl["num"], "  [!] Invalid Option."))
        time.sleep(1.2)
        return
        
    print(Colorate.Horizontal(cl["txt"], "\n  Save with protocol prefix? (example: http://1.2.3.4:80)"))
    prefix_choice = get_inpt("  (y/n): ").strip().lower() == "y"
    
    print(Colorate.Horizontal(cl["num"], "\n  [>] Scraper initialized. Fetching lists..."))
    
    sources = {
        "http": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/clketc/Free-Proxy-List/main/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/OfficialPutu/free-proxy/main/http.txt",
            "https://raw.githubusercontent.com/saisuiu/Free-Proxy-List/main/http.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt"
        ],
        "socks4": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=yes&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/clketc/Free-Proxy-List/main/socks4.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/OfficialPutu/free-proxy/main/socks4.txt",
            "https://raw.githubusercontent.com/saisuiu/Free-Proxy-List/main/socks4.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt"
        ],
        "socks5": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=yes&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/socks5.txt",
            "https://raw.githubusercontent.com/clketc/Free-Proxy-List/main/socks5.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/OfficialPutu/free-proxy/main/socks5.txt",
            "https://raw.githubusercontent.com/saisuiu/Free-Proxy-List/main/socks5.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt"
        ]
    }
    
    scraped_proxies = []
    scraped_lock = threading.Lock()
    
    def fetch_source(proto, url):
        try:
            resp = requests.get(url, timeout=8)
            if resp.status_code == 200:
                count = 0
                for line in resp.text.split("\n"):
                    line = line.strip()
                    if ":" in line and not line.startswith("#"):
                        for prefix in ["http://", "https://", "socks4://", "socks5://"]:
                            if line.lower().startswith(prefix):
                                line = line[len(prefix):]
                        
                        formatted = f"{proto}://{line}" if prefix_choice else line
                        with scraped_lock:
                            scraped_proxies.append(formatted)
                            count += 1
                print(Colorate.Horizontal(cl["head"], f"  [+] Fetched {count} proxies from: ") + Colorate.Horizontal(cl["txt"], url[:60] + "..."))
        except:
            pass

    threads = []
    for proto in protocols:
        for url in sources[proto]:
            t = threading.Thread(target=fetch_source, args=(proto, url))
            t.start()
            threads.append(t)
            
    for t in threads:
        t.join()
        
    unique_proxies = list(set(scraped_proxies))
    
    output_dir = "input"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file = os.path.join(output_dir, "proxies.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for p in unique_proxies:
            f.write(p + "\n")
            
    print(Colorate.Horizontal(cl["head"], f"\n  [=] Scraping Completed!"))
    print(Colorate.Horizontal(cl["head"], f"  [+] Scraped: {len(scraped_proxies)} total, {len(unique_proxies)} unique."))
    print(Colorate.Horizontal(cl["txt"], f"  [+] Saved to {output_file}"))
    
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
