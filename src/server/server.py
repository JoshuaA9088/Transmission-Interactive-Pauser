from mcstatus import MinecraftServer
import transmissionrpc
import csv
from IPy import IP
from time import sleep
import configparser
import time

config = configparser.ConfigParser()
config.read("settings.ini")

# Parse CLIENTS config into list
CLIENTS = config["VPN"]["CLIENTS"]
CLIENTS = CLIENTS.replace(",", "")
CLIENTS = list(CLIENTS.split())

EXCLUDED_USERS = config["MINECRAFT"]["EXCLUDED_USERS"]
EXCLUDED_USERS = EXCLUDED_USERS.replace(",", "")
EXCLUDED_USERS = EXCLUDED_USERS.lower()
EXCLUDED_USERS = list(EXCLUDED_USERS.split())

tc = transmissionrpc.Client(
    address=config["CLIENT"]["IP"],
    port=config["CLIENT"]["PORT"],
    user=config["CLIENT"]["USER"],
    password=config["CLIENT"]["PASSWORD"]
)

server = MinecraftServer.lookup(
    f"{config['MINECRAFT']['IP']} : {config['MINECRAFT']['PORT']}")


def common_member(a: list, b: list) -> bool:
    a = set(a)
    b = set(b)
    return (a & b)


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


def client_vpn() -> bool:
    f = open(config["VPN"]["LOG_PATH"])
    csv_reader = csv.reader(f, delimiter=",")
    user_data = []

    for row in csv_reader:
        if common_member(CLIENTS, row):
            try:
                IP(row[0])
            except ValueError:
                user_data.append(row)
    f.close()
    return (len(user_data) > 2)


def client_mc() -> bool:
    query = server.query()
    players = [name.lower() for name in query.players.names]
    return (players != EXCLUDED_USERS and len(players) > 0)


while True:
    status = server.status()
    if client_mc():
        stop_torrents()
    else:
        start_torrents()
    time.sleep(10)
