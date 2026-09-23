#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import os, sys, time, json, hashlib, re, zlib, base64, stat, struct
from core.display import Colorate, Theme, get_inpt, print_banner

try: import piexif
except: piexif = None

try: import exifread
except: exifread = None

try: from PIL import Image
except: Image = None

try: import mutagen
except: mutagen = None

DUMP_DIR = "output/metadata_dumps"

def detect_type(p):
    try:
        with open(p, "rb") as f: h = f.read(64)
    except: return "error"

    if h.startswith(b"\xFF\xD8\xFF"): return "image/jpeg"
    if h.startswith(b"\x89PNG\r\n\x1a\n"): return "image/png"
    if h.startswith(b"GIF87a") or h.startswith(b"GIF89a"): return "image/gif"
    if h.startswith(b"BM"): return "image/bmp"
    if h.startswith(b"%PDF"): return "application/pdf"
    
    if h.startswith(b"ID3") or h[:2] in (b"\xFF\xFB", b"\xFF\xF3"): return "audio/mpeg"
    if h.startswith(b"fLaC"): return "audio/flac"
    if h.startswith(b"RIFF") and h[8:12] == b"WAVE": return "audio/wav"
    
    return "unknown/binary"

def clean_val(v):
    if v is None: return "N/A"
    if isinstance(v, bytes):
        try: return v.decode("utf-8", "ignore")
        except: return str(v)
    if isinstance(v, (list, tuple)): return [clean_val(i) for i in v]
    if isinstance(v, dict): return {str(k): clean_val(i) for k, i in v.items()}
    return str(v)

def get_hashes(p):
    m, s1, s2 = hashlib.md5(), hashlib.sha1(), hashlib.sha256()
    try:
        with open(p, "rb") as f:
            while True:
                b = f.read(8192)
                if not b: break
                m.update(b); s1.update(b); s2.update(b)
        return {"MD5": m.hexdigest(), "SHA1": s1.hexdigest(), "SHA256": s2.hexdigest()}
    except: return {}

def extract_embedded(p):
    res = []
    try:
        with open(p, "rb") as f: data = f.read()
        sigs = [(b"\xff\xd8\xff", "jpg"), (b"\x89PNG\r\n\x1a\n", "png"), (b"%PDF", "pdf")]
        for i, (sig, ext) in enumerate(sigs):
            found = data.find(sig)
            if found != -1:
                if not os.path.exists(DUMP_DIR): os.makedirs(DUMP_DIR)
                out = os.path.join(DUMP_DIR, f"extracted_{i}.{ext}")
                with open(out, "wb") as f2: f2.write(data[found:found+1000000]) 
                res.append(out)
    except: pass
    return res

def scan_file(p):
    cl = Theme.get_colors()
    if not os.path.exists(p):
        print(Colorate.Horizontal(cl["num"], "  [!] File not found."))
        return
    print(Colorate.Horizontal(cl["head"], f"  [+] Scanning: {os.path.basename(p)}..."))
    time.sleep(0.5)
    info = {}
    s = os.stat(p)
    info["Basic"] = {
        "Size": f"{s.st_size} bytes",
        "Created": time.ctime(s.st_ctime),
        "Modified": time.ctime(s.st_mtime)
    }

    ft = detect_type(p)
    info["Type"] = ft
    info["Hashes"] = get_hashes(p)

    if ft.startswith("image") and Image:
        try:
            with Image.open(p) as img:
                info["Image"] = {
                    "Format": img.format,
                    "Size": f"{img.width}x{img.height}",
                    "Mode": img.mode
                }
        except: pass
    if piexif and ft == "image/jpeg":
        try:
            ex = piexif.load(p)
            info["EXIF"] = {}
            for ifd in ("0th", "Exif", "GPS", "1st"):
                for tag, val in ex.get(ifd, {}).items():
                    name = piexif.TAGS.get(ifd, {}).get(tag, {}).get("name", tag)
                    info["EXIF"][name] = clean_val(val)
        except: pass
    if mutagen and ft.startswith("audio"):
        try:
            a = mutagen.File(p)
            if a: info["Audio"] = clean_val(dict(a))
        except: pass
    print(Colorate.Horizontal(cl["head"], "\n  [ RESULTS ]"))
    for cat, data in info.items():
        print(Colorate.Horizontal(cl["num"], f"  --- {cat} ---"))
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict): v = "..."
                print(Colorate.Horizontal(cl["num"], f"    {k}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        else:
            print(Colorate.Horizontal(cl["txt"], f"    {data}"))
    emb = extract_embedded(p)
    if emb:
        print(Colorate.Horizontal(cl["head"], f"\n  [!] Dumped {len(emb)} possible embedded files to {DUMP_DIR}"))
    if get_inpt("Save report to JSON? (y/n):").lower() == "y":
        out_json = f"output/report_{int(time.time())}.json"
        if not os.path.exists("output"): os.mkdir("output")
        with open(out_json, "w") as f: json.dump(info, f, indent=4)
        print(Colorate.Horizontal(cl["head"], f"  [>] Saved to {out_json}"))

def metadata_init():
    while True:
        print_banner()
        cl = Theme.get_colors()
        print(Colorate.Horizontal(cl["head"], "  [ FILE METADATA SCANNER ]\n"))
        path = get_inpt("path (or '99' to exit):")
        if path == "99": break
        path = path.replace('"', '').replace("'", "").strip()
        scan_file(path)
        input(Colorate.Horizontal(cl["head"], "\n  Press Enter to continue..."))
