import transmissionrpc
import psutil
from time import sleep
import json


def start_torrents(tc) -> None:
    torrents = tc.get_torrents()
    for t in torrents:
        if t.status == "stopped":
            t.start()


def stop_torrents(tc) -> None:
    torrents = tc.get_torrents()
    for t in torrents:
        if t.status != "stopped":
            t.stop()


def interrupt_transmission(progs):
    processes = (p.name() for p in psutil.process_iter())
    return (set(progs) & set(processes))


if __name__ == "__main__":

    with open("settings.json") as config_file:
        config = json.load(config_file)

    tc = transmissionrpc.Client(
        address=config["TRANSMISSION"]["IP"],
        port=config["TRANSMISSION"]["PORT"],
        user=config["TRANSMISSION"]["USER"],
        password=config["TRANSMISSION"]["PASSWORD"]
    )

    PROGRAMS = config["APPS"]

    while True:
        if interrupt_transmission(PROGRAMS):
            stop_torrents(tc)
        else:
            start_torrents(tc)
        sleep(30)
