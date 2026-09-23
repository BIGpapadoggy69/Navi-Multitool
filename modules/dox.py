#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import requests, os, time, random, socket, webbrowser, sys
from core.display import Theme, Colorate, get_inpt, menu_opts

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except:
    os.system("pip install phonenumbers -q")
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
from modules.lookup import NumberInfo

def _wired_p(m, s='?'):
    c = Theme.get_colors()
    return f" {Colorate.Horizontal(c['num'], f'[{s}]')} {Colorate.Horizontal(c['txt'], m)}"


def TokenInfo(tk):
    h = {"Authorization": tk, "Content-Type": "application/json"}
    try:
        u = requests.get('https://discord.com/api/v9/users/@me', headers=h).json()
        un = f"{u.get('username')}#{u.get('discriminator')}"
        dn = u.get("global_name", "N/A")
        id = u.get("id", "N/A")
        av = f"https://cdn.discordapp.com/avatars/{id}/{u.get('avatar')}.png"
        cr = time.ctime(((int(id) >> 22) + 1420070400000) / 1000)
        em = u.get("email", "N/A")
        ph = u.get("phone", "N/A")
        nit = {0:"False",1:"Nitro Classic",2:"Nitro Boosts",3:"Nitro Basic"}.get(u.get("premium_type"), "False")
        mfa = str(u.get("mfa_enabled", "N/A"))
        return un, dn, id, av, cr, em, ph, nit, "N/A", "N/A", mfa
    except: return ("N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A")

