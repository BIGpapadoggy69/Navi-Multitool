#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import platform, os, ctypes, psutil, subprocess, time

def get_sys_data():
    _cl = lambda x: str(round(x, 2))
    _m = psutil.virtual_memory()
    _d = psutil.disk_usage('/')
    _ut = time.time() - psutil.boot_time()
    _h, _rem = divmod(_ut, 3600)
    _min, _sec = divmod(_rem, 60)
    
    _data = {
        "OS": f"{platform.system()} {platform.release()}",
        "RAM Total": f"{_m.total // (1024**3)} GB",
        "RAM Used": f"{_m.used // (1024**3)} GB",
        "RAM Usage": f"{_m.percent}%",
        "CPU Usage": f"{psutil.cpu_percent()}%",
        "CPU Cores": f"{psutil.cpu_count(logical=False)} phys / {psutil.cpu_count()} log",
        "Uptime": f"{int(_h)}h {int(_min)}m {int(_sec)}s",
        "Disk Usage": f"{_d.used // (1024**3)}/{_d.total // (1024**3)} GB ({_d.percent}%)",
    }
    
    try:
        _gpu = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode().split('\n')[1].strip()
        _data["GPU"] = _gpu
    except: pass
    
    try: _a = os.getuid() == 0
    except:
        try: _a = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except: _a = False
    _data["Privileged"] = str(_a)
    
    return _data
