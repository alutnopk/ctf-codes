from hashlib import md5
import string

# target code obtained by using 'pa' from radare2
ALPHABET = string.digits + string.ascii_letters
PASSWD = ""
SALT = "GpLaMjEWpVOjnnmkRGiledp6Mvcezxls"
CODE = b"\x48\x89\xfe\x48\xbf\xf1\x26\xdc\xb3\x07\x00\x00\x00\xff\xd6"
OFFSET = [8, 2, 7, 1]
INSTR_SIZE = [4, 4, 4, 3]

def gen_word(s, i):
    if len(s) == 4:
        word = ''.join(s)
        solve(word, i)
        return
    global ALPHABET
    for c in ALPHABET:
        s.append(c)
        gen_word(s, i)
        s.pop()
    
def solve(word, i):
    global SALT, CODE
    salted_word = word + SALT[i<<3:(i+1)<<3]
    m = md5()
    m.update(salted_word.encode('utf-8'))
    res = m.digest()
    code = res[OFFSET[i]:OFFSET[i]+INSTR_SIZE[i]]
    if code == CODE[i<<2:(i+1)<<2]:
        print(f"Word {i}: {word}")
        global PASSWD
        PASSWD += word
        return

for i in range(4):
    s = []
    gen_word(s, i)
print(f"Final password: {PASSWD}")