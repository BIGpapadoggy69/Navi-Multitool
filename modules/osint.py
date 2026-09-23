#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import requests, socket, webbrowser, concurrent.futures, time
from core.display import get_inpt, menu_opts, Colors, Colorate, Theme
from modules.email_lookup import email_lookup_init

def _g(u):
    try:
        r = requests.get(u, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

def whois_lookup(v):
    cl = Theme.get_colors()
    ip = 0
    try: socket.inet_aton(v); ip = 1
    except: pass
    r = {}
    if ip:
        g, n = _g(f"http://ip-api.com/json/{v}?fields=66846719"), _g(f"https://rdap.org/ip/{v}")
        if g and g.get("status") == "success":
            for f in ["country","regionName","city","zip","lat","lon","timezone","isp","org","as","mobile","proxy","hosting"]:
                if g.get(f): r[f.upper()] = g[f]
        if n:
            r["NET_NAME"], r["NET_HANDLE"], r["CIDR"] = n.get("name","N/A"), n.get("handle","N/A"), n.get("parentHandle","N/A")
            for e in n.get("entities", []):
                if "abuse" in e.get("roles", []):
                    for v in e.get("vcardArray", [None, []])[1]:
                        if v[0] == "email": r["ABUSE_EMAIL"] = v[3]
    else:
        d = _g(f"https://rdap.org/domain/{v}")
        if not d: return {"ERR": "Domain not found"}
        r["DOMAIN"] = d.get("handle", v)
        for e in d.get("entities", []):
            rs = e.get("roles", [])
            if "registrar" in rs or "registrant" in rs:
                for vc in e.get("vcardArray", [None, []])[1]:
                    if vc[0] == "fn": r[f"{rs[0].upper()}_NAME"] = vc[3]
                    if vc[0] == "email": r[f"{rs[0].upper()}_MAIL"] = vc[3]
        for ev in d.get("events", []):
            a = ev.get("eventAction")
            if a in ["registration", "expiration", "last changed"]: r[a.replace(" ","_").upper()] = ev.get("eventDate")
    return r

def dns_lookup(t):
    try: return {"IP": socket.gethostbyname(t), "HOST": t}
    except: return {"error": "failed"}

def ip_pinger():
    _cl = Theme.get_colors()
    _h = get_inpt("host:")
    _p = int(get_inpt("port (80):") or 80)
    _b = int(get_inpt("bytes (64):") or 64)
    print(Colorate.Horizontal(_cl["head"], f"\n  [+] Pinging {_h}:{_p}... (CTRL+C)\n"))
    _ts, _sc, _fl, _rs = [], 0, 0, []
    def _png():
        nonlocal _sc, _fl
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _s:
                _s.settimeout(2)
                _st = time.time()
                _s.connect((_h, _p))
                _s.sendall(b'\x00' * _b)
                _ms = (time.time() - _st) * 1000
                _sc += 1; _rs.append(_ms)
                _ls = (_fl / (_sc + _fl)) * 100 if (_sc + _fl) > 0 else 0
                print(Colorate.Horizontal(_cl["head"], f"  [+] Reply: {_ms:.2f}ms | sent={_sc} loss={_ls:.1f}%"))
        except:
            _fl += 1
            print(Colorate.Horizontal(_cl["num"], f"  [!] Timeout: {_h}"))
    try:
        while 1: _png(); time.sleep(0.1)
    except KeyboardInterrupt:
        _tot = _sc + _fl
        _l = (_fl / _tot) * 100 if _tot > 0 else 0
        print("\n" + Colorate.Horizontal(_cl["head"], f"  [=] Stats: sent={_tot} lost={_fl} loss={_l:.1f}%"))
        if _rs:
            print(Colorate.Horizontal(_cl["head"], f"  [=] RTT:   min={min(_rs):.2f}ms  avg={sum(_rs)/len(_rs):.2f}ms  max={max(_rs):.2f}ms"))
    input(Colorate.Horizontal(_cl["head"], "\n  Press Enter..."))
