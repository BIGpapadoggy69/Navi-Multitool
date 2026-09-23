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
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.display import Theme, Colorate, get_inpt, print_banner

def check_proxy(proxy, url, timeout, print_lock, cl, results):
    clean_proxy = proxy.strip()
    scheme = "http"
    
    for s in ["http://", "https://", "socks4://", "socks5://"]:
        if clean_proxy.lower().startswith(s):
            scheme = s[:-3]
            clean_proxy = clean_proxy[len(s):]
            break
            
    parts = clean_proxy.split(":")
    if len(parts) == 4:
        if parts[1].isdigit():
            ip, port, user, password = parts
        else:
            user, password, ip, port = parts
        clean_proxy = f"{user}:{password}@{ip}:{port}"
        
    proxy_url = f"{scheme}://{clean_proxy}"
    proxies_dict = {"http": proxy_url, "https": proxy_url}
    
    try:
        start_time = time.time()
        resp = requests.get(url, proxies=proxies_dict, timeout=timeout, stream=True)
        elapsed = int((time.time() - start_time) * 1000)
        if 200 <= resp.status_code < 500:
            with print_lock:
                print(Colorate.Horizontal(cl["head"], f"  [+] Working: {proxy} ({elapsed}ms)"))
            results.append(proxy)
            return True
        else:
            with print_lock:
                print(Colorate.Horizontal(cl["num"], f"  [-] Failed ({resp.status_code}): {proxy}"))
            return False
    except Exception:
        with print_lock:
            print(Colorate.Horizontal(cl["num"], f"  [-] Bad: {proxy}"))
        return False

def proxy_checker_menu():
    cl = Theme.get_colors()
    print_banner()
    print(Colorate.Horizontal(cl["head"], "  [ PROXY CHECKER ]\n"))
    
    proxies_file = "input/proxies.txt"
    if not os.path.exists(proxies_file):
        print(Colorate.Horizontal(cl["num"], f"  [!] proxies.txt not found in {proxies_file}."))
        get_inpt("  Press Enter...")
        return
        
    with open(proxies_file, "r", encoding="utf-8") as f:
        proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
    if not proxies:
        print(Colorate.Horizontal(cl["num"], f"  [!] No proxies found in {proxies_file}."))
        get_inpt("  Press Enter...")
        return
        
    print(Colorate.Horizontal(cl["head"], f"  [+] Loaded {len(proxies)} proxies from {proxies_file}."))
    
    url = get_inpt("URL to test (default https://discord.com/api/v9/experiments): ").strip() or "https://discord.com/api/v9/experiments"
    
    timeout_inpt = get_inpt("Timeout in seconds (default 3): ").strip()
    try:
        timeout = float(timeout_inpt) if timeout_inpt else 3.0
    except ValueError:
        timeout = 3.0
        
    threads_inpt = get_inpt("Threads (default 50): ").strip()
    try:
        threads = int(threads_inpt) if threads_inpt else 50
    except ValueError:
        threads = 50
        
    print(Colorate.Horizontal(cl["head"], f"\n  [>] Checking {len(proxies)} proxies against {url}...\n"))
    
    print_lock = threading.Lock()
    working_proxies = []
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_proxy, p, url, timeout, print_lock, cl, working_proxies) for p in proxies]
        for fut in as_completed(futures):
            try:
                fut.result()
            except:
                pass
                
    elapsed = (time.time() - start_time) / 60
    
    print(Colorate.Horizontal(cl["head"], f"\n  [=] Checker Finished!"))
    print(Colorate.Horizontal(cl["head"], f"  [+] Working: {len(working_proxies)} / {len(proxies)}"))
    print(Colorate.Horizontal(cl["txt"], f"  [+] Elapsed: {elapsed:.2f}m"))
    
    if working_proxies:
        if not os.path.exists("output"):
            os.makedirs("output")
        output_file = "output/working_proxies.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(working_proxies) + "\n")
        print(Colorate.Horizontal(cl["txt"], f"  [+] Saved working proxies to {output_file}"))
        
        overwrite_choice = get_inpt("  Replace input/proxies.txt with working proxies? (y/n): ").strip().lower() == "y"
        if overwrite_choice:
            with open(proxies_file, "w", encoding="utf-8") as f:
                f.write("\n".join(working_proxies) + "\n")
            print(Colorate.Horizontal(cl["head"], f"  [+] input/proxies.txt has been updated!"))
            
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
