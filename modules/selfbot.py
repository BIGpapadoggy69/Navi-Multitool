#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import json, os, re, random, threading, time
import requests, websocket
from datetime import datetime
from core.display import Colors, Colorate, Theme, get_inpt, print_banner, menu_opts

_LOGDIR = "logs"
_CFG    = "core/selfbot_config.json"
os.makedirs(_LOGDIR, exist_ok=True)
os.makedirs("core",  exist_ok=True)


class NaviSelfbot:
    def __init__(self, token):
        self.token   = token
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        self.running  = False
        self.user_id  = None
        self.username = None

        self.nitro_sniper    = False
        self.auto_responder  = False
        self.triggers        = {}
        self.logger          = False
        self.dm_logger       = False
        self.ghost_mode      = False
        self.ghost_delay     = 5
        self.status_rotator  = False
        self.statuses        = []
        self.anti_spam       = False
        self.reaction_adder  = False
        self.reaction_emoji  = "✅"
        self.reaction_channel = None
        self.typing_loop     = False
        self.typing_channel  = None

        self.ws = None
        self.heartbeat_interval = None
        self.seen_messages = set()
        self._stop_event   = threading.Event()
        self._session_id   = None
        self._last_seq     = None
        self._reconnect    = False

        self.cl = Theme.get_colors()

    def log(self, m, level="ok"):
        _icons  = {"ok": "+", "warn": "~", "err": "!", "info": "*"}
        _colors = {"ok": self.cl["head"], "warn": self.cl["num"], "err": self.cl["num"], "info": self.cl["txt"]}
        sym = _icons.get(level, "+")
        col = _colors.get(level, self.cl["txt"])
        ts  = datetime.now().strftime("%H:%M:%S")
        print(Colorate.Horizontal(col, f"  [{sym}] {ts}  {m}"))

    def _flog(self, cat, line):
        p = os.path.join(_LOGDIR, f"selfbot_{cat}.log")
        with open(p, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {line}\n")

    def save_settings(self):
        payload = {
            "nitro_sniper":    self.nitro_sniper,
            "auto_responder":  self.auto_responder,
            "triggers":        self.triggers,
            "logger":          self.logger,
            "dm_logger":       self.dm_logger,
            "ghost_mode":      self.ghost_mode,
            "ghost_delay":     self.ghost_delay,
            "status_rotator":  self.status_rotator,
            "statuses":        self.statuses,
            "anti_spam":       self.anti_spam,
            "reaction_adder":  self.reaction_adder,
            "reaction_emoji":  self.reaction_emoji,
            "reaction_channel": self.reaction_channel,
            "typing_loop":     False,
            "typing_channel":  self.typing_channel,
        }
        try:
            with open(_CFG, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"save failed: {e}", "err")

    def load_settings(self):
        if not os.path.exists(_CFG):
            return
        try:
            raw = open(_CFG, "r", encoding="utf-8").read()
            d   = json.loads(raw)
            for k, default in [
                ("nitro_sniper", False), ("auto_responder", False),
                ("triggers", {}), ("logger", False), ("dm_logger", False),
                ("ghost_mode", False), ("ghost_delay", 5),
                ("status_rotator", False), ("statuses", []),
                ("anti_spam", False), ("reaction_adder", False),
                ("reaction_emoji", "✅"), ("reaction_channel", None),
                ("typing_channel", None),
            ]:
                setattr(self, k, d.get(k, default))
            self.log("settings loaded", "info")
        except Exception as e:
            self.log(f"load failed: {e}", "warn")

    def _req(self, method, endpoint, **kw):
        url = f"https://discord.com/api/v9{endpoint}"
        try:
            return getattr(requests, method)(url, headers=self.headers, timeout=10, **kw)
        except Exception as e:
            self.log(f"{method.upper()} {endpoint}: {e}", "err")
            return None

    def _get(self, ep):    return self._req("get",    ep)
    def _post(self, ep, j=None): return self._req("post",   ep, json=j)
    def _delete(self, ep): return self._req("delete", ep)
    def _patch(self, ep, j=None): return self._req("patch",  ep, json=j)

    def fetch_user(self):
        r = self._get("/users/@me")
        if r and r.status_code == 200:
            d = r.json()
            self.user_id  = d["id"]
            disc = d.get("discriminator", "0")
            self.username = d["username"] + (f"#{disc}" if disc not in ("0", None) else "")
            return True
        return False

    def on_message(self, ws, raw):
        try:
            data = json.loads(raw)
        except Exception:
            return

        op = data.get("op")
        t  = data.get("t")
        d  = data.get("d") or {}
        s  = data.get("s")

        if s is not None:
            self._last_seq = s

        if op == 10:
            self.heartbeat_interval = d["heartbeat_interval"] / 1000
            threading.Thread(target=self.heartbeat, args=(ws,), daemon=True).start()
            if self._reconnect and self._session_id:
                self._resume(ws)
            else:
                self.identify(ws)

        elif op == 7:
            self._reconnect = True
            try: ws.close()
            except: pass

        elif op == 9:
            self._reconnect  = False
            self._session_id = None
            self._last_seq   = None
            time.sleep(random.uniform(1, 5))
            self.identify(ws)

        if t == "READY":
            self._session_id = d.get("session_id")
            self._reconnect  = False
            self.running     = True
            self.log(f"ready  ->  {self.username}")

        if t == "RESUMED":
            self.running = True
            self.log("session resumed", "info")

        if t == "MESSAGE_CREATE":
            self._handle_msg(d)

        if t == "MESSAGE_DELETE" and self.logger:
            self.log(f"del ch:{d.get('channel_id')} id:{d.get('id')}", "warn")

        if t == "MESSAGE_UPDATE" and self.logger:
            self.log(f"edit ch:{d.get('channel_id')} -> {d.get('content','')[:80]}", "warn")

    def heartbeat(self, ws):
        while self.running and not self._stop_event.is_set():
            try:
                ws.send(json.dumps({"op": 1, "d": self._last_seq}))
            except:
                break
            time.sleep(self.heartbeat_interval)

    def identify(self, ws):
        try:
            ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": self.token,
                    "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"},
                    "presence": {"status": "online", "activities": [], "since": None, "afk": False}
                }
            }))
        except Exception as e:
            self.log(f"identify err: {e}", "err")

    def _resume(self, ws):
        try:
            ws.send(json.dumps({
                "op": 6,
                "d": {"token": self.token, "session_id": self._session_id, "seq": self._last_seq}
            }))
        except Exception as e:
            self.log(f"resume err: {e}", "err")

    def _handle_msg(self, d):
        content    = d.get("content", "")
        author     = d.get("author") or {}
        author_id  = author.get("id")
        channel_id = d.get("channel_id")
        msg_id     = d.get("id")
        is_dm      = d.get("guild_id") is None

        if self.anti_spam:
            k = f"{channel_id}:{content}"
            if k in self.seen_messages:
                return
            self.seen_messages.add(k)
            if len(self.seen_messages) > 500:
                self.seen_messages.clear()

        if self.nitro_sniper and "discord.gift/" in content:
            m = re.search(r"discord\.gift/(\w+)", content)
            if m:
                threading.Thread(target=self._snipe, args=(m.group(1),), daemon=True).start()

        if self.auto_responder and author_id != self.user_id:
            for trig, resp in self.triggers.items():
                if trig.lower() in content.lower():
                    self.send_msg(channel_id, resp)
                    break

        if self.ghost_mode and author_id == self.user_id:
            threading.Thread(target=self._del_after, args=(channel_id, msg_id, self.ghost_delay), daemon=True).start()

        if self.reaction_adder:
            if self.reaction_channel is None or self.reaction_channel == channel_id:
                threading.Thread(target=self._react, args=(channel_id, msg_id, self.reaction_emoji), daemon=True).start()

        if self.dm_logger and is_dm and author_id != self.user_id:
            uname = f"{author.get('username','?')}#{author.get('discriminator','0')}"
            self._flog("dms", f"{uname} ({author_id}) ch:{channel_id} | {content}")
            self.log(f"DM from {uname}: {content[:60]}", "info")

    def _snipe(self, code):
        self.log(f"sniping {code}", "info")
        r = self._post(f"/entitlements/gift-codes/{code}/redeem")
        if r and r.status_code == 200:
            self.log(f"claimed! {code}")
        else:
            self.log(f"snipe failed: {r.json() if r else 'no resp'}", "err")

    def send_msg(self, channel_id, content):
        self._post(f"/channels/{channel_id}/messages", {"content": content})

    def _del_after(self, channel_id, msg_id, delay):
        time.sleep(delay)
        self._delete(f"/channels/{channel_id}/messages/{msg_id}")

    def _react(self, channel_id, msg_id, emoji):
        try:
            import urllib.parse
            e = urllib.parse.quote(emoji)
            requests.put(
                f"https://discord.com/api/v9/channels/{channel_id}/messages/{msg_id}/reactions/{e}/@me",
                headers=self.headers, timeout=5
            )
        except:
            pass

    def rotate_status(self):
        while self.status_rotator and self.running:
            for s in self.statuses:
                if not self.status_rotator or not self.running:
                    return
                self._patch("/users/@me/settings", {"custom_status": {"text": s.strip()}})
                time.sleep(10)

    def set_presence(self, status="online", name="", atype=0, emoji=None):
        acts = []
        if name:
            a = {"type": atype, "name": name}
            if emoji: a["emoji"] = {"name": emoji}
            acts.append(a)
        if self.ws:
            try:
                self.ws.send(json.dumps({
                    "op": 3,
                    "d": {"since": None, "activities": acts, "status": status, "afk": False}
                }))
                self.log(f"presence -> [{status}] {name}")
            except Exception as e:
                self.log(f"presence err: {e}", "err")

    def typing_loop_fn(self, channel_id):
        while self.typing_loop and self.running:
            self._post(f"/channels/{channel_id}/typing")
            time.sleep(8)

    def mass_dm(self, msg):
        r = self._get("/users/@me/relationships")
        if not r or r.status_code != 200:
            self.log("cant fetch friends", "err"); return
        sent = 0
        for f in r.json():
            if f.get("type") != 1: continue
            uid = f.get("id") or f.get("user", {}).get("id")
            cr  = self._post("/users/@me/channels", {"recipient_id": uid})
            if cr and cr.status_code == 200:
                self.send_msg(cr.json()["id"], msg)
                sent += 1
                self.log(f"sent -> {f.get('user',{}).get('username', uid)}")
                time.sleep(1.5)
        self.log(f"done, sent to {sent} friends")

    def spam_channel(self, channel_id, message, amount, delay=0.8):
        for i in range(amount):
            self.send_msg(channel_id, message)
            self.log(f"[{i+1}/{amount}]", "info")
            time.sleep(delay)
        self.log("spam done")

    def purge_own(self, channel_id, limit=50):
        r = self._get(f"/channels/{channel_id}/messages?limit=100")
        if not r or r.status_code != 200:
            self.log("fetch failed", "err"); return
        gone = 0
        for m in r.json():
            if m.get("author", {}).get("id") != self.user_id: continue
            res = self._delete(f"/channels/{channel_id}/messages/{m['id']}")
            if res and res.status_code == 204:
                gone += 1
            time.sleep(0.5)
            if gone >= limit: break
        self.log(f"purged {gone}")

    def nuke_guild(self, guild_id, mode="channels"):
        self.log(f"nuking {guild_id} mode={mode}", "warn")
        targets = []
        if mode in ("channels", "all"):
            r = self._get(f"/guilds/{guild_id}/channels")
            if r and r.status_code == 200:
                targets = [("/channels/" + c["id"], c.get("name")) for c in r.json()]
        for ep, name in targets:
            res = self._delete(ep)
            ok = res and res.status_code in (200, 204)
            self.log(f"  {'ok' if ok else 'fail'} {name}", "info" if ok else "err")
            time.sleep(0.3)
        if mode in ("roles", "all"):
            r = self._get(f"/guilds/{guild_id}/roles")
            if r and r.status_code == 200:
                for role in r.json():
                    if role["name"] == "@everyone": continue
                    self._delete(f"/guilds/{guild_id}/roles/{role['id']}")
                    time.sleep(0.3)
        self.log("nuke done")

    def fr_spam(self, uids):
        for uid in uids:
            r = self._post(f"/users/@me/relationships/{uid.strip()}", {})
            ok = r and r.status_code in (200, 204)
            self.log(f"fr {uid}: {'ok' if ok else 'fail'}", "info")
            time.sleep(1)

    def join_server(self, code):
        code = code.strip().split("/")[-1]
        r = self._post(f"/invites/{code}")
        if r and r.status_code == 200:
            self.log(f"joined: {r.json().get('guild',{}).get('name','?')}")
        else:
            self.log(f"join fail: {r.text if r else '?'}", "err")

    def _ws_once(self):
        self.ws = websocket.WebSocketApp(
            "wss://gateway.discord.gg/?v=9&encoding=json",
            on_message=self.on_message,
            on_error=lambda ws, e: self.log(f"ws err: {e}", "err"),
            on_close=lambda ws, *a: None,
        )
        self.ws.run_forever(ping_interval=30, ping_timeout=10)

    def _loop(self):
        wait = 1
        while not self._stop_event.is_set():
            self.running = False
            try:
                self._ws_once()
            except Exception as e:
                self.log(f"ws exception: {e}", "err")
            if self._stop_event.is_set():
                break
            self.log(f"disconnected, retry in {wait}s", "warn")
            self._reconnect = True
            time.sleep(wait)
            wait = min(wait * 2, 60)

    def start(self):
        self._stop_event.clear()
        threading.Thread(target=self._loop, daemon=True).start()
        for _ in range(100):
            if self.running: break
            time.sleep(0.1)

    def stop(self):
        self._stop_event.set()
        self.running = False
        try:
            if self.ws: self.ws.close()
        except: pass


