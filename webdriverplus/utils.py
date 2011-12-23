import urllib2


def _download(url, filename):
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(filename, 'wb')
    meta = u.info()
    size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, size)

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
        print status,

    print chr(8) + 'Done' + ' ' * (len(status) + 1)
    f.close()
