#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import asyncio
import os
import sys
import time
import random
import hashlib
import hmac
from datetime import datetime
from pystyle import Colors as _PY
from Crypto.Hash import keccak, RIPEMD160

class BIP32:
    P = 2**256 - 2**32 - 977
    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    G = (Gx, Gy)

    @classmethod
    def _inv(cls, a, n):
        if a == 0:
            return 0
        lm, hm = 1, 0
        low, high = a % n, n
        while low > 1:
            r = high // low
            nm, new = hm - r * lm, high - r * low
            lm, low, hm, high = nm, new, lm, low
        return lm % n

    @classmethod
    def _ec_add(cls, p, q):
        if not p: return q
        if not q: return p
        (px, py), (qx, qy) = p, q
        if px == qx and py == qy:
            s = ((3 * px * px) * cls._inv(2 * py, cls.P)) % cls.P
        else:
            if px == qx: return None
            s = ((qy - py) * cls._inv(qx - px, cls.P)) % cls.P
        rx = (s * s - px - qx) % cls.P
        ry = (s * (px - rx) - py) % cls.P
        return (rx, ry)

    @classmethod
    def _ec_mul(cls, k, p):
        res = None
        addend = p
        while k:
            if k & 1:
                res = cls._ec_add(res, addend)
            addend = cls._ec_add(addend, addend)
            k >>= 1
        return res

    @classmethod
    def privkey_to_pubkey(cls, privkey_bytes, compressed=True):
        k = int.from_bytes(privkey_bytes, 'big')
        pt = cls._ec_mul(k, cls.G)
        if pt is None:
            raise ValueError("Invalid private key")
        x, y = pt
        if compressed:
            prefix = b'\x02' if y % 2 == 0 else b'\x03'
            return prefix + x.to_bytes(32, 'big')
        else:
            return b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

    @classmethod
    def from_seed(cls, seed):
        I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
        return cls(I[:32], I[32:])

    def __init__(self, private_key, chain_code):
        self.private_key = private_key
        self.chain_code = chain_code

    def child(self, index):
        is_hardened = (index & 0x80000000) != 0
        if is_hardened:
            data = b'\x00' + self.private_key + index.to_bytes(4, 'big')
        else:
            pubkey = self.privkey_to_pubkey(self.private_key, compressed=True)
            data = pubkey + index.to_bytes(4, 'big')

        I = hmac.new(self.chain_code, data, hashlib.sha512).digest()
        Il, Ir = I[:32], I[32:]

        k_par = int.from_bytes(self.private_key, 'big')
        il_int = int.from_bytes(Il, 'big')
        if il_int >= self.N:
            raise ValueError("Invalid child key")
        child_k = (il_int + k_par) % self.N
        if child_k == 0:
            raise ValueError("Invalid child key")

        return BIP32(child_k.to_bytes(32, 'big'), Ir)

    def derive_path(self, path):
        parts = path.split('/')
        if parts[0] != 'm':
            raise ValueError("Path must start with 'm'")
        curr = self
        for part in parts[1:]:
            if part.endswith("'"):
                index = int(part[:-1]) | 0x80000000
            else:
                index = int(part)
            curr = curr.child(index)
        return curr

def base58_encode(b):
    chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(b, 'big')
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(chars[r])
    pad = 0
    for c in b:
        if c == 0:
            pad += 1
        else:
            break
    return (chars[0] * pad) + "".join(reversed(res))

def base58_check_encode(version_byte, payload):
    data = version_byte + payload
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    return base58_encode(data + checksum)

def ripemd160_hash(data):
    r = RIPEMD160.new()
    r.update(data)
    return r.digest()

def keccak256_hash(data):
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

