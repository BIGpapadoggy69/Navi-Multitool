#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
#
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import os, time, sys, re
from pystyle import Center

def _strip(_t): return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', _t)

class ModernUI:
    @staticmethod
    def print_banner(_col, _thm, _clr):
        _clr()
        _c = _thm.get_colors()
        _b = [
            r" _   _               _ ",
            r"| \ | |             (_)",
            r"|  \| |  __ _ __   __ _ ",
            r"| . ` | / _` |\ \ / /| |",
            r"| |\  || (_| | \ V / | |",
            r"|_| \_| \__,_|  \_/  |_|"
        ]
        
        import shutil
        _tw = shutil.get_terminal_size().columns
        
        print("\n\n")
        for i, line in enumerate(_b):
            if i == 5:
                _left = "~ present day "
                _right = "present time ~"
                _pad = 5
                
                _total_w = len(_left) + _pad + len(line) + _pad + len(_right)
                _start_p = (_tw - _total_w) // 2
                
                _res = " " * _start_p
                _res += _col.Horizontal(_c["num"], _left)
                _res += " " * _pad
                _res += _col.Horizontal(_c["banner"], line)
                _res += " " * _pad
                _res += _col.Horizontal(_c["num"], _right)
                print(_res)
            else:
                print(_col.Horizontal(_c["banner"], Center.XCenter(line)))
        print("\n")



    @staticmethod
    def render_menu(_col, _thm, _cats):
        _c = _thm.get_colors()
        _nc = len(_cats)
        _cw = 32 if _nc == 3 else 26
        import shutil
        _tw = shutil.get_terminal_size().columns
        _tot = (_cw * _nc) + ((_nc - 1) * 2)
        _p = " " * max(0, (_tw - _tot) // 2)

        _mx = max(len(_it) for _, _it in _cats)
        
        _hl = _p
        for _n, _ in _cats: _hl += _n.center(_cw) + "  "
        print(_col.Horizontal(_c["head"], _hl))
        
        _tl = _p
        for _ in _cats: _tl += "┌" + "─" * (_cw - 2) + "┐" + "  "
        print(_col.Horizontal(_c["num"], _tl))
        
        for _i in range(_mx):
            _rl = _p
            for _, _it in _cats:
                if _i < len(_it) and _it[_i]:
                    _f = _it[_i]
                    if "]" in _f: _f = f"({_f[_f.find('[')+1:_f.find(']')].zfill(2)}) > {_f[_f.find(']')+1:].strip()}"
                    _pl = _cw - 4 - len(_strip(_f))
                    _rl += _col.Horizontal(_c["num"], "│ ") + _col.Horizontal(_c["txt"], _f) + " " * _pl + _col.Horizontal(_c["num"], " │") + "  "
                else: _rl += _col.Horizontal(_c["num"], "│" + " " * (_cw - 2) + "│") + "  "
            print(_rl)
            
        _bl = _p
        for _ in _cats: _bl += "└" + "─" * (_cw - 2) + "┘" + "  "
        print(_col.Horizontal(_c["num"], _bl))
