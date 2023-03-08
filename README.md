# Zeroconf Plugin for CLN

A plugin for selectively allowing zeroconf channels from a peer.

## Quickstart

Assuming you have a running `lightningd` and a working `lightning-cli`:

```sh
git clone https://github.com/voltagecloud/zero-conf-cln.git zero-conf-cln
lightning-cli -k plugin subcommand=start \
                        plugin="$PWD"/zero-conf-cln/zero-conf-cln.py \
			zeroconf-allow=<peer_hex_pubkey>
```

To start `lightningd` with the plugin enabled:

```sh
git clone https://github.com/voltagecloud/zero-conf-cln.git zero-conf-cln
lightningd ... \
           --plugin="$PWD"/zero-conf-cln/zero-conf-cln.py \
           --zeroconf-allow=<peer_hex_pubkey> \
	   ...
```