def eth_address(privkey):
    pubkey = BIP32.privkey_to_pubkey(privkey, compressed=False)[1:]
    khash = keccak256_hash(pubkey)
    addr_hex = khash[-20:].hex()
    
    addr_hex = addr_hex.lower()
    k = keccak.new(digest_bits=256)
    k.update(addr_hex.encode('ascii'))
    ahash = k.hexdigest()
    checksum_addr = ""
    for i in range(40):
        if int(ahash[i], 16) >= 8:
            checksum_addr += addr_hex[i].upper()
        else:
            checksum_addr += addr_hex[i]
    return "0x" + checksum_addr

def btc_address(privkey):
    pubkey = BIP32.privkey_to_pubkey(privkey, compressed=True)
    sha = hashlib.sha256(pubkey).digest()
    pkhash = ripemd160_hash(sha)
    return base58_check_encode(b'\x00', pkhash)

def ltc_address(privkey):
    pubkey = BIP32.privkey_to_pubkey(privkey, compressed=True)
    sha = hashlib.sha256(pubkey).digest()
    pkhash = ripemd160_hash(sha)
    return base58_check_encode(b'\x30', pkhash)

def trx_address(privkey):
    pubkey = BIP32.privkey_to_pubkey(privkey, compressed=False)[1:]
    khash = keccak256_hash(pubkey)
    pkhash = khash[-20:]
    return base58_check_encode(b'\x41', pkhash)

def _get_theme():
    from core.display import Colorate, Theme, get_inpt
    return Colorate, Theme, get_inpt

def wallet_scanner_init():
    Colorate, Theme, get_inpt = _get_theme()
    try:
        import aiohttp
        from mnemonic import Mnemonic
    except ImportError:
        import subprocess
        _cl = Theme.get_colors()
        print(Colorate.Horizontal(_cl["num"], "  [*] Installing required packages (aiohttp, mnemonic)..."))
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "aiohttp", "mnemonic", "-q"
        ])
        import aiohttp
        from mnemonic import Mnemonic
    _run(aiohttp, Mnemonic, Colorate, Theme, get_inpt)

