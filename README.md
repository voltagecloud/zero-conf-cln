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

## Zeroconf Probing

The plugin includes the responder side of an ad-hoc protocol based on `custommsg`s that a funder node can use to ask a fundee node whether or not it will accept zeroconf channels from the funder node.

This ad-hoc protocol is a JSON-RPC 2.0-like request-response protocol on top of `custommsg`s, whereby all the bytes following the 2-byte type prefix form a valid UTF-8 JSON encoding. Essentially:

```py3
message_bytes = <type>.to_bytes(2, 'big') + json.dumps(<payload>).encode('utf-8')
```

### For a funder to probe whether a fundee accepts zeroconf channels from the funder

> Note: this part is NOT included in the plugin

1. Generate a uuid4 string (call it `uuid`)
2. Send the peer a `custommsg` like this (encode into `message_bytes` using above):
    
    type(u16, 2-byte): `55443`
    payload:
    ```json
    {
        "id": <uuid>,
        "method": "getzeroconfinfo"
    }
    ```

### For a fundee to respond to the zeroconf probing request

> Note: this part IS included in the plugin

1. Get the request's uuid4 id (call it `uuid`)
2. Send the requester a `custommsg` like this (encode into `message_bytes` using above):
    
    type(u16, 2-byte): `55445`
    payload:
    ```json
    {
        "id": <uuid>,
        "result": {
            "allows_your_zeroconf": true  # or false if not allowed
        }
    }
    ```
