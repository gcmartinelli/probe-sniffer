## probe-sniffer

Records to disk 802.11 network probe requests.

I.e. What WIFI networks are devices around you looking for?

### Dependencies
* Linux
* iwconfig (Linux utility)
* [Python 3](https://python.org)
* [scapy](https://scapy.net)

### Instalation

`pip install -r requirements.txt`

### Usage

`python listen.py <interface_name> [filename]`

`interface_name` can be found using the `iwconfig` command on Linux

If `filename` is not passed, a `dump.txt` file will be created on the same directory as the script.

You may need to run as superuser in case `iwconfig` complains about not being able to change the network card's channel/frequency