def _run(aiohttp, Mnemonic, Colorate, Theme, get_inpt):
    RED     = _PY.red
    GREEN   = _PY.green
    CYAN    = _PY.cyan
    YELLOW  = _PY.yellow
    MAGENTA = _PY.pink
    RESET   = _PY.reset
    stats        = {"generated": 0, "found": 0}
    script_start = time.time()
    semaphore  = asyncio.Semaphore(150)
    print_lock = asyncio.Lock()

    def set_title(title: str):
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            sys.stdout.write(f"\x1b]2;{title}\x07")
            sys.stdout.flush()

    def save_wallet(network, address, balance, mnemonic, priv_key):
        os.makedirs("found_wallets", exist_ok=True)
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"found_wallets/{network}_{ts}.txt"
        with open(filename, "w") as f:
            f.write(f"Network      : {network}\n")
            f.write(f"Address      : {address}\n")
            f.write(f"Balance      : {balance}\n\n")
            f.write(f"Mnemonic     : {mnemonic}\n")
            f.write(f"Private Key  : {priv_key}\n")
        return filename

    def generate_wallets(seed_bytes):
        root = BIP32.from_seed(seed_bytes)
        eth_priv = root.derive_path("m/44'/60'/0'/0/0").private_key
        btc_priv = root.derive_path("m/44'/0'/0'/0/0").private_key
        ltc_priv = root.derive_path("m/44'/2'/0'/0/0").private_key
        trx_priv = root.derive_path("m/44'/195'/0'/0/0").private_key
        
        return (
            eth_address(eth_priv),
            btc_address(btc_priv),
            ltc_address(ltc_priv),
            trx_address(trx_priv),
        )

    async def get_balance(session, address, network):
        timeout = aiohttp.ClientTimeout(total=10)
        if network == "btc":
            url = f"https://blockstream.info/api/address/{address}"
            async with semaphore:
                try:
                    async with session.get(url, timeout=timeout) as r:
                        if r.status == 200:
                            d      = await r.json()
                            chain  = d.get("chain_stats", {})
                            return str(chain.get("funded_txo_sum", 0) - chain.get("spent_txo_sum", 0))
                        if r.status == 429:
                            await asyncio.sleep(2)
                            return await get_balance(session, address, network)
                except Exception:
                    return "0"
            return "0"
        if network == "trx":
            url = f"https://api.trongrid.io/v1/accounts/{address}"
            async with semaphore:
                try:
                    async with session.get(url, timeout=timeout) as r:
                        if r.status == 200:
                            data = (await r.json()).get("data", [])
                            return str(data[0].get("balance", 0)) if data else "0"
                except Exception:
                    return "0"
            return "0"
        endpoints = {
            "eth": f"https://ethbook.guarda.co/api/v2/address/{address}",
            "bnb": f"https://bsc-nn.atomicwallet.io/api/v2/address/{address}",
            "ltc": f"https://litecoin.atomicwallet.io/api/v2/address/{address}",
        }
        async with semaphore:
            try:
                async with session.get(endpoints[network], timeout=timeout) as r:
                    if r.status == 200:
                        return str((await r.json()).get("balance", "0"))
                    if r.status == 429:
                        await asyncio.sleep(2)
                        return await get_balance(session, address, network)
            except Exception:
                return "0"
        return "0"

    async def worker(session, word_count):
        await asyncio.sleep(random.uniform(0.0, 2.0))
        mnemo = Mnemonic("english")
        while True:
            mnemonic_str = mnemo.generate(strength=128 if word_count == 12 else 256)
            seed_bytes   = mnemo.to_seed(mnemonic_str, passphrase="")
            eth_addr, btc_addr, ltc_addr, trx_addr = generate_wallets(seed_bytes)
            results = await asyncio.gather(
                get_balance(session, eth_addr, "eth"),
                get_balance(session, eth_addr, "bnb"),
                get_balance(session, btc_addr, "btc"),
                get_balance(session, ltc_addr, "ltc"),
                get_balance(session, trx_addr, "trx"),
                return_exceptions=True
            )
            stats["generated"] += 1
            def val(raw, dec):
                return 0.0 if isinstance(raw, Exception) else int(raw) / 10**dec
            e_val   = val(results[0], 18)
            b_val   = val(results[1], 18)
            btc_val = val(results[2], 8)
            ltc_val = val(results[3], 8)
            trx_val = val(results[4], 6)
            m_str = mnemonic_str
            found = any(v > 0 for v in [e_val, b_val, btc_val, ltc_val, trx_val])
            if found:
                stats["found"] += 1
                _cl = Theme.get_colors()
                fp  = ""
                if e_val   > 0: fp = save_wallet("ETH", eth_addr, e_val,   m_str, seed_bytes.hex())
                if b_val   > 0: fp = save_wallet("BNB", eth_addr, b_val,   m_str, seed_bytes.hex())
                if btc_val > 0: fp = save_wallet("BTC", btc_addr, btc_val, m_str, seed_bytes.hex())
                if ltc_val > 0: fp = save_wallet("LTC", ltc_addr, ltc_val, m_str, seed_bytes.hex())
                if trx_val > 0: fp = save_wallet("TRX", trx_addr, trx_val, m_str, seed_bytes.hex())
                async with print_lock:
                    print(Colorate.Horizontal(_cl["head"], f"\n  {'█'*68}"))
                    print(Colorate.Horizontal(_cl["head"], f"  [$$$]  WALLET WITH BALANCE FOUND  [$$$]"))
                    print(Colorate.Horizontal(_cl["sub"],  f"  {'─'*68}"))
                    print(Colorate.Horizontal(_cl["num"],  f"  SEED    : ") + Colorate.Horizontal(_cl["txt"], m_str))
                    print(Colorate.Horizontal(_cl["num"],  f"  ETH/BNB : ") + Colorate.Horizontal(_cl["txt"], f"{eth_addr}  →  ETH:{e_val}  BNB:{b_val}"))
                    print(Colorate.Horizontal(_cl["num"],  f"  BTC     : ") + Colorate.Horizontal(_cl["txt"], f"{btc_addr}  →  {btc_val}"))
                    print(Colorate.Horizontal(_cl["num"],  f"  LTC     : ") + Colorate.Horizontal(_cl["txt"], f"{ltc_addr}  →  {ltc_val}"))
                    print(Colorate.Horizontal(_cl["num"],  f"  TRX     : ") + Colorate.Horizontal(_cl["txt"], f"{trx_addr}  →  {trx_val}"))
                    print(Colorate.Horizontal(_cl["inp"],  f"  Saved   : {fp}"))
                    print(Colorate.Horizontal(_cl["head"], f"  {'█'*68}\n"))
            seed_s = m_str[:12] + ".."
            e_s    = f"{eth_addr[:5]}..{eth_addr[-3:]}"
            btc_s  = f"{btc_addr[:5]}..{btc_addr[-3:]}"
            ltc_s  = f"{ltc_addr[:5]}..{ltc_addr[-3:]}"
            trx_s  = f"{trx_addr[:5]}..{trx_addr[-3:]}"
            bal = (
                f"{GREEN}E:{e_val} B:{b_val} BTC:{btc_val} LTC:{ltc_val} TRX:{trx_val}{RESET}"
                if found else "0"
            )
            line = (
                f"SEED:{MAGENTA}{seed_s:<14}{RESET}"
                f" | E/B:{CYAN}{e_s}{RESET}"
                f" BTC:{YELLOW}{btc_s}{RESET}"
                f" LTC:{CYAN}{ltc_s}{RESET}"
                f" TRX:{RED}{trx_s}{RESET}"
                f" | BAL:{bal}"
            )
            async with print_lock:
                print(line)

    async def title_loop():
        while True:
            elapsed = time.time() - script_start
            rps     = stats["generated"] / elapsed if elapsed > 0 else 0
            set_title(
                f"Scanned: {stats['generated']:,}  |  Hits: {stats['found']}  |  {rps:.1f} w/s"
            )
            await asyncio.sleep(1)

    async def _main(num_workers, word_count):
        _cl = Theme.get_colors()
        os.system("cls" if os.name == "nt" else "clear")
        print(Colorate.Horizontal(_cl["head"], f"  {'═'*50}"))
        print(Colorate.Horizontal(_cl["head"], f"  {'':^4}Crypto Wallet Scanner  v3.0"))
        print(Colorate.Horizontal(_cl["sub"],  f"  {'':^4}ETH  /  BNB  /  BTC  /  LTC  /  TRX"))
        print(Colorate.Horizontal(_cl["head"], f"  {'═'*50}\n"))
        print(
            Colorate.Horizontal(_cl["num"], "  Workers : ") +
            Colorate.Horizontal(_cl["txt"], str(num_workers)) +
            Colorate.Horizontal(_cl["num"], "   |   Seed Words : ") +
            Colorate.Horizontal(_cl["txt"], str(word_count)) + "\n"
        )
        connector = aiohttp.TCPConnector(limit=500, limit_per_host=100, ttl_dns_cache=300)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [asyncio.create_task(worker(session, word_count)) for _ in range(num_workers)]
            tasks.append(asyncio.create_task(title_loop()))
            await asyncio.gather(*tasks)

    _cl = Theme.get_colors()
    os.system("cls" if os.name == "nt" else "clear")
    print(Colorate.Horizontal(_cl["head"], f"\n  ╔══════════════════════════════════════════╗"))
    print(Colorate.Horizontal(_cl["sub"],  f"  ║       ETH  BNB  BTC  LTC  TRX            ║"))
    print(Colorate.Horizontal(_cl["head"], f"  ╚══════════════════════════════════════════╝\n"))
    try:
        w = get_inpt("navi@walletbrute workers (default 50):").strip()
        num_workers = int(w) if w else 50
    except ValueError:
        num_workers = 50
    print()
    print(Colorate.Horizontal(_cl["head"], "  ┌─────────────────────────────────────────────────────────────┐"))
    print(Colorate.Horizontal(_cl["txt"],  "  │  Seed Word Count — what's the difference?                   │"))
    print(Colorate.Horizontal(_cl["sub"],  "  │                                                             │"))
    print(Colorate.Horizontal(_cl["num"],  "  │  12 words") + Colorate.Horizontal(_cl["txt"], "  →  2^128 combinations  (340 undecillion)        │"))
    print(Colorate.Horizontal(_cl["txt"],  "  │              Used by: MetaMask, TrustWallet, Coinbase       │"))
    print(Colorate.Horizontal(_cl["inp"],  "  │              Speed: faster to generate  ✓ recommended       │"))
    print(Colorate.Horizontal(_cl["sub"],  "  │                                                             │"))
    print(Colorate.Horizontal(_cl["num"],  "  │  24 words") + Colorate.Horizontal(_cl["txt"], "  →  2^256 combinations  (astronomically more)    │"))
    print(Colorate.Horizontal(_cl["txt"],  "  │              Used by: Ledger, Trezor (hardware wallets)     │"))
    print(Colorate.Horizontal(_cl["txt"],  "  │              Speed: slightly slower, fewer targets online   │"))
    print(Colorate.Horizontal(_cl["sub"],  "  │                                                             │"))
    print(Colorate.Horizontal(_cl["inp"],  "  │  → Use 12 for scanning. Most funded wallets use 12 words.  │"))
    print(Colorate.Horizontal(_cl["head"], "  └─────────────────────────────────────────────────────────────┘"))
    try:
        wc = get_inpt("navi@wallet-scanner word-count 12/24 (default 12):").strip()
        word_count = int(wc) if wc in ["12", "24"] else 12
    except ValueError:
        word_count = 12
    print()
    print(
        Colorate.Horizontal(_cl["num"], f"  [*] Starting ") +
        Colorate.Horizontal(_cl["txt"], str(num_workers)) +
        Colorate.Horizontal(_cl["num"], " workers with ") +
        Colorate.Horizontal(_cl["txt"], str(word_count)) +
        Colorate.Horizontal(_cl["num"], "-word seeds...\n")
    )
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(_main(num_workers, word_count))
    except KeyboardInterrupt:
        elapsed = time.time() - script_start
        rps     = stats["generated"] / elapsed if elapsed > 0 else 0
        mins, s = divmod(int(elapsed), 60)
        hrs, m  = divmod(mins, 60)
        _cl = Theme.get_colors()
        print()
        print(Colorate.Horizontal(_cl["head"], f"\n  {'─'*46}"))
        print(Colorate.Horizontal(_cl["head"], "    SCANNER STOPPED"))
        print(Colorate.Horizontal(_cl["head"], f"  {'─'*46}"))
        print(
            Colorate.Horizontal(_cl["num"], "  Total Scanned : ") +
            Colorate.Horizontal(_cl["txt"], f"{stats['generated']:,}")
        )
        print(
            Colorate.Horizontal(_cl["num"], "  Total Found   : ") +
            Colorate.Horizontal(_cl["txt"], str(stats["found"]))
        )
        print(
            Colorate.Horizontal(_cl["num"], "  Avg Speed     : ") +
            Colorate.Horizontal(_cl["txt"], f"{rps:.2f} wallets/sec")
        )
        print(
            Colorate.Horizontal(_cl["num"], "  Runtime       : ") +
            Colorate.Horizontal(_cl["txt"], f"{hrs:02d}h {m:02d}m {s:02d}s")
        )
        print(Colorate.Horizontal(_cl["head"], f"  {'─'*46}\n"))
        input(Colorate.Horizontal(_cl["inp"], "\n  Press Enter to return to menu..."))
