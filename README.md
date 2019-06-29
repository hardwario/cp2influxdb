# COOPER to InfluxDB

[![Travis](https://img.shields.io/travis/hardwario/cp2influxdb/master.svg)](https://travis-ci.org/hardwario/cp2influxdb)
[![Release](https://img.shields.io/github/release/hardwario/cp2influxdb.svg)](https://github.com/hardwario/cp2influxdb/releases)
[![License](https://img.shields.io/github/license/hardwario/cp2influxdb.svg)](https://github.com/hardwario/cp2influxdb/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cp2influxdb.svg)](https://pypi.org/project/cp2influxdb/)


## Installing

You can install **cp2influxdb** directly from PyPI:

```sh
sudo pip3 install -U cp2influxdb
```

## Usage

Update config.yml and run

```sh
cp2influxdb -c config.yml
```

### Systemd

Insert this snippet to the file /lib/systemd/system/cp2influxdb.service:
```
[Unit]
Description=COOPER cp2influxdb
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/cp2influxdb -c /etc/cooper/cp2influxdb.yml
Restart=always
RestartSec=5
StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
```

Start the service:

    sudo systemctl start cp2influxdb.service

Enable the service start on boot:

    sudo systemctl enable cp2influxdb.service

View the service log:

    journalctl -u cp2influxdb.service -f

## License

This project is licensed under the [**MIT License**](https://opensource.org/licenses/MIT/) - see the [**LICENSE**](LICENSE) file for details.
