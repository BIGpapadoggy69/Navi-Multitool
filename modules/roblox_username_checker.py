import asyncio
import aiohttp
import random
import string
import time
import os
from urllib.parse import quote
from core.display import Theme, Colorate, clr, get_inpt

SHIT_NIGGA_API = "https://auth.roblox.com/v1/usernames/validate?username={}&birthday=2000-01-01"
USERAGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]

def load_file(filepath):
    if not os.path.exists(filepath): return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]
def parse_proxy(proxy_str):
    proxy_str = proxy_str.strip()
    if not proxy_str: return None
    if proxy_str.startswith("http://") or proxy_str.startswith("https://"):
        return proxy_str
    parts = proxy_str.split(":")
    if len(parts) == 2:
        return f"http://{parts[0]}:{parts[1]}"
    elif len(parts) == 4:
        ip, port, user, password = parts
        return f"http://{user}:{password}@{ip}:{port}"
    return None
async def check_one(session, username, proxy_url, sem, stats, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            async with sem:
                ua = random.choice(USERAGENTS)
                headers = {
                    "User-Agent": ua,
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Referer": "https://www.roblox.com/",
                    "Origin": "https://www.roblox.com",
                    "Connection": "keep-alive",
                }
                url = SHIT_NIGGA_API.format(quote(username))
                async with session.get(
                    url,
                    headers=headers,
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    status_code = resp.status
                    if status_code == 429:
                        stats["rate_limited"] += 1
                        return (username, None, "rate_limited", "")
                    if 400 <= status_code < 500 and status_code != 429:
                        stats["errors"] += 1
                        return (username, None, f"http_{status_code}", "")
                    if status_code >= 500:
                        if attempt < max_retries:
                            await asyncio.sleep(0.5 * attempt)
                            continue
                        else:
                            stats["errors"] += 1
                            return (username, None, f"http_{status_code}", "")
                    data = await resp.json()
                    if not isinstance(data, dict):
                        if attempt < max_retries:
                            await asyncio.sleep(0.3)
                            continue
                        stats["errors"] += 1
                        return (username, None, "non_dict", "")
                    code = data.get("code")
                    msg = data.get("message", "")
                    if code == 0:
                        stats["available"] += 1
                        return (username, True, "available", msg)
                    if code == 1:
                        stats["taken"] += 1
                        return (username, False, "taken", msg)
                    if code == 2:
                        stats["taken"] += 1
                        return (username, False, "inappropriate", msg)
                    if code == 4:
                        stats["invalid"] += 1
                        return (username, None, "invalid", msg)
                    if code == 10:
                        stats["invalid"] += 1
                        return (username, None, "private_info", msg)
                    if attempt < max_retries:
                        await asyncio.sleep(0.3)
                        continue
                    stats["unknown"] += 1
                    return (username, None, f"code_{code}", msg)
        except asyncio.TimeoutError:
            if attempt < max_retries:
                await asyncio.sleep(0.5 * attempt)
                continue
            stats["errors"] += 1
            return (username, None, "timeout", "")
        except Exception as e:
            err_name = type(e).__name__
            if attempt < max_retries:
                await asyncio.sleep(0.3 * attempt)
                continue
            stats["errors"] += 1
            return (username, None, err_name, str(e))
    stats["errors"] += 1
    return (username, None, "unknown", "")
async def run_batch(usernames, concurrency, proxies, cl):
    sem = asyncio.Semaphore(concurrency)
    stats = {"available": 0, "taken": 0, "unknown": 0, "errors": 0,
             "rate_limited": 0, "invalid": 0}

    def get_proxy():
        if not proxies: return None
        return random.choice(proxies)

    connector = aiohttp.TCPConnector(
        limit=concurrency * 2,
        limit_per_host=concurrency,
        force_close=False,
        enable_cleanup_closed=True,
    )
    total = len(usernames)
    start_time = time.time()
    completed = 0
    available_list = []
    if not os.path.exists("output"):
        os.makedirs("output")
    out_file = "output/roblox_available.txt"
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = {}
        for u in usernames:
            task = asyncio.create_task(
                check_one(session, u, get_proxy(), sem, stats)
            )
            tasks[task] = u
        pending = set(tasks.keys())
        while pending:
            done, pending = await asyncio.wait(
                pending,
                timeout=30,
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                username, result, status, message = task.result()
                completed += 1
                elapsed = time.time() - start_time
                rate = completed / elapsed if elapsed > 0 else 0
                remaining = total - completed
                eta = remaining / rate if rate > 0 else 0
                if result is True:
                    available_list.append(username)
                    with open(out_file, "a", encoding="utf-8") as f:
                        f.write(username + "\n")
                    print(Colorate.Horizontal(cl["head"], f"  [+] Available: {username} [{completed}/{total} | {rate:.0f}/s | ETA {eta:.0f}s]"), flush=True)
                elif result is False:
                    print(Colorate.Horizontal(cl["txt"], f"  [-] Taken: {username} [{completed}/{total} | {rate:.0f}/s | ETA {eta:.0f}s]"), flush=True)
                else:
                    if status == "rate_limited":
                        print(Colorate.Horizontal(cl["num"], f"  [!] Rate limited for: {username}"), flush=True)
                    else:
                        print(Colorate.Horizontal(cl["num"], f"  [?] Invalid/Error: {username} ({status}) [{completed}/{total} | {rate:.0f}/s]"), flush=True)
            if not done and pending:
                for t in pending: t.cancel()
                break
        for t in pending:
            t.cancel()
            try: await t
            except: pass
    end_time = time.time()
    total_elapsed = end_time - start_time
    overall_rate = total / total_elapsed if total_elapsed > 0 else 0
    return stats, total_elapsed, overall_rate, available_list

def main():
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    cl = Theme.get_colors() # navi themes are just so goated
    while True:
        clr()
        print(Colorate.Horizontal(cl["head"], "  [ ROBLOX USERNAME CHECKER ]\n"))
        print(Colorate.Horizontal(cl["num"], "  [1] ") + Colorate.Horizontal(cl["txt"], "Generate Usernames"))
        print(Colorate.Horizontal(cl["num"], "  [2] ") + Colorate.Horizontal(cl["txt"], "Check Usernames"))
        print(Colorate.Horizontal(cl["num"], "  [3] ") + Colorate.Horizontal(cl["txt"], "Return"))
        choice = get_inpt("navi@roblox_checker:~# ").strip()
        if choice == "1":
            print(Colorate.Horizontal(cl["num"], "  Which kind of usernames to generate? [5L, 5C, 4L, 4C, 3L, 3C]"))
            username_type = get_inpt("  > ").strip().upper()
            print(Colorate.Horizontal(cl["num"], "  Allow underscores (_)? [y/n]"))
            allow_special = get_inpt("  > ").strip().lower() == "y"
            letters = string.ascii_lowercase
            chars = string.ascii_lowercase + string.digits
            if allow_special:
                chars += "_"
            if username_type == "5L":
                length = 5
                chars = letters + ("_" if allow_special else "")
            elif username_type == "5C":
                length = 5
            elif username_type == "4L":
                length = 4
                chars = letters + ("_" if allow_special else "")
            elif username_type == "4C":
                length = 4
            elif username_type == "3L":
                length = 3
                chars = letters + ("_" if allow_special else "")
            elif username_type == "3C":
                length = 3
            else:
                print(Colorate.Horizontal(cl["num"], "  Invalid option."))
                get_inpt("  Press Enter...")
                continue
            amount_str = get_inpt("  Amount of usernames (default 50000): ")
            amount = int(amount_str) if amount_str.isdigit() else 50000
            max_possible = len(chars) ** length
            if amount > max_possible:
                amount = max_possible
            output_file = "input/roblox_usernames.txt"
            if not os.path.exists("input"):
                os.makedirs("input")  
            usernames = set()
            failed_attempts = 0
            while len(usernames) < amount and failed_attempts < 100000:
                name = "".join(random.choices(chars, k=length))
                valid = True
                if name.startswith("_") or name.endswith("_"): valid = False
                if "__" in name: valid = False
                if valid:
                    before = len(usernames)
                    usernames.add(name)
                    if len(usernames) == before:
                        failed_attempts += 1
                    else:
                        failed_attempts = 0
                else:
                    failed_attempts += 1

            with open(output_file, "w", encoding="utf-8") as f:
                username_list = list(usernames)
                random.shuffle(username_list)
                for username in username_list:
                    f.write(username + "\n")
            print(Colorate.Horizontal(cl["head"], f"  {len(usernames)} valid Roblox usernames saved to '{output_file}'."))
            get_inpt("  Press Enter...")
        elif choice == "2":
            usernames_file = "input/roblox_usernames.txt"
            proxies_file = "input/proxies.txt"
            concurrency_str = get_inpt("  Concurrency (default 50): ")
            concurrency = int(concurrency_str) if concurrency_str.isdigit() else 50
            usernames = load_file(usernames_file)
            proxies_raw = load_file(proxies_file)
            if not usernames:
                print(Colorate.Horizontal(cl["num"], f"  [!] No usernames found in {usernames_file}."))
                get_inpt("  Press Enter...")
                continue
            use_proxies_input = get_inpt("  Use proxies? (y/n): ").strip().lower()
            use_proxies = (use_proxies_input == 'y')
            if use_proxies:
                proxies = [p for p in (parse_proxy(x) for x in proxies_raw) if p]
                if not proxies:
                    print(Colorate.Horizontal(cl["num"], f"  [!] Proxies not found in {proxies_file}. Running proxyless (high chance of rate limit)."))
                    use_proxies = False
                else:
                    print(Colorate.Horizontal(cl["head"], f"  [+] Loaded {len(proxies)} proxies."))
            else:
                print(Colorate.Horizontal(cl["head"], "  [*] Proxyless mode selected."))
                proxies = []
            print(Colorate.Horizontal(cl["txt"], f"  Usernames: {len(usernames)}"))
            print(Colorate.Horizontal(cl["txt"], f"  Concurrency: {concurrency}\n"))
            print(Colorate.Horizontal(cl["txt"], "  [>] Starting checks..."))
            stats, total_elapsed, overall_rate, available_list = asyncio.run(
                run_batch(usernames, concurrency, proxies if use_proxies else [], cl)
            )
            print(Colorate.Horizontal(cl["head"], "\n  [=] Checker Finished"))
            print(Colorate.Horizontal(cl["txt"], f"  Completed in {total_elapsed:.1f}s ({overall_rate:.0f}/s)"))
            print(Colorate.Horizontal(cl["txt"], f"  Available: {stats['available']} | Taken: {stats['taken']} | "
                  f"Invalid: {stats['invalid']} | Errors: {stats['errors']} | Rate-limited: {stats['rate_limited']}"))
            if available_list:
                print(Colorate.Horizontal(cl["txt"], "  Saved to output/roblox_available.txt"))    
            get_inpt("  Press Enter...")
        elif choice == "3":
            break

if __name__ == "__main__": # if main = name = true start: roblox chegger
    main()