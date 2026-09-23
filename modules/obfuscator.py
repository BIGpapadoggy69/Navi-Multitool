#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import zlib, base64, marshal, time, os, tkinter as tk; from tkinter import filedialog; from core.display import Theme, Colorate, get_inpt, print_banner

def _0x1(t): _cl = Theme.get_colors(); print(Colorate.Horizontal(_cl["num"], "  [*] ") + Colorate.Horizontal(_cl["txt"], t))
def _0x2(t): _cl = Theme.get_colors(); print(Colorate.Horizontal(_cl["num"], "  [!] ") + Colorate.Horizontal(_cl["head"], t))

def _0x3(c):
    _0x1("compiling bytecode..."); time.sleep(0.3)
    _0x9 = compile(c, '', 'exec')
    _0x8 = marshal.dumps(_0x9)
    _0x1("layers initializing..."); time.sleep(0.4)
    _0x0 = lambda x: "".join([chr(ord(i)^0x7) for i in x])
    _z = getattr(zlib, 'compress')(_0x8)
    _b = getattr(base64, 'b64encode')(_z).decode()
    _r = _b[::-1]
    _x = _0x0(_r)
    _h = _x.encode().hex()
    
    _l = "m=__import__('marshal');z=__import__('zlib');b=__import__('base64');"
    _e = "exec(m.loads(z.decompress(b.b64decode(''.join([chr(ord(i)^0x7) for i in bytes.fromhex('"+_h+"').decode()[::-1]])))))"
    return "'''\n~ OBFUSCATED BY NAVI ~\n'''\n" + _l + _e

def obfuscator_init():
    _cl = Theme.get_colors(); print_banner(); print(Colorate.Horizontal(_cl["head"], "  [ PYTHON OBFUSCATOR ]\n"))
    _0x1("waiting for file selection..."); _rt = tk.Tk(); _rt.withdraw(); _rt.attributes("-topmost", True)
    _f = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")]); _rt.destroy()
    if not _f: _0x2("no file selected."); time.sleep(1.2); return
    try:
        if not os.path.exists("output"): os.makedirs("output")
        with open(_f, 'r', encoding='utf-8', errors='ignore') as _h: _c = _h.read()
        _o = _0x3(_c); _on = os.path.join("output", os.path.basename(_f).replace(".py", "-obf.py"))
        with open(_on, 'w', encoding='utf-8', errors='ignore') as _h: _h.write(_o)
        _0x1(f"finished: {os.path.basename(_on)}"); os.startfile("output")
    except Exception as _e: _0x2(f"error: {str(_e)}")
    input(Colorate.Horizontal(_cl["head"], "\n  Press Enter..."))
