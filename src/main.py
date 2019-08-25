import transmissionrpc
import psutil
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

PROGRAMS = config.sections()
PROGRAMS.remove("CLIENT SETTINGS")

tc = transmissionrpc.Client(
    address=config["CLIENT SETTINGS"]["IP"],
    port=config["CLIENT SETTINGS"]["PORT"],
    user=config["CLIENT SETTINGS"]["USER"],
    password=config["CLIENT SETTINGS"]["PASSWORD"]
    )


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    return (a_set & b_set)

while True:
    sleep(5)
    processes = (p.name() for p in psutil.process_iter())
    torrents = tc.get_torrents()

    if common_member(PROGRAMS, processes):
        for t in torrents:
            if t.status != "stopped":
                t.stop()
                if __debug__:
                    print(f"Stopped {t.name}")
    else:
        for t in torrents:
            if t.status == "stopped":
                t.start()
                if __debug__:
                    print(f"Started {t.name}")