def dox_creator():
    cl = Theme.get_colors()
    from core.display import print_banner
    print_banner()
    print(Colorate.Horizontal(cl["head"], "  [ DOX CREATOR ]\n"))
    
    # 1:1 Fields from provided code
    by = get_inpt("doxed_by:")
    reason = get_inpt("reason:")
    p1 = get_inpt("first_pseudo:")
    p2 = get_inpt("second_pseudo:")

    print(Colorate.Horizontal(cl["num"], "\n  [ DISCORD INFO ]"))
    if get_inpt("use_token? (y/n):").lower() == 'y':
        tk = get_inpt("token:")
        un_d, dn_d, id_d, av_d, cr_d, em_d, ph_d, nit_d, fr_d, gc_d, mfa_d = TokenInfo(tk)
    else:
        tk = "None"
        un_d, dn_d, id_d, av_d, cr_d, em_d, ph_d, nit_d, fr_d, gc_d, mfa_d = [get_inpt(f"{x}:") for x in ["username","display","id","avatar","created","email","phone","nitro","friends","gifts","mfa"]]

    print(Colorate.Horizontal(cl["num"], "\n  [ IP INFO ]"))
    ip_pub = get_inpt("public_ip:")
    ip_loc = get_inpt("local_ip:")
    ipv6 = get_inpt("ipv6:")
    vpn = get_inpt("vpn (y/n):")
    
    print(Colorate.Horizontal(cl["num"], "\n  [ PC INFO ]"))
    pc_n = get_inpt("pc_name:")
    pc_un = get_inpt("pc_username:")
    pc_dn = get_inpt("pc_display:")
    pc_plt = get_inpt("platform:")
    pc_os = get_inpt("os:")
    pc_key = get_inpt("win_key:")
    pc_mac = get_inpt("mac:")
    pc_hwid = get_inpt("hwid:")
    pc_cpu = get_inpt("cpu:")
    pc_gpu = get_inpt("gpu:")
    pc_ram = get_inpt("ram:")
    pc_dsk = get_inpt("disk:")

    print(Colorate.Horizontal(cl["num"], "\n  [ PHONE INFO ]"))
    ph_num = get_inpt("number:")
    ph_brd = get_inpt("brand:")
    res = NumberInfo(ph_num)
    if res:
        ph_op, ph_typ, ph_cc, ph_reg, ph_tz = res["Carrier"], res["Type"], res["Region"], res["Location"], res["Timezone"]
    else:
        ph_op, ph_typ, ph_cc, ph_reg, ph_tz = "N/A", "N/A", "N/A", "N/A", "N/A"

    print(Colorate.Horizontal(cl["num"], "\n  [ PERSONAL INFO ]"))
    gender = get_inpt("gender:")
    l_name = get_inpt("last_name:")
    f_name = get_inpt("first_name:")
    age = get_inpt("age:")
    mother = get_inpt("mother:")
    father = get_inpt("father:")
    
    print(Colorate.Horizontal(cl["num"], "\n  [ LOCATION ]"))
    cont = get_inpt("continent:")
    country = get_inpt("country:")
    region = get_inpt("region:")
    zip_c = get_inpt("zip:")
    city = get_inpt("city:")
    addr = get_inpt("address:")

    print(Colorate.Horizontal(cl["num"], "\n  [ SOCIAL & OTHER ]"))
    mail = get_inpt("email:")
    pwd = get_inpt("password:")
    other = get_inpt("other:")
    db = get_inpt("database:")
    logs = get_inpt("logs:")

    name_file = get_inpt("file_name:") or f"dox_{random.randint(1,999)}"
    if not os.path.exists("output/dox"): os.makedirs("output/dox", exist_ok=True)
    path = f"output/dox/{name_file}.txt"

    with open(path, 'w', encoding='utf-8') as file:
        file.write(f'''
    ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                        
            ███╗   ██╗ █████╗ ██╗   ██╗██╗
            ████╗  ██║██╔══██╗██║   ██║██║
            ██╔██╗ ██║███████║██║   ██║██║
            ██║╚██╗██║██╔══██║╚██╗ ██╔╝██║
            ██║ ╚████║██║  ██║ ╚████╔╝ ██║
            ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝
                              
                                                                                   
            Doxed By : {by}
            Reason   : {reason}
            Pseudo   : "{p1}", "{p2}"
    
    ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            DISCORD:
            =====================================================================================
            [+] Username     : {un_d}
            [+] Display Name : {dn_d}
            [+] ID           : {id_d}
            [+] Avatar       : {av_d}
            [+] Created At   : {cr_d}
            [+] Token        : {tk}
            [+] E-Mail       : {em_d}
            [+] Phone        : {ph_d}
            [+] Nitro        : {nit_d}
            [+] Friends      : {fr_d}
            [+] Gift Code    : {gc_d}
            [+] MFA          : {mfa_d}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            INFORMATION:
            =====================================================================================
            +────────────Pc────────────+
            [+] IP Public    : {ip_pub}
            [+] Ip Local     : {ip_loc}
            [+] Ipv6         : {ipv6}
            [+] VPN Y/N      : {vpn}

            [+] Name         : {pc_n}
            [+] Username     : {pc_un}
            [+] Display Name : {pc_dn}

            [+] Plateform    : {pc_plt}
            [+] Exploitation : {pc_os}
            [+] Windows Key  : {pc_key}

            [+] MAC          : {pc_mac}
            [+] HWID         : {pc_hwid}
            [+] CPU          : {pc_cpu}
            [+] GPU          : {pc_gpu}
            [+] RAM          : {pc_ram}
            [+] Disk         : {pc_dsk}

            +───────────Phone──────────+
            [+] Phone Number : {ph_num}
            [+] Brand        : {ph_brd}
            [+] Operator     : {ph_op}
            [+] Type Number  : {ph_typ}
            [+] Country      : {ph_cc}
            [+] Region       : {ph_reg}
            [+] Timezone     : {ph_tz}

            +───────────Personal───────+
            [+] Gender      : {gender}
            [+] Last Name   : {l_name}
            [+] First Name  : {f_name}
            [+] Age         : {age}
            [+] Mother      : {mother}
            [+] Father      : {father}

            +────────────Loc───────────+
            [+] Continent   : {cont}
            [+] Country     : {country}
            [+] Region      : {region}
            [+] Postal Code : {zip_c}
            [+] City        : {city}
            [+] Address     : {addr}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            SOCIAL:
            =====================================================================================
            [+] Email    : {mail}
            [+] Password : {pwd}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            OTHER:
            =====================================================================================
            {other}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            DATABASE:
            =====================================================================================
            {db}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            LOGS:
            =====================================================================================
            {logs}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝
    ''')
    
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Dox created: {path}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def dox_tracker():
    cl = Theme.get_colors()
    from core.display import print_banner
    print_banner()
    print(Colorate.Horizontal(cl["head"], "  [ DOX TRACKER ]\n"))
    while 1:
        menu_opts({"1": "Username Checker", "2": "Name Search", "99": "Go Back"})
        t = get_inpt("navi@dox:~#")
        if t == '99': break
        if t == '1':
            u = get_inpt("username:")
            print(Colorate.Horizontal(cl["head"], f"\n  [+] Checking '{u}'...\n"))
            s = requests.Session()
            s.headers.update({"User-Agent": "Mozilla/5.0"})
            st = {
                "GitHub":f"https://github.com/{u}","YouTube":f"https://www.youtube.com/@{u}","TikTok":f"https://www.tiktok.com/@{u}","Twitter":f"https://twitter.com/{u}","Instagram":f"https://instagram.com/{u}","Facebook":f"https://www.facebook.com/{u}","Reddit":f"https://www.reddit.com/user/{u}","Pinterest":f"https://www.pinterest.com/{u}","Tumblr":f"https://{u}.tumblr.com","Twitch":f"https://www.twitch.tv/{u}","Steam":f"https://steamcommunity.com/id/{u}","SoundCloud":f"https://soundcloud.com/{u}","Telegram":f"https://t.me/{u}","Snapchat":f"https://www.snapchat.com/add/{u}","DeviantArt":f"https://www.deviantart.com/{u}","Medium":f"https://medium.com/@{u}","Quora":f"https://www.quora.com/profile/{u}","Vimeo":f"https://vimeo.com/{u}"
            }
            for n, l in st.items():
                try:
                    r = s.get(l, timeout=6)
                    if r.status_code == 200:
                        print(Colorate.Horizontal(cl["head"], f"  [+] FOUND: {n:<12} => {l}"))
                    else:
                        print(Colorate.Horizontal(cl["num"], f"  [-] MISSING: {n:<12}"))
                except:
                    print(Colorate.Horizontal(cl["num"], f"  [!] ERROR: {n:<12}"))
            input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
        elif t == '2':
            ln, fn = get_inpt("last_name:"), get_inpt("first_name:")
            q = f"{ln} {fn}".replace(" ", "%20")
            print(Colorate.Horizontal(cl["head"], "\n  [+] Searching..."))
            for u in [f"https://www.facebook.com/search/top/?q={q}", f"https://www.peekyou.com/{ln}_{fn}"]:
                try: webbrowser.open(u)
                except: pass
            input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))