#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import socket, threading, requests, os
from core.display import Colors, Colorate, get_inpt, Theme

def _hp(ip, p, r, i):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((ip, p)) == 0: r[i] = p
        s.close()
    except: pass

def do_port_check(ip):
    o, ts = [None] * 1025, []
    for x in range(1, 1025):
        t = threading.Thread(target=_hp, args=(ip, x, o, x))
        ts.append(t); t.start()
    [t.join() for t in ts]
    return [x for x in o if x is not None]

def clone_website(url):
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], f"  [*] Cloning {url} (Structured)..."))
    try:
        from bs4 import BeautifulSoup
        if not url.startswith("http"): url = "https://" + url
        _base = "/".join(url.split("/")[:3])
        _hdrs = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }
        r = requests.get(url, timeout=10, headers=_hdrs)
        if r.status_code != 200: 
            print(Colorate.Horizontal(cl["num"], f"  [!] Status: {r.status_code}"))
        else:
            _f = url.split("//")[-1].replace("/", "_").replace(".", "_")
            _dir = os.path.join("output", f"clone_{_f}")
            for d in ["css", "js", "img"]:
                os.makedirs(os.path.join(_dir, d), exist_ok=True)
            
            _soup = BeautifulSoup(r.text, "html.parser")
            _maps = {"img": ("src", "img"), "link": ("href", "css"), "script": ("src", "js")}
            
            for tag, (attr, folder) in _maps.items():
                for el in _soup.find_all(tag):
                    val = el.get(attr)
                    if val:
                        if val.startswith("//"): src = "https:" + val
                        elif val.startswith("/"): src = _base + val
                        elif not val.startswith("http"): src = url + "/" + val
                        else: src = val
                        
                        try:
                            name = src.split("/")[-1].split("?")[0]
                            if not name: continue
                            if folder == "css" and not name.endswith(".css"): continue
                            
                            res = requests.get(src, timeout=5)
                            path = os.path.join(folder, name)
                            with open(os.path.join(_dir, path), "wb") as f: f.write(res.content)
                            el[attr] = path
                        except: pass
            
            with open(os.path.join(_dir, "index.html"), "w", encoding="utf-8") as f: f.write(_soup.prettify())
            print(Colorate.Horizontal(cl["head"], f"  [+] Success! Folder: {_dir}"))
    except Exception as e: print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
