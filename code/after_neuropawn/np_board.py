"""Shared helpers for the NeuroPawn Knight scripts (record.py, live_view.py)."""
import time


def parse_channels(s):
    out = set()
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-"); out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return sorted(c for c in out if 1 <= c <= 8)


def is_streaming(buf):
    """True if buf holds consecutive valid 57-byte Knight IMU frames with rising counters."""
    k, cnt = 0, []
    while k + 57 <= len(buf):
        if buf[k] == 0xA0 and buf[k + 56] == 0xC0:
            cnt.append(buf[k + 1]); k += 57
        else:
            k += 1
    return sum(1 for x, y in zip(cnt, cnt[1:]) if (y - x) % 256 == 1) >= 5


def ensure_good_boot(port, tries=8, wait=6.0):
    """Opening the port resets the board (DTR). Resets often hang at 'Scanning for IMU...'.
    Retry until a boot reaches 'EEG ... SPS', then clear HUPCL so closing/reopening the port
    no longer resets the board -> BrainFlow connects to the already-running board."""
    import serial, termios
    for i in range(1, tries + 1):
        s = serial.Serial(port, 115200, timeout=0.2)
        t = time.time(); buf = b""
        while b"SPS\r\n" not in buf and time.time() - t < wait:
            buf += s.read(4096)
            if len(buf) > 100000:      # garbage flood, not a real boot
                break
            if len(buf) > 600 and is_streaming(buf):
                print("Board already running (no reset) - reusing it.")
                s.close(); return True
        if b"SPS\r\n" in buf and len(buf) < 100000:
            attrs = termios.tcgetattr(s.fd)
            attrs[2] &= ~termios.HUPCL        # keep DTR asserted on close -> no reset on reopen
            termios.tcsetattr(s.fd, termios.TCSANOW, attrs)
            s.close()
            banner = buf[:buf.find(b"SPS\r\n") + 3].decode(errors="replace").replace("\r\n", " / ")
            print(f"Good boot on try {i}: {banner}")
            return True
        print(f"Boot try {i}: stuck ({buf[:30]!r}), resetting")
        s.close()                              # HUPCL still set -> next open resets the board
        time.sleep(0.5)
    return False


def uv_factor():
    """BrainFlow < 5.24 scales Knight EEG ~79.57x too high; return the factor that converts to uV."""
    from importlib.metadata import version
    major, minor = (int(x) for x in version("brainflow").split(".")[:2])
    return 1 / 79.57 if (major, minor) < (5, 24) else 1.0
