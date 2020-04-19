import csv
import time

import jstyleson
import transmissionrpc
from IPy import IP
from mcstatus import MinecraftServer


def common_member(a: list, b: list) -> bool:
    a = set(a)
    b = set(b)
    return a & b


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


def client_vpn(log_path, clients, num_pause) -> bool:
    f = open(log_path)
    csv_reader = csv.reader(f, delimiter=",")
    user_data = []

    for row in csv_reader:
        if common_member(clients, row):
            try:
                IP(row[0])
            except ValueError:
                user_data.append(row)
    f.close()
    return len(user_data) > num_pause


def client_mc(server, excluded) -> bool:
    query = server.query()
    players = [name.lower() for name in query.players.names]
    return players != excluded and len(players) > 0


if __name__ == "__main__":

    with open("settings.json") as config_file:
        config = jstyleson.load(config_file)

    # VPN Parameters
    LOG_PATH = config["VPN"]["LOG"]
    MIN_CLIENTS = config["VPN"]["MIN_CLIENTS"]
    CLIENTS = config["VPN"]["CLIENTS"]

    # Minecraft Parameters
    EXCLUDED_USERS = config["MINECRAFT"]["EXCLUDED_USERS"]

    tc = transmissionrpc.Client(
        address=config["TRANSMISSION"]["IP"],
        port=config["TRANSMISSION"]["PORT"],
        user=config["TRANSMISSION"]["USER"],
        password=config["TRANSMISSION"]["PASSWORD"],
    )

    server = MinecraftServer.lookup(
        f"{config['MINECRAFT']['IP']} : {config['MINECRAFT']['PORT']}"
    )

    while True:
        status = server.status()
        if client_mc(server, EXCLUDED_USERS) or client_vpn(LOG_PATH, MIN_CLIENTS):
            stop_torrents()
        else:
            start_torrents()
        time.sleep(30)