def _tog(cl, k, lbl, flag, k2=None, lbl2=None, f2=None):
    def _state(f):
        return Colorate.Horizontal(cl["head"], "[ON] ") if f else Colorate.Horizontal(cl["num"], "[OFF]")
    row = Colorate.Horizontal(cl["num"], f"  [{k}] ") + Colorate.Horizontal(cl["txt"], lbl) + "  " + _state(flag)
    if k2 is not None:
        row += Colorate.Horizontal(cl["num"], f"   [{k2}] ") + Colorate.Horizontal(cl["txt"], lbl2) + "  " + _state(f2)
    print(row)

def _act(cl, k, lbl, k2=None, lbl2=None):
    row = Colorate.Horizontal(cl["num"], f"  [{k}] ") + Colorate.Horizontal(cl["txt"], lbl)
    if k2:
        row += Colorate.Horizontal(cl["num"], f"   [{k2}] ") + Colorate.Horizontal(cl["txt"], lbl2)
    print(row)

def _sep(cl):
    print(Colorate.Horizontal(cl["num"], "  " + "─" * 56))

def _draw_menu(cl, bot):
    print_banner()
    print(Colorate.Horizontal(cl["head"], f"  [ SELFBOT  ─  {bot.username} ]\n"))
    print(Colorate.Horizontal(cl["head"], "  TOGGLES"))
    _sep(cl)
    _tog(cl, "1",  "Nitro Sniper   ", bot.nitro_sniper,   "2", "Auto Responder ", bot.auto_responder)
    _tog(cl, "3",  "Edit/Del Logger", bot.logger,         "4", "Ghost Mode     ", bot.ghost_mode)
    _tog(cl, "5",  "Status Rotator ", bot.status_rotator, "6", "Anti Spam      ", bot.anti_spam)
    _tog(cl, "7",  "Auto Reactor   ", bot.reaction_adder, "8", "Typing Loop    ", bot.typing_loop)
    _tog(cl, "9",  "DM Logger      ", bot.dm_logger)
    print()
    print(Colorate.Horizontal(cl["head"], "  CONFIG"))
    _sep(cl)
    _act(cl, "10", "Setup Triggers", "11", "Setup Statuses")
    _act(cl, "12", "Set Presence")
    print()
    print(Colorate.Horizontal(cl["head"], "  ACTIONS"))
    _sep(cl)
    _act(cl, "20", "Mass DM Friends", "21", "Channel Spammer")
    _act(cl, "22", "Purge Own Msgs",  "23", "Server Nuke    ")
    _act(cl, "24", "Friend Spammer",  "25", "Join Server    ")
    print()
    _sep(cl)
    _act(cl, "99", "Terminate & Exit")
    print()


