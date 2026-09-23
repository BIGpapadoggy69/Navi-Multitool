#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import os, sys
from core.display import Theme, Colorate, get_inpt

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except:
    os.system("pip install phonenumbers -q")
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone

def _w_log(m, s='+'):
    c = Theme.get_colors()
    return f" {Colorate.Horizontal(c['num'], f'[{s}]')} {Colorate.Horizontal(c['txt'], m)}"

def NumberInfo(p_num):
    try:
        p = phonenumbers.parse(p_num, None)
        return {
            "Carrier": carrier.name_for_number(p, "en"),
            "Type": "Mobile" if phonenumbers.number_type(p) == phonenumbers.PhoneNumberType.MOBILE else "Fixed",
            "Region": phonenumbers.region_code_for_number(p),
            "Location": geocoder.description_for_number(p, "en"),
            "Timezone": timezone.time_zones_for_number(p)[0] if timezone.time_zones_for_number(p) else "N/A"
        }
    except: return None

def phone_track():
    cl = Theme.get_colors()
    from core.display import print_banner
    print_banner()
    print(Colorate.Horizontal(cl["head"], "  [ PHONE TRACKER ]\n"))
    
    _n = get_inpt("number (ex: +1...):")
    if not _n: return
    print(Colorate.Horizontal(cl["head"], f"  [*] Fetching data for {_n}...\n"))
    
    try:
        _p = phonenumbers.parse(_n, None)
        _valid = phonenumbers.is_valid_number(_p)
        
        _res = {
            "Valid": _valid,
            "E164": phonenumbers.format_number(_p, phonenumbers.PhoneNumberFormat.E164),
            "International": phonenumbers.format_number(_p, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "National": phonenumbers.format_number(_p, phonenumbers.PhoneNumberFormat.NATIONAL),
            "Carrier": carrier.name_for_number(_p, "en") or "Unknown",
            "Type": "Mobile" if phonenumbers.number_type(_p) == phonenumbers.PhoneNumberType.MOBILE else "Fixed",
            "Region": phonenumbers.region_code_for_number(_p),
            "Location": geocoder.description_for_number(_p, "en"),
            "Timezones": len(timezone.time_zones_for_number(_p)),
            "WhatsApp": f"https://wa.me/{_n.strip('+').replace(' ', '')}",
            "Telegram": f"https://t.me/{_n}"
        }
        
        for _k, _v in _res.items():
            print(f"  {Colorate.Horizontal(cl['num'], f'{_k:<12}')} : {Colorate.Horizontal(cl['txt'], str(_v))}")
            
    except Exception as _e:
        print(Colorate.Horizontal(cl["num"], f"  [!] Error: {_e}"))
        
    input(Colorate.Horizontal(cl["head"], "\n  Press Enter..."))
