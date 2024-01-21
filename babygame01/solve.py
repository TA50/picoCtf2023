from pwn import *

exe = ELF("./game_patched")


context.arch = 'amd64'


REMOTE = False
DEBUG = False
LOG = True
def conn():
    global REMOTE
    global DEBUG
    global LOG
    
    if 'R' in args:
        REMOTE = True
        return remote(f'saturn.picoctf.net', 52668)
    
    
    r = process(exe.path)
    if 'D' in args:
        DEBUG = True
        gdb.attach(r, '''
                    # while True:
                    b 0x0010133d
                    c
                       ''')
    return r

def main():
    global LOG
    
    r = conn()
    if DEBUG:
        print("waiting for debugger")
        sleep(1)
    # good luck pwning :)
    r.sendline(b'cat ./flag')
    r.interactive()


if __name__ == "__main__":
    main()