def selfbot_menu():
    cl = Theme.get_colors()
    print_banner()
    tk = get_inpt("Token:")
    bot = NaviSelfbot(tk)
    if not bot.fetch_user():
        print(Colorate.Horizontal(cl["num"], "  [!] Invalid Token."))
        time.sleep(2)
        return

    bot.start()
    bot.load_settings()

    while True:
        cl = Theme.get_colors()
        _draw_menu(cl, bot)
        c = get_inpt("navi@selfbot:~#")

        if c == "1":
            bot.nitro_sniper = not bot.nitro_sniper
            bot.log(f"nitro sniper {'on' if bot.nitro_sniper else 'off'}")
            bot.save_settings()

        elif c == "2":
            bot.auto_responder = not bot.auto_responder
            bot.log(f"auto responder {'on' if bot.auto_responder else 'off'}")
            bot.save_settings()

        elif c == "3":
            bot.logger = not bot.logger
            bot.log(f"logger {'on' if bot.logger else 'off'}")
            bot.save_settings()

        elif c == "4":
            bot.ghost_mode = not bot.ghost_mode
            if bot.ghost_mode:
                try: bot.ghost_delay = int(get_inpt("delay (sec):") or 5)
                except: bot.ghost_delay = 5
            bot.log(f"ghost mode {'on' if bot.ghost_mode else 'off'}")
            bot.save_settings()

        elif c == "5":
            bot.status_rotator = not bot.status_rotator
            if bot.status_rotator and bot.statuses:
                threading.Thread(target=bot.rotate_status, daemon=True).start()
            bot.log(f"status rotator {'on' if bot.status_rotator else 'off'}")
            bot.save_settings()

        elif c == "6":
            bot.anti_spam = not bot.anti_spam
            bot.log(f"anti spam {'on' if bot.anti_spam else 'off'}")
            bot.save_settings()

        elif c == "7":
            bot.reaction_adder = not bot.reaction_adder
            if bot.reaction_adder:
                bot.reaction_emoji   = get_inpt("emoji (default ✅):") or "✅"
                bot.reaction_channel = get_inpt("channel id (blank=all):").strip() or None
            bot.log(f"auto reactor {'on' if bot.reaction_adder else 'off'}")
            bot.save_settings()

        elif c == "8":
            bot.typing_loop = not bot.typing_loop
            if bot.typing_loop:
                bot.typing_channel = get_inpt("channel id:").strip()
                threading.Thread(target=bot.typing_loop_fn, args=(bot.typing_channel,), daemon=True).start()
            bot.log(f"typing loop {'on' if bot.typing_loop else 'off'}")
            bot.save_settings()

        elif c == "9":
            bot.dm_logger = not bot.dm_logger
            bot.log(f"dm logger {'on' if bot.dm_logger else 'off'}")
            bot.save_settings()

        elif c == "10":
            bot.log("format: word:reply,word2:reply2")
            t = get_inpt("triggers:")
            try:
                n = 0
                for pair in t.split(","):
                    if ":" not in pair: continue
                    k, v = pair.split(":", 1)
                    bot.triggers[k.strip()] = v.strip()
                    n += 1
                bot.log(f"set {n} triggers ({len(bot.triggers)} total)")
                bot.save_settings()
            except Exception as e:
                bot.log(str(e), "err")
            time.sleep(1)

        elif c == "11":
            raw = get_inpt("statuses (comma sep):")
            bot.statuses = [x.strip() for x in raw.split(",") if x.strip()]
            bot.log(f"set {len(bot.statuses)} statuses")
            bot.save_settings()
            time.sleep(1)

        elif c == "12":
            print(Colorate.Horizontal(cl["head"], "  online | idle | dnd | invisible"))
            st  = get_inpt("status:") or "online"
            nm  = get_inpt("activity name:")
            try: at = int(get_inpt("type 0=play 1=stream 2=listen 3=watch:") or 0)
            except: at = 0
            em = get_inpt("emoji:") or None
            bot.set_presence(st, nm, at, em)
            time.sleep(1)

        elif c == "20":
            msg = get_inpt("message:")
            threading.Thread(target=bot.mass_dm, args=(msg,), daemon=True).start()
            input(Colorate.Horizontal(cl["txt"], "  [running in bg, enter to return]"))

        elif c == "21":
            ch  = get_inpt("channel id:")
            msg = get_inpt("message:")
            try: amt = int(get_inpt("amount:") or 10)
            except: amt = 10
            try: dl = float(get_inpt("delay (s):") or 0.8)
            except: dl = 0.8
            threading.Thread(target=bot.spam_channel, args=(ch.strip(), msg, amt, dl), daemon=True).start()
            input(Colorate.Horizontal(cl["txt"], "  [running in bg, enter to return]"))

        elif c == "22":
            ch = get_inpt("channel id:")
            try: lim = int(get_inpt("max delete:") or 50)
            except: lim = 50
            threading.Thread(target=bot.purge_own, args=(ch.strip(), lim), daemon=True).start()
            input(Colorate.Horizontal(cl["txt"], "  [running in bg, enter to return]"))

        elif c == "23":
            print(Colorate.Horizontal(cl["num"], "  [!] irreversible!"))
            gid  = get_inpt("guild id:")
            mode = get_inpt("mode (channels/roles/all):") or "channels"
            if get_inpt("type NUKE:") == "NUKE":
                threading.Thread(target=bot.nuke_guild, args=(gid.strip(), mode), daemon=True).start()
                input(Colorate.Horizontal(cl["txt"], "  [running, enter to return]"))
            else:
                bot.log("cancelled", "warn"); time.sleep(1)

        elif c == "24":
            raw = get_inpt("user ids (comma sep):")
            uids = [x.strip() for x in raw.split(",") if x.strip()]
            threading.Thread(target=bot.fr_spam, args=(uids,), daemon=True).start()
            input(Colorate.Horizontal(cl["txt"], "  [running in bg, enter to return]"))

        elif c == "25":
            inv = get_inpt("invite:")
            bot.join_server(inv)
            time.sleep(1)

        elif c == "99":
            bot.stop()
            break
