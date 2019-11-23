# Transmission-Interactive-Pauser

Automatically pauses all torrents on remote server when specific conditions are met.

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

<!-- <figure class="video_container">
  <video controls="true" allowfullscreen="true">
    <source src="https://raw.githubusercontent.com/JoshuaA9088/Transmission-Interactive-Pauser/master/assets/demo.webm" type="video/webm">
  </video>
</figure> -->

## Dependencies
Install all required dependencies with `pip install -r requirements.txt` from the `src/` directory.

Ensure that RPC is enabled for Transmission Daemon.

## Client
The `src/games.py` file will auto pause all transmisson torrents upon any of the games listed in the `settings.json` running.

Although the naming scheme implies that a server client relationship exists, the server script included in this repository does not have to be running for `src/games.py` to work. Infact they are **completely** independent of each other and designed to not affect each other.

#### Settings
The settings.json file declares many necessary constants.
```
{
    "TRANSMISSION": {
        "IP": "IP_OF_TRANSMISSION",
        "PORT": "PORT_OF_TRANSMISSION",
        "USER": "USERNAME",
        "PASSWORD": "PASSWORD"
    },
    "APPS": [
        "app1.exe",
        "app2.exe",
        "app3.exe"
    ]
}
```

## Server
This script is eventually intended to be run as a systemd service, requiring a custom user to run under for optimal security.

This will pause all torrents upon a client connecting to the local OpenVPN server. The `/etc/openvpn/openvpn-status.log` file is read every 10 seconds to look for new clients.

It will also pause all torrent upon a client joining the minecraft server. Users can be excluded from this behavior if listed in the `settings.json` file.

#### Settings
The `settings.json` file declares many necessary constants.

```
{
    "TRANSMISSION": {
        "IP": "IP_OF_TRANSMISSION",
        "PORT": "PORT_OF_TRANSMISSION",
        "USER": "USERNAME",
        "PASSWORD": "PASSWORD"
    },
    "VPN": {
        "LOG": "PATH_TO_LOG",
        "MIN_CLIENTS": "1",
        "CLIENTS": [
            "Client1",
            "Client2",
            "Client3"
        ]
    },
    "MINECRAFT": {
        "IP": "IP_OF_MC_SERVER",
        "PORT": "PORT_OF_MC_SERVER",
        "EXCLUDED_USERS": [
            "Client1",
            "Client2",
            "Client3"
        ]
    }
}
```

## License
- **[MIT license](http://opensource.org/licenses/mit-license.php)**
