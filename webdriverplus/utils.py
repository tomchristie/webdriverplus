import os
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


def _download(url, filename):
    file_name = url.split('/')[-1]
    u = urlopen(url)
    f = open(filename, 'wb')
    meta = u.info()
    size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, size))

    downloaded = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        downloaded += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (downloaded, downloaded * 100. / size)
        status = status + chr(8) * (len(status) + 1)
        print(status),

    print(chr(8) + 'Done' + ' ' * (len(status) + 1))
    f.close()


# http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
def get_terminal_size():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import struct
            import termios
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])
