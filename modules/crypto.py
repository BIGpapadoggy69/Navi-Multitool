#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import base64, random, string

class CryptXer:
    @staticmethod
    def b64_e(s): return base64.b64encode(s.encode('utf-8')).decode('utf-8')
    @staticmethod
    def b64_d(s): return base64.b64decode(s.encode('utf-8')).decode('utf-8')

def make_pw(ln=16):
    c = list(string.ascii_letters + string.digits + "!@#$%^&*")
    random.shuffle(c)
    return "".join([random.choice(c) for _ in range(ln)])
