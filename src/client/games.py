import transmissionrpc
import psutil
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

tc = transmissionrpc.Client(
    address=config["CLIENT SETTINGS"]["IP"],
    port=config["CLIENT SETTINGS"]["PORT"],
    user=config["CLIENT SETTINGS"]["USER"],
    password=config["CLIENT SETTINGS"]["PASSWORD"]
)

PROGRAMS = config["APPS"]["APPS"]
PROGRAMS = PROGRAMS.replace(",", "")
PROGRAMS = PROGRAMS.lower()
PROGRAMS = list(PROGRAMS.split())


def start_torrents() -> None:
    torrents = tc.get_torrents()
    for t in torrents:
        if t.status == "stopped":
            t.start()


def stop_torrents() -> None:
    torrents = tc.get_torrents()
    for t in torrents:
        if t.status != "stopped":
            t.stop()


def interrupt_transmission():
    processes = (p.name() for p in psutil.process_iter())
    return (set(PROGRAMS) & set(processes))


while True:
    if interrupt_transmission():
        stop_torrents()
    else:
        start_torrents()
    sleep(10)
