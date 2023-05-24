import socket
import socks
from .Downloader import downloadPapers


def proxy(pchain):
    chain = pchain

    socks.setdefaultproxy()
    for hop in chain:
        socks.set_default_proxy(socks.SOCKS5, "localhost", 1080)

    rawsocket = socket.socket
    socket.socket = socks.socksocket
